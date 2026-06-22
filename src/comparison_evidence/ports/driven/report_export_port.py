from typing import Protocol

from comparison_evidence.domain.models.comparison_result import ComparisonResult


class ReportExportPort(Protocol):
    def export(self, result: ComparisonResult, output_dir: str) -> list[str]: ...
