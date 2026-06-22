from __future__ import annotations

from dataclasses import dataclass

from comparison_evidence.shared.identifiers import validate_safe_identifier


@dataclass(frozen=True)
class DatasetReference:
    source_id: str
    schema_name: str | None
    object_name: str
    display_name: str = ""

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("Dataset source_id is required.")
        validate_safe_identifier(self.object_name, label="object_name")
        if self.schema_name is not None:
            validate_safe_identifier(self.schema_name, label="schema_name")

    def label(self) -> str:
        if self.display_name:
            return self.display_name
        if self.schema_name:
            return f"{self.schema_name}.{self.object_name}"
        return self.object_name

    def qualified_name(self) -> str:
        if self.schema_name:
            return f"{self.schema_name}.{self.object_name}"
        return self.object_name
