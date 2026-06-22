from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ColumnStat:
    column_name: str
    compared_count: int
    match_count: int
    diff_count: int


@dataclass(frozen=True)
class RowDifference:
    key: dict[str, Any]
    column_name: str
    before_value: Any
    after_value: Any


@dataclass(frozen=True)
class ComparisonResult:
    run_id: str
    created_at: datetime
    before_row_count: int
    after_row_count: int
    compared_row_count: int
    missing_before_count: int
    missing_after_count: int
    changed_cell_count: int
    compared_cell_count: int
    column_stats: tuple[ColumnStat, ...] = ()
    detailed_differences: tuple[RowDifference, ...] = ()
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def cell_match_percent(self) -> float:
        if self.compared_cell_count == 0:
            return 0.0
        return 100.0 * (self.compared_cell_count - self.changed_cell_count) / self.compared_cell_count
