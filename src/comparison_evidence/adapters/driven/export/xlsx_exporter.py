from comparison_evidence.domain.models.comparison_result import ComparisonResult


class XlsxExporter:
    def export(self, result: ComparisonResult, output_dir: str) -> list[str]:
        raise NotImplementedError("Create workbook tabs from the result contract.")
