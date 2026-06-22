from __future__ import annotations

from pathlib import Path

from comparison_evidence.adapters.driving.cli.main import main


def test_cli_sqlite_workflow_exports_evidence(tmp_path: Path, capsys) -> None:
    status = main(
        [
            "run-sqlite",
            "--database",
            "tests/fixtures/mvp_cases.sqlite",
            "--before",
            "identical_before",
            "--after",
            "changed_after",
            "--keys",
            "id",
            "--export-root",
            str(tmp_path),
        ]
    )

    assert status == 0
    output = capsys.readouterr().out
    assert "changed_cells=1" in output
    artifact_line = next(line for line in output.splitlines() if line.startswith("artifact_dir="))
    artifact_dir = Path(artifact_line.split("=", 1)[1])
    assert (artifact_dir / "result.json").exists()
    assert (artifact_dir / "report.html").exists()
    assert (artifact_dir / "report.xlsx").exists()
