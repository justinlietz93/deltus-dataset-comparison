from typing import Protocol

from comparison_evidence.domain.models.comparison_result import ComparisonResult


class ResultStorePort(Protocol):
    def save(self, result: ComparisonResult) -> None: ...

    def get(self, run_id: str) -> ComparisonResult: ...
