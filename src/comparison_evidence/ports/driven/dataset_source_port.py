from typing import Protocol

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import SchemaProfile


class DatasetSourcePort(Protocol):
    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile: ...

    def compare(self, contract: ComparisonContract) -> ComparisonResult: ...
