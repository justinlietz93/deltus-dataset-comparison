from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.ports.driven.dataset_source_port import DatasetSourcePort
from comparison_evidence.ports.driven.result_store_port import ResultStorePort


class RunComparisonUseCase:
    def __init__(self, source: DatasetSourcePort, store: ResultStorePort):
        self._source = source
        self._store = store

    def execute(self, contract: ComparisonContract) -> ComparisonResult:
        contract.require_valid()
        result = self._source.compare(contract)
        self._store.save(result)
        return result
