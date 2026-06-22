from typing import Protocol

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.schema_profile import SchemaProfile


class ComparisonWorkflowPort(Protocol):
    def inspect_schema(self, source_id: str, object_name: str) -> SchemaProfile: ...

    def run_comparison(self, contract: ComparisonContract) -> ComparisonResult: ...
