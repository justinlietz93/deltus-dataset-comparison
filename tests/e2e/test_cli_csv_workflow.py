from pathlib import Path

from comparison_evidence.adapters.driving.cli.main import main


def test_cli_run_csv_exports_report_package(tmp_path: Path, capsys) -> None:
    before = tmp_path / "before.csv"
    after = tmp_path / "after.csv"
    before.write_text("id,name,status\n1,Ada,active\n2,Grace,active\n", encoding="utf-8")
    after.write_text("id,name,status\n1,Ada,active\n2,Grace,inactive\n", encoding="utf-8")
    export_root = tmp_path / "exports"

    status = main(
        [
            "run-csv",
            "--before-csv",
            str(before),
            "--after-csv",
            str(after),
            "--keys",
            "id",
            "--export-root",
            str(export_root),
        ]
    )

    assert status == 0
    output = capsys.readouterr().out
    artifact_line = next(line for line in output.splitlines() if line.startswith("artifact_dir="))
    artifact_dir = Path(artifact_line.split("=", 1)[1])
    assert (artifact_dir / "report.html").exists()
    assert (artifact_dir / "report.xlsx").exists()
    assert (artifact_dir / "result.json").exists()


def test_cli_run_csv_suite_exports_suite_and_candidate_reports(tmp_path: Path, capsys) -> None:
    export_root = tmp_path / "exports"

    status = main(
        [
            "run-csv-suite",
            "--manifest",
            "tests/fixtures/csv_suite/manifest.json",
            "--export-root",
            str(export_root),
        ]
    )

    assert status == 0
    output = capsys.readouterr().out
    artifact_line = next(line for line in output.splitlines() if line.startswith("artifact_dir="))
    artifact_dir = Path(artifact_line.split("=", 1)[1])
    assert (artifact_dir / "suite_report.html").exists()
    assert (artifact_dir / "suite_report.xlsx").exists()
    assert (artifact_dir / "suite_result.json").exists()
    assert (artifact_dir / "comparisons" / "candidate_a" / "report.html").exists()
    assert (artifact_dir / "comparisons" / "candidate_b" / "report.xlsx").exists()
