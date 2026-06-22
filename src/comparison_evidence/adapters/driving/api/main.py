from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from comparison_evidence.config.container import build_run_comparison_use_case
from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference

app = FastAPI(title="Deltus Dataset Comparison", version="0.1.0")
workflow = build_run_comparison_use_case()


class DatasetReferenceDTO(BaseModel):
    source_id: str
    schema_name: str | None = None
    object_name: str
    display_name: str = ""

    def to_domain(self) -> DatasetReference:
        return DatasetReference(**self.model_dump())


class ComparisonContractDTO(BaseModel):
    before: DatasetReferenceDTO
    after: DatasetReferenceDTO
    key_columns: list[str] = Field(min_length=1)
    excluded_columns: list[str] = []
    clear_nulls: bool = True
    numeric_precision: int | None = None
    max_detail_rows: int = 10_000

    def to_domain(self) -> ComparisonContract:
        return ComparisonContract(
            before=self.before.to_domain(),
            after=self.after.to_domain(),
            key_columns=tuple(self.key_columns),
            excluded_columns=tuple(self.excluded_columns),
            clear_nulls=self.clear_nulls,
            numeric_precision=self.numeric_precision,
            max_detail_rows=self.max_detail_rows,
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sources/{source_id}/tables")
def list_tables(source_id: str) -> list[dict[str, Any]]:
    return [table.__dict__ for table in workflow.list_tables(source_id)]


@app.post("/schema/inspect")
def inspect_schema(dataset: DatasetReferenceDTO) -> dict[str, Any]:
    try:
        return workflow.inspect_schema(dataset.to_domain()).__dict__
    except Exception as exc:  # noqa: BLE001 - API boundary translates adapter/domain errors.
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/comparison/validate")
def validate_comparison(contract: ComparisonContractDTO) -> dict[str, Any]:
    try:
        messages = workflow.validate_comparison(contract.to_domain())
        return {"valid": not messages, "messages": list(messages)}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/comparison/run")
def run_comparison(contract: ComparisonContractDTO) -> dict[str, Any]:
    try:
        result = workflow.run_comparison(contract.to_domain())
        return {
            "run_id": result.run_id,
            "summary": result.to_dict()["summary"],
            "artifact_dir": workflow._store.run_dir(result.run_id),  # noqa: SLF001
        }
    except ContractValidationError as exc:
        raise HTTPException(status_code=422, detail=list(exc.messages)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/runs/{run_id}")
def load_run(run_id: str) -> dict[str, Any]:
    try:
        return workflow.load_run(run_id).to_dict()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/runs/{run_id}/artifacts")
def list_run_artifacts(run_id: str) -> dict[str, Any]:
    try:
        result = workflow.load_run(run_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    artifact_dir = workflow._store.run_dir(result.run_id)  # noqa: SLF001
    return {
        "run_id": run_id,
        "artifact_dir": artifact_dir,
        "artifacts": [
            "manifest.json",
            "summary.json",
            "schema_overlap.json",
            "type_mismatches.json",
            "column_stats.json",
            "detailed_differences.json",
            "missing_before.json",
            "missing_after.json",
            "report.html",
            "report.xlsx",
        ],
    }


@app.get("/runs/{run_id}/artifacts/{artifact_name}")
def download_run_artifact(run_id: str, artifact_name: str) -> FileResponse:
    allowed = {
        "manifest.json",
        "summary.json",
        "schema_overlap.json",
        "type_mismatches.json",
        "column_stats.json",
        "detailed_differences.json",
        "missing_before.json",
        "missing_after.json",
        "duplicate_keys.json",
        "warnings.json",
        "report.html",
        "report.xlsx",
    }
    if artifact_name not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported artifact name.")
    try:
        result = workflow.load_run(run_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    path = Path(workflow._store.run_dir(result.run_id)) / artifact_name  # noqa: SLF001
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Artifact not found: {artifact_name}")
    return FileResponse(path)
