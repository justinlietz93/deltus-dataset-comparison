from __future__ import annotations

from pathlib import Path

from comparison_evidence.adapters.driven.export import HtmlReportExporter, XlsxExporter
from comparison_evidence.adapters.driven.local_files import LocalJsonResultStore
from comparison_evidence.application.use_cases.run_comparison import RunComparisonUseCase

from tests.conftest import contract


def test_run_comparison_use_case_persists_json_and_exports(tmp_path: Path, fixture_source) -> None:
    store = LocalJsonResultStore(tmp_path)
    use_case = RunComparisonUseCase(
        source=fixture_source,
        store=store,
        exporters=(HtmlReportExporter(), XlsxExporter()),
    )

    result = use_case.run_comparison(contract("identical_before", "changed_after"))
    run_dir = Path(store.run_dir(result.run_id))

    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "summary.json").exists()
    assert (run_dir / "schema_overlap.json").exists()
    assert (run_dir / "type_mismatches.json").exists()
    assert (run_dir / "column_stats.json").exists()
    assert (run_dir / "detailed_differences.json").exists()
    assert (run_dir / "missing_before.json").exists()
    assert (run_dir / "missing_after.json").exists()
    assert (run_dir / "report.html").exists()
    assert (run_dir / "report.xlsx").exists()

    loaded = use_case.load_run(result.run_id)
    assert loaded.run_id == result.run_id
    assert loaded.summary.changed_cell_count == 1
