from __future__ import annotations

from dataclasses import asdict, dataclass

from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.shared.identifiers import validate_safe_identifier


@dataclass(frozen=True)
class ComparisonContract:
    before: DatasetReference
    after: DatasetReference
    key_columns: tuple[str, ...]
    excluded_columns: tuple[str, ...] = ()
    clear_nulls: bool = True
    numeric_precision: int | None = None
    max_detail_rows: int = 10_000

    def require_valid(self) -> None:
        messages: list[str] = []
        if not self.key_columns:
            messages.append("At least one key column is required.")
        if len(set(self.key_columns)) != len(self.key_columns):
            messages.append("Duplicate key columns are not allowed.")
        if len(set(self.excluded_columns)) != len(self.excluded_columns):
            messages.append("Duplicate excluded columns are not allowed.")
        overlap = set(self.key_columns).intersection(self.excluded_columns)
        if overlap:
            messages.append(f"Key columns cannot be excluded: {sorted(overlap)}")
        if self.numeric_precision is not None and self.numeric_precision < 0:
            messages.append("numeric_precision must be zero or greater when provided.")
        if self.max_detail_rows < 0:
            messages.append("max_detail_rows must be zero or greater.")
        for column in (*self.key_columns, *self.excluded_columns):
            try:
                validate_safe_identifier(column, label="column")
            except ValueError as exc:
                messages.append(str(exc))
        if messages:
            raise ValueError("; ".join(messages))

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["before"] = asdict(self.before)
        data["after"] = asdict(self.after)
        data["key_columns"] = list(self.key_columns)
        data["excluded_columns"] = list(self.excluded_columns)
        return data
