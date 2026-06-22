from __future__ import annotations

from fastapi.testclient import TestClient

from comparison_evidence.adapters.driving.api.main import app


def test_api_fixture_workflow_runs_and_serves_artifacts() -> None:
    client = TestClient(app)

    assert client.get("/health").json() == {"status": "ok"}
    tables = client.get("/sources/fixture/tables").json()
    assert any(table["object_name"] == "identical_before" for table in tables)

    payload = {
        "before": {"source_id": "fixture", "schema_name": "dbo", "object_name": "identical_before"},
        "after": {"source_id": "fixture", "schema_name": "dbo", "object_name": "changed_after"},
        "key_columns": ["id"],
        "excluded_columns": [],
    }
    validation = client.post("/comparison/validate", json=payload).json()
    assert validation == {"valid": True, "messages": []}

    run_response = client.post("/comparison/run", json=payload).json()
    assert run_response["summary"]["changed_cell_count"] == 1
    run_id = run_response["run_id"]

    loaded = client.get(f"/runs/{run_id}").json()
    assert loaded["summary"]["changed_cell_count"] == 1

    artifacts = client.get(f"/runs/{run_id}/artifacts").json()
    assert "report.html" in artifacts["artifacts"]

    html = client.get(f"/runs/{run_id}/artifacts/report.html")
    assert html.status_code == 200
    assert "Deltus Evidence Report" in html.text
