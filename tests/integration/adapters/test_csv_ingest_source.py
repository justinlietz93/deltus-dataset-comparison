from pathlib import Path

from comparison_evidence.adapters.driven.csv import CsvToSqliteIngestAdapter
from comparison_evidence.application.use_cases.run_comparison import RunComparisonUseCase
from comparison_evidence.adapters.driven.local_files import LocalJsonResultStore


def test_csv_pair_ingests_to_sqlite_and_reuses_comparison_engine(tmp_path):
    before = tmp_path / "before.csv"
    after = tmp_path / "after.csv"
    before.write_text("id,name,status\n1,Ada,active\n2,Grace,active\n", encoding="utf-8")
    after.write_text("id,name,status\n1,Ada,active\n2,Grace,inactive\n", encoding="utf-8")

    ingester = CsvToSqliteIngestAdapter(tmp_path / "csv.sqlite")
    contract = ingester.ingest_pair(
        before,
        after,
        key_columns=("id",),
        before_name="baseline",
        after_name="candidate",
    )
    use_case = RunComparisonUseCase(
        source=ingester.sqlite_source(),
        store=LocalJsonResultStore(tmp_path / "exports"),
    )

    result = use_case.run_comparison(contract)

    assert result.summary.changed_cell_count == 1
    assert result.detailed_differences[0].column_name == "status"


def test_csv_suite_manifest_ingests_baseline_and_candidates(tmp_path):
    fixture_dir = Path("tests/fixtures/csv_suite")
    ingester = CsvToSqliteIngestAdapter(tmp_path / "suite.sqlite")

    suite = ingester.ingest_suite_manifest(fixture_dir / "manifest.json")

    assert suite.suite_name == "customer_change_suite"
    assert suite.baseline.object_name == "baseline"
    assert [candidate.object_name for candidate in suite.candidates] == ["candidate_a", "candidate_b"]
