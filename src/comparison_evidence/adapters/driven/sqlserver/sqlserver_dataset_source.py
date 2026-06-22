from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import SchemaProfile


class SqlServerDatasetSource:
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile:
        raise NotImplementedError("Implement SQL Server schema inspection first.")

    def compare(self, contract: ComparisonContract) -> ComparisonResult:
        raise NotImplementedError("Wrap the existing stored procedure result contract here.")
