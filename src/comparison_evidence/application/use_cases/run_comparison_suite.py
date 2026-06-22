from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_suite_contract import ComparisonSuiteContract
from comparison_evidence.domain.models.comparison_suite_result import (
    ComparisonSuiteResult,
    SuiteManifest,
    build_candidate_summary,
    build_suite_summary,
)
from comparison_evidence.ports.driven.dataset_source_port import DatasetSourcePort

TOOL_VERSION = "0.1.2"


class RunComparisonSuiteUseCase:
    def __init__(self, source: DatasetSourcePort):
        self._source = source

    def validate_suite(self, suite: ComparisonSuiteContract) -> tuple[str, ...]:
        messages: list[str] = []
        try:
            suite.require_valid()
        except ValueError as exc:
            messages.extend(str(exc).split("; "))
            return tuple(messages)
        for index, contract in enumerate(suite.comparison_contracts(), start=1):
            contract_messages = self._source.validate_contract(contract)
            if contract_messages:
                candidate = contract.after.label()
                messages.extend(f"candidate {index} ({candidate}): {message}" for message in contract_messages)
        return tuple(messages)

    def run_suite(self, suite: ComparisonSuiteContract) -> ComparisonSuiteResult:
        messages = self.validate_suite(suite)
        if messages:
            raise ContractValidationError(list(messages))

        created_at = datetime.now(UTC)
        suite_id = f"suite_{suite.suite_name}_{created_at.strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
        results = tuple(self._source.compare(contract) for contract in suite.comparison_contracts())
        candidate_summaries = tuple(build_candidate_summary(result) for result in results)
        manifest = SuiteManifest(
            suite_id=suite_id,
            suite_name=suite.suite_name,
            created_at=created_at,
            tool_name="Deltus Dataset Comparison",
            tool_version=TOOL_VERSION,
            baseline_label=suite.baseline.label(),
            candidate_count=len(suite.candidates),
            key_columns=suite.key_columns,
            excluded_columns=suite.excluded_columns,
            clear_nulls=suite.clear_nulls,
            numeric_precision=suite.numeric_precision,
            max_detail_rows=suite.max_detail_rows,
        )
        suite_warnings = _suite_warnings(candidate_summaries)
        return ComparisonSuiteResult(
            manifest=manifest,
            summary=build_suite_summary(candidate_summaries),
            candidate_summaries=candidate_summaries,
            results=results,
            warnings=suite_warnings,
        )

    def execute(self, suite: ComparisonSuiteContract) -> ComparisonSuiteResult:
        return self.run_suite(suite)


def _suite_warnings(candidate_summaries):
    warnings: list[str] = []
    if any(summary.status == "FAIL" for summary in candidate_summaries):
        warnings.append("One or more candidates produced missing rows, duplicate keys, or schema/type issues.")
    if any(summary.status == "WARN" for summary in candidate_summaries):
        warnings.append("One or more candidates produced changed cells without hard-fail conditions.")
    return tuple(warnings)
