from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import UTC, datetime
from typing import Any


JsonDict = dict[str, Any]


@dataclass(frozen=True)
class SchemaOverlap:
    common_columns: tuple[str, ...]
    comparable_columns: tuple[str, ...]
    before_only_columns: tuple[str, ...]
    after_only_columns: tuple[str, ...]
    excluded_columns: tuple[str, ...]
    key_columns: tuple[str, ...]


@dataclass(frozen=True)
class TypeMismatch:
    column_name: str
    before_type: str
    after_type: str


@dataclass(frozen=True)
class ColumnStat:
    column_name: str
    compared_count: int
    match_count: int
    diff_count: int

    @property
    def match_percent(self) -> float:
        if self.compared_count == 0:
            return 0.0
        return 100.0 * self.match_count / self.compared_count


@dataclass(frozen=True)
class RowDifference:
    key: JsonDict
    column_name: str
    before_value: Any
    after_value: Any


@dataclass(frozen=True)
class MissingRow:
    key: JsonDict
    side: str
    row: JsonDict


@dataclass(frozen=True)
class DuplicateKeyWarning:
    side: str
    key: JsonDict
    count: int


@dataclass(frozen=True)
class EvidenceManifest:
    run_id: str
    created_at: datetime
    tool_name: str
    tool_version: str
    before_label: str
    after_label: str
    key_columns: tuple[str, ...]
    excluded_columns: tuple[str, ...]
    clear_nulls: bool
    numeric_precision: int | None
    max_detail_rows: int


@dataclass(frozen=True)
class ComparisonSummary:
    before_row_count: int
    after_row_count: int
    matched_key_count: int
    compared_row_count: int
    missing_before_count: int
    missing_after_count: int
    changed_cell_count: int
    compared_cell_count: int
    type_mismatch_count: int
    duplicate_key_count: int
    warning_count: int

    @property
    def cell_match_percent(self) -> float:
        if self.compared_cell_count == 0:
            return 0.0
        return 100.0 * (self.compared_cell_count - self.changed_cell_count) / self.compared_cell_count


@dataclass(frozen=True)
class ComparisonResult:
    manifest: EvidenceManifest
    summary: ComparisonSummary
    schema_overlap: SchemaOverlap
    type_mismatches: tuple[TypeMismatch, ...] = ()
    column_stats: tuple[ColumnStat, ...] = ()
    detailed_differences: tuple[RowDifference, ...] = ()
    missing_before: tuple[MissingRow, ...] = ()
    missing_after: tuple[MissingRow, ...] = ()
    duplicate_keys: tuple[DuplicateKeyWarning, ...] = ()
    warnings: tuple[str, ...] = field(default_factory=tuple)
    failures: tuple[str, ...] = field(default_factory=tuple)

    @property
    def run_id(self) -> str:
        return self.manifest.run_id

    @property
    def created_at(self) -> datetime:
        return self.manifest.created_at

    @property
    def before_row_count(self) -> int:
        return self.summary.before_row_count

    @property
    def after_row_count(self) -> int:
        return self.summary.after_row_count

    @property
    def compared_row_count(self) -> int:
        return self.summary.compared_row_count

    @property
    def missing_before_count(self) -> int:
        return self.summary.missing_before_count

    @property
    def missing_after_count(self) -> int:
        return self.summary.missing_after_count

    @property
    def changed_cell_count(self) -> int:
        return self.summary.changed_cell_count

    @property
    def compared_cell_count(self) -> int:
        return self.summary.compared_cell_count

    @property
    def cell_match_percent(self) -> float:
        return self.summary.cell_match_percent

    def to_dict(self) -> JsonDict:
        return _to_jsonable(self)


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
