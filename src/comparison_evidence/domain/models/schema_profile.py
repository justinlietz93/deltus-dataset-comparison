from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    data_type: str
    nullable: bool
    ordinal: int


@dataclass(frozen=True)
class SchemaProfile:
    dataset_label: str
    columns: tuple[ColumnProfile, ...]

    def names(self) -> set[str]:
        return {column.name for column in self.columns}
