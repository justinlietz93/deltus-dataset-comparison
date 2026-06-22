from dataclasses import dataclass

from comparison_evidence.domain.models.dataset_reference import DatasetReference


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
        if not self.key_columns:
            raise ValueError("At least one key column is required.")
        if len(set(self.key_columns)) != len(self.key_columns):
            raise ValueError("Duplicate key columns are not allowed.")
        overlap = set(self.key_columns).intersection(self.excluded_columns)
        if overlap:
            raise ValueError(f"Key columns cannot be excluded: {sorted(overlap)}")
