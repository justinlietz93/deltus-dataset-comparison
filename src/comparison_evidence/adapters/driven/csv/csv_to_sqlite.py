from __future__ import annotations

import csv
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from comparison_evidence.adapters.driven.sqlite import SqliteDatasetSource
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_suite_contract import ComparisonSuiteContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference


@dataclass(frozen=True)
class CsvDatasetSpec:
    name: str
    path: Path


class CsvToSqliteIngestAdapter:
    def __init__(
        self,
        database_path: str | Path,
        *,
        source_id: str = "csv_sqlite",
        delimiter: str = ",",
        encoding: str = "utf-8",
        null_tokens: tuple[str, ...] = ("",),
        replace: bool = True,
    ):
        self._database_path = Path(database_path)
        self._source_id = source_id
        self._delimiter = delimiter
        self._encoding = encoding
        self._null_tokens = null_tokens
        self._replace = replace
        self._database_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def database_path(self) -> Path:
        return self._database_path

    @property
    def source_id(self) -> str:
        return self._source_id

    def sqlite_source(self) -> SqliteDatasetSource:
        return SqliteDatasetSource(self._database_path, source_id=self._source_id)

    def ingest_dataset(self, spec: CsvDatasetSpec) -> DatasetReference:
        table_name = _safe_table_name(spec.name)
        rows, headers = self._read_csv(spec.path)
        self._write_table(table_name, headers, rows)
        return DatasetReference(
            source_id=self._source_id,
            schema_name=None,
            object_name=table_name,
            display_name=spec.name,
        )

    def ingest_pair(
        self,
        before_path: str | Path,
        after_path: str | Path,
        *,
        before_name: str = "before",
        after_name: str = "after",
        key_columns: tuple[str, ...],
        excluded_columns: tuple[str, ...] = (),
        clear_nulls: bool = True,
        numeric_precision: int | None = None,
        max_detail_rows: int = 10_000,
    ) -> ComparisonContract:
        before = self.ingest_dataset(CsvDatasetSpec(before_name, Path(before_path)))
        after = self.ingest_dataset(CsvDatasetSpec(after_name, Path(after_path)))
        return ComparisonContract(
            before=before,
            after=after,
            key_columns=key_columns,
            excluded_columns=excluded_columns,
            clear_nulls=clear_nulls,
            numeric_precision=numeric_precision,
            max_detail_rows=max_detail_rows,
        )

    def ingest_suite_manifest(self, manifest_path: str | Path) -> ComparisonSuiteContract:
        path = Path(manifest_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        base_dir = path.parent
        suite_name = _safe_table_name(str(data.get("suite_name", "csv_suite")))
        delimiter = str(data.get("delimiter", self._delimiter))
        encoding = str(data.get("encoding", self._encoding))
        self._delimiter = delimiter
        self._encoding = encoding

        baseline_data = data["baseline"]
        baseline = self.ingest_dataset(
            CsvDatasetSpec(
                name=str(baseline_data.get("name", "baseline")),
                path=_resolve_path(base_dir, baseline_data["path"]),
            )
        )
        candidates = tuple(
            self.ingest_dataset(
                CsvDatasetSpec(
                    name=str(candidate.get("name", Path(candidate["path"]).stem)),
                    path=_resolve_path(base_dir, candidate["path"]),
                )
            )
            for candidate in data.get("candidates", [])
        )
        return ComparisonSuiteContract(
            suite_name=suite_name,
            baseline=baseline,
            candidates=candidates,
            key_columns=tuple(data["key_columns"]),
            excluded_columns=tuple(data.get("excluded_columns", [])),
            clear_nulls=bool(data.get("clear_nulls", True)),
            numeric_precision=data.get("numeric_precision"),
            max_detail_rows=int(data.get("max_detail_rows", 10_000)),
        )

    def _read_csv(self, path: Path) -> tuple[list[dict[str, Any]], list[str]]:
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
        with path.open("r", encoding=self._encoding, newline="") as handle:
            reader = csv.DictReader(handle, delimiter=self._delimiter)
            if reader.fieldnames is None:
                raise ValueError(f"CSV file has no header row: {path}")
            headers = [_safe_column_name(header or "column") for header in reader.fieldnames]
            if len(set(headers)) != len(headers):
                raise ValueError(f"CSV file contains duplicate column names after normalization: {path}")
            rows: list[dict[str, Any]] = []
            for raw in reader:
                row: dict[str, Any] = {}
                for original, normalized in zip(reader.fieldnames, headers, strict=True):
                    value = raw.get(original)
                    row[normalized] = None if value in self._null_tokens else value
                rows.append(row)
        return rows, headers

    def _write_table(self, table_name: str, headers: list[str], rows: list[dict[str, Any]]) -> None:
        quoted_table = _quote_identifier(table_name)
        with sqlite3.connect(self._database_path) as connection:
            if self._replace:
                connection.execute(f"DROP TABLE IF EXISTS {quoted_table}")
            column_sql = ", ".join(f"{_quote_identifier(header)} TEXT" for header in headers)
            connection.execute(f"CREATE TABLE IF NOT EXISTS {quoted_table} ({column_sql})")
            if rows:
                columns = ", ".join(_quote_identifier(header) for header in headers)
                placeholders = ", ".join("?" for _ in headers)
                connection.executemany(
                    f"INSERT INTO {quoted_table} ({columns}) VALUES ({placeholders})",
                    [tuple(row.get(header) for header in headers) for row in rows],
                )
            connection.commit()


def _resolve_path(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else base_dir / path


def _safe_column_name(value: str) -> str:
    safe = _safe_table_name(value.strip())
    if not safe:
        raise ValueError(f"Unsafe empty CSV column name: {value!r}")
    return safe


def _safe_table_name(value: str) -> str:
    safe = "".join(character if character.isalnum() else "_" for character in value.strip())
    safe = "_".join(part for part in safe.split("_") if part)
    if not safe:
        safe = "dataset"
    if safe[0].isdigit():
        safe = f"dataset_{safe}"
    return safe


def _quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'
