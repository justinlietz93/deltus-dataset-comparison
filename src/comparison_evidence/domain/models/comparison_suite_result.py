from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import UTC, datetime
from typing import Any

from comparison_evidence.domain.models.comparison_result import ComparisonResult

JsonDict = dict[str, Any]


@dataclass(frozen=True)
class SuiteManifest:
    suite_id: str
    suite_name: str
    created_at: datetime
    tool_name: str
    tool_version: str
    baseline_label: str
    candidate_count: int
    key_columns: tuple[str, ...]
    excluded_columns: tuple[str, ...]
    clear_nulls: bool
    numeric_precision: int | None
    max_detail_rows: int


@dataclass(frozen=True)
class CandidateSuiteSummary:
    candidate_label: str
    run_id: str
    status: str
    difference_score: int
    changed_cell_count: int
    missing_before_count: int
    missing_after_count: int
    type_mismatch_count: int
    duplicate_key_count: int
    warning_count: int
    compared_cell_count: int
    cell_match_percent: float


@dataclass(frozen=True)
class SuiteSummary:
    candidate_count: int
    pass_count: int
    warn_count: int
    fail_count: int
    total_changed_cell_count: int
    total_missing_before_count: int
    total_missing_after_count: int
    candidates_with_warnings: int
    best_candidate_label: str | None
    best_candidate_score: int | None


@dataclass(frozen=True)
class ComparisonSuiteResult:
    manifest: SuiteManifest
    summary: SuiteSummary
    candidate_summaries: tuple[CandidateSuiteSummary, ...]
    results: tuple[ComparisonResult, ...]
    warnings: tuple[str, ...] = ()

    @property
    def suite_id(self) -> str:
        return self.manifest.suite_id

    @property
    def created_at(self) -> datetime:
        return self.manifest.created_at

    def to_dict(self) -> JsonDict:
        return _to_jsonable(self)


def build_candidate_summary(result: ComparisonResult) -> CandidateSuiteSummary:
    summary = result.summary
    difference_score = (
        summary.changed_cell_count
        + summary.missing_before_count
        + summary.missing_after_count
        + summary.type_mismatch_count
        + summary.duplicate_key_count
    )
    status = _status_for_result(result)
    return CandidateSuiteSummary(
        candidate_label=result.manifest.after_label,
        run_id=result.run_id,
        status=status,
        difference_score=difference_score,
        changed_cell_count=summary.changed_cell_count,
        missing_before_count=summary.missing_before_count,
        missing_after_count=summary.missing_after_count,
        type_mismatch_count=summary.type_mismatch_count,
        duplicate_key_count=summary.duplicate_key_count,
        warning_count=summary.warning_count,
        compared_cell_count=summary.compared_cell_count,
        cell_match_percent=summary.cell_match_percent,
    )


def build_suite_summary(candidate_summaries: tuple[CandidateSuiteSummary, ...]) -> SuiteSummary:
    best = min(candidate_summaries, key=lambda item: (item.difference_score, item.candidate_label), default=None)
    return SuiteSummary(
        candidate_count=len(candidate_summaries),
        pass_count=sum(1 for item in candidate_summaries if item.status == "PASS"),
        warn_count=sum(1 for item in candidate_summaries if item.status == "WARN"),
        fail_count=sum(1 for item in candidate_summaries if item.status == "FAIL"),
        total_changed_cell_count=sum(item.changed_cell_count for item in candidate_summaries),
        total_missing_before_count=sum(item.missing_before_count for item in candidate_summaries),
        total_missing_after_count=sum(item.missing_after_count for item in candidate_summaries),
        candidates_with_warnings=sum(1 for item in candidate_summaries if item.warning_count > 0),
        best_candidate_label=None if best is None else best.candidate_label,
        best_candidate_score=None if best is None else best.difference_score,
    )


def _status_for_result(result: ComparisonResult) -> str:
    summary = result.summary
    if (
        result.failures
        or summary.duplicate_key_count > 0
        or summary.type_mismatch_count > 0
        or summary.missing_before_count > 0
        or summary.missing_after_count > 0
    ):
        return "FAIL"
    if summary.changed_cell_count > 0 or result.warnings:
        return "WARN"
    return "PASS"


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if is_dataclass(value):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value
