from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetReference:
    source_id: str
    schema_name: str | None
    object_name: str
    display_name: str

    def label(self) -> str:
        if self.schema_name:
            return f"{self.schema_name}.{self.object_name}"
        return self.object_name
