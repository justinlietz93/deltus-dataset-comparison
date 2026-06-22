from __future__ import annotations

from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import SchemaProfile
from comparison_evidence.ports.driven.dataset_source_port import DatasetSourcePort
from comparison_evidence.ports.driven.report_export_port import ReportExportPort
from comparison_evidence.ports.driven.result_store_port import ResultStorePort


class RunComparisonUseCase:
    def __init__(
        self,
        source: DatasetSourcePort,
        store: ResultStorePort,
        exporters: tuple[ReportExportPort, ...] = (),
    ):
        self._source = source
        self._store = store
        self._exporters = exporters

    def list_tables(self, source_id: str) -> tuple[DatasetReference, ...]:
        return self._source.list_tables(source_id)

    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile:
        return self._source.inspect_schema(dataset)

    def validate_comparison(self, contract: ComparisonContract) -> tuple[str, ...]:
        return self._source.validate_contract(contract)

    def run_comparison(self, contract: ComparisonContract) -> ComparisonResult:
        messages = self.validate_comparison(contract)
        if messages:
            raise ContractValidationError(list(messages))
        result = self._source.compare(contract)
        self._store.save(result)
        run_dir = self._store.run_dir(result.run_id)
        for exporter in self._exporters:
            exporter.export(result, run_dir)
        return result

    def execute(self, contract: ComparisonContract) -> ComparisonResult:
        return self.run_comparison(contract)

    def load_run(self, run_id: str) -> ComparisonResult:
        return self._store.get(run_id)
