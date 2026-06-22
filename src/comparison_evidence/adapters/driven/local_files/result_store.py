from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from comparison_evidence.domain.models.comparison_result import (
    ColumnStat,
    ComparisonResult,
    ComparisonSummary,
    DuplicateKeyWarning,
    EvidenceManifest,
    MissingRow,
    RowDifference,
    SchemaOverlap,
    TypeMismatch,
)
from comparison_evidence.domain.models.comparison_suite_result import (
    CandidateSuiteSummary,
    ComparisonSuiteResult,
    SuiteManifest,
    SuiteSummary,
)


class LocalJsonResultStore:
    def __init__(self, root: str | Path):
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)

    def save(self, result: ComparisonResult) -> None:
        save_result_package(result, self.run_dir(result.run_id))

    def get(self, run_id: str) -> ComparisonResult:
        path = Path(self.run_dir(run_id)) / "result.json"
        if not path.exists():
            raise FileNotFoundError(f"No result found for run_id={run_id}")
        return comparison_result_from_dict(json.loads(path.read_text(encoding="utf-8")))

    def run_dir(self, run_id: str) -> str:
        return str(self._root / run_id)


class LocalJsonSuiteResultStore:
    def __init__(self, root: str | Path):
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)

    def save(self, suite_result: ComparisonSuiteResult) -> None:
        suite_dir = Path(self.suite_dir(suite_result.suite_id))
        suite_dir.mkdir(parents=True, exist_ok=True)
        data = suite_result.to_dict()
        _write_json(suite_dir / "suite_result.json", data)
        _write_json(suite_dir / "suite_manifest.json", data["manifest"])
        _write_json(suite_dir / "suite_summary.json", data["summary"])
        _write_json(suite_dir / "candidate_summaries.json", data["candidate_summaries"])
        _write_json(suite_dir / "suite_warnings.json", data["warnings"])
        comparisons_dir = suite_dir / "comparisons"
        comparisons_dir.mkdir(exist_ok=True)
        for result in suite_result.results:
            candidate_dir = comparisons_dir / _safe_path_segment(result.manifest.after_label)
            save_result_package(result, candidate_dir)

    def suite_dir(self, suite_id: str) -> str:
        return str(self._root / suite_id)


def save_result_package(result: ComparisonResult, output_dir: str | Path) -> None:
    run_dir = Path(output_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    data = result.to_dict()
    _write_json(run_dir / "result.json", data)
    _write_json(run_dir / "manifest.json", data["manifest"])
    _write_json(run_dir / "summary.json", data["summary"])
    _write_json(run_dir / "schema_overlap.json", data["schema_overlap"])
    _write_json(run_dir / "type_mismatches.json", data["type_mismatches"])
    _write_json(run_dir / "column_stats.json", data["column_stats"])
    _write_json(run_dir / "detailed_differences.json", data["detailed_differences"])
    _write_json(run_dir / "missing_before.json", data["missing_before"])
    _write_json(run_dir / "missing_after.json", data["missing_after"])
    _write_json(run_dir / "duplicate_keys.json", data["duplicate_keys"])
    _write_json(run_dir / "warnings.json", data["warnings"])


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str), encoding="utf-8")


def comparison_result_from_dict(data: dict[str, Any]) -> ComparisonResult:
    manifest_data = data["manifest"]
    manifest = EvidenceManifest(
        run_id=manifest_data["run_id"],
        created_at=_parse_datetime(manifest_data["created_at"]),
        tool_name=manifest_data["tool_name"],
        tool_version=manifest_data["tool_version"],
        before_label=manifest_data["before_label"],
        after_label=manifest_data["after_label"],
        key_columns=tuple(manifest_data["key_columns"]),
        excluded_columns=tuple(manifest_data["excluded_columns"]),
        clear_nulls=manifest_data["clear_nulls"],
        numeric_precision=manifest_data["numeric_precision"],
        max_detail_rows=manifest_data["max_detail_rows"],
    )
    summary = ComparisonSummary(**data["summary"])
    overlap = data["schema_overlap"]
    schema_overlap = SchemaOverlap(
        common_columns=tuple(overlap["common_columns"]),
        comparable_columns=tuple(overlap["comparable_columns"]),
        before_only_columns=tuple(overlap["before_only_columns"]),
        after_only_columns=tuple(overlap["after_only_columns"]),
        excluded_columns=tuple(overlap["excluded_columns"]),
        key_columns=tuple(overlap["key_columns"]),
    )
    return ComparisonResult(
        manifest=manifest,
        summary=summary,
        schema_overlap=schema_overlap,
        type_mismatches=tuple(TypeMismatch(**item) for item in data.get("type_mismatches", [])),
        column_stats=tuple(ColumnStat(**item) for item in data.get("column_stats", [])),
        detailed_differences=tuple(RowDifference(**item) for item in data.get("detailed_differences", [])),
        missing_before=tuple(MissingRow(**item) for item in data.get("missing_before", [])),
        missing_after=tuple(MissingRow(**item) for item in data.get("missing_after", [])),
        duplicate_keys=tuple(DuplicateKeyWarning(**item) for item in data.get("duplicate_keys", [])),
        warnings=tuple(data.get("warnings", [])),
        failures=tuple(data.get("failures", [])),
    )


def comparison_suite_result_from_dict(data: dict[str, Any]) -> ComparisonSuiteResult:
    manifest_data = data["manifest"]
    manifest = SuiteManifest(
        suite_id=manifest_data["suite_id"],
        suite_name=manifest_data["suite_name"],
        created_at=_parse_datetime(manifest_data["created_at"]),
        tool_name=manifest_data["tool_name"],
        tool_version=manifest_data["tool_version"],
        baseline_label=manifest_data["baseline_label"],
        candidate_count=manifest_data["candidate_count"],
        key_columns=tuple(manifest_data["key_columns"]),
        excluded_columns=tuple(manifest_data["excluded_columns"]),
        clear_nulls=manifest_data["clear_nulls"],
        numeric_precision=manifest_data["numeric_precision"],
        max_detail_rows=manifest_data["max_detail_rows"],
    )
    summary = SuiteSummary(**data["summary"])
    candidates = tuple(CandidateSuiteSummary(**item) for item in data.get("candidate_summaries", []))
    results = tuple(comparison_result_from_dict(item) for item in data.get("results", []))
    return ComparisonSuiteResult(
        manifest=manifest,
        summary=summary,
        candidate_summaries=candidates,
        results=results,
        warnings=tuple(data.get("warnings", [])),
    )


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _safe_path_segment(value: str) -> str:
    safe = "".join(character if character.isalnum() or character in "_-" else "_" for character in value)
    safe = safe.strip("_")
    return safe or "candidate"
