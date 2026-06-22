from __future__ import annotations

from typing import Protocol

from comparison_evidence.domain.models.comparison_result import ComparisonResult


class ReportExportPort(Protocol):
    artifact_name: str

    def export(self, result: ComparisonResult, output_dir: str) -> str: ...
