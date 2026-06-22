from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import ColumnProfile, SchemaProfile
from comparison_evidence.domain.services.comparison_engine import TabularComparisonEngine

Row = dict[str, Any]


class FixtureDatasetSource:
    def __init__(self, datasets: dict[str, tuple[SchemaProfile, list[Row]]]):
        self._datasets = datasets
        self._engine = TabularComparisonEngine()

    @classmethod
    def from_json_file(cls, path: str | Path) -> "FixtureDatasetSource":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        datasets: dict[str, tuple[SchemaProfile, list[Row]]] = {}
        for item in data["datasets"]:
            ref = DatasetReference(
                source_id=item.get("source_id", "fixture"),
                schema_name=item.get("schema_name"),
                object_name=item["object_name"],
                display_name=item.get("display_name", ""),
            )
            columns = tuple(
                ColumnProfile(
                    name=column["name"],
                    data_type=column.get("data_type", "nvarchar"),
                    nullable=column.get("nullable", True),
                    ordinal=column.get("ordinal", index),
                    precision=column.get("precision"),
                    scale=column.get("scale"),
                )
                for index, column in enumerate(item["columns"])
            )
            datasets[_dataset_key(ref)] = (SchemaProfile(ref.label(), columns), item["rows"])
        return cls(datasets)

    def list_tables(self, source_id: str) -> tuple[DatasetReference, ...]:
        refs: list[DatasetReference] = []
        for key in sorted(self._datasets):
            source, qualified = key.split(":", 1)
            if source != source_id:
                continue
            parts = qualified.split(".", 1)
            schema_name = parts[0] if len(parts) == 2 else None
            object_name = parts[1] if len(parts) == 2 else parts[0]
            refs.append(DatasetReference(source_id=source, schema_name=schema_name, object_name=object_name))
        return tuple(refs)

    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile:
        schema, _ = self._get_dataset(dataset)
        return schema

    def validate_contract(self, contract: ComparisonContract) -> tuple[str, ...]:
        before_schema = self.inspect_schema(contract.before)
        after_schema = self.inspect_schema(contract.after)
        return self._engine.validate_contract(contract, before_schema, after_schema)

    def compare(self, contract: ComparisonContract) -> ComparisonResult:
        before_schema, before_rows = self._get_dataset(contract.before)
        after_schema, after_rows = self._get_dataset(contract.after)
        return self._engine.compare(contract, before_schema, after_schema, before_rows, after_rows)

    def _get_dataset(self, reference: DatasetReference) -> tuple[SchemaProfile, list[Row]]:
        key = _dataset_key(reference)
        try:
            return self._datasets[key]
        except KeyError as exc:
            raise KeyError(f"Dataset not found: {reference.qualified_name()}") from exc


def _dataset_key(reference: DatasetReference) -> str:
    return f"{reference.source_id}:{reference.qualified_name()}"
