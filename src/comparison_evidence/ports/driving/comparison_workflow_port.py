from __future__ import annotations

from typing import Protocol

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import SchemaProfile


class ComparisonWorkflowPort(Protocol):
    def list_tables(self, source_id: str) -> tuple[DatasetReference, ...]: ...

    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile: ...

    def validate_comparison(self, contract: ComparisonContract) -> tuple[str, ...]: ...

    def run_comparison(self, contract: ComparisonContract) -> ComparisonResult: ...

    def load_run(self, run_id: str) -> ComparisonResult: ...
