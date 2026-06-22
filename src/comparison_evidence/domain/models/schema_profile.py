from __future__ import annotations

from dataclasses import dataclass

from comparison_evidence.shared.identifiers import validate_safe_identifier


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    data_type: str
    nullable: bool = True
    ordinal: int = 0
    precision: int | None = None
    scale: int | None = None

    def __post_init__(self) -> None:
        validate_safe_identifier(self.name, label="column_name")
        if not self.data_type:
            raise ValueError(f"Column {self.name!r} requires a data_type.")

    def normalized_type(self) -> str:
        return self.data_type.strip().lower()


@dataclass(frozen=True)
class SchemaProfile:
    dataset_label: str
    columns: tuple[ColumnProfile, ...]

    def names(self) -> set[str]:
        return {column.name for column in self.columns}

    def column_map(self) -> dict[str, ColumnProfile]:
        return {column.name: column for column in self.columns}

    def require_columns(self, columns: tuple[str, ...], *, label: str) -> None:
        missing = sorted(set(columns) - self.names())
        if missing:
            raise ValueError(f"{label} missing columns: {missing}")
