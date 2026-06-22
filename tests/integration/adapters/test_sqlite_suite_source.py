from comparison_evidence.adapters.driven.csv import CsvToSqliteIngestAdapter
from comparison_evidence.application.use_cases.run_comparison_suite import RunComparisonSuiteUseCase


def test_sqlite_suite_runner_compares_baseline_against_many_candidates(tmp_path):
    ingester = CsvToSqliteIngestAdapter(tmp_path / "suite.sqlite")
    suite = ingester.ingest_suite_manifest("tests/fixtures/csv_suite/manifest.json")
    use_case = RunComparisonSuiteUseCase(source=ingester.sqlite_source())

    result = use_case.run_suite(suite)

    statuses = {item.candidate_label: item.status for item in result.candidate_summaries}
    assert statuses["candidate_a"] == "PASS"
    assert statuses["candidate_b"] == "FAIL"
    assert result.summary.best_candidate_label == "candidate_a"
    assert result.summary.candidate_count == 2
