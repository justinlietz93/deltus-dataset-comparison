from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import ColumnProfile, SchemaProfile
from comparison_evidence.domain.services.comparison_engine import TabularComparisonEngine
from comparison_evidence.shared.identifiers import validate_safe_identifier

Row = dict[str, Any]


class SqliteDatasetSource:
    def __init__(
        self,
        database_path: str | Path,
        *,
        source_id: str = "sqlite",
        row_limit: int | None = None,
    ):
        self._database_path = str(database_path)
        self._source_id = source_id
        self._row_limit = row_limit
        self._engine = TabularComparisonEngine()

    @property
    def database_path(self) -> str:
        return self._database_path

    def list_tables(self, source_id: str | None = None) -> tuple[DatasetReference, ...]:
        resolved_source_id = source_id or self._source_id
        rows = self._query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        return tuple(
            DatasetReference(
                source_id=resolved_source_id,
                schema_name=None,
                object_name=row["name"],
            )
            for row in rows
        )

    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile:
        table_name = _quote_sqlite_identifier(dataset.object_name)
        rows = self._query(f"PRAGMA table_info({table_name})")
        if not rows:
            raise ValueError(f"SQLite table not found or has no columns: {dataset.qualified_name()}")
        return SchemaProfile(
            dataset_label=dataset.label(),
            columns=tuple(
                ColumnProfile(
                    name=row["name"],
                    data_type=row["type"] or "text",
                    nullable=not bool(row["notnull"]),
                    ordinal=int(row["cid"]),
                )
                for row in rows
            ),
        )

    def validate_contract(self, contract: ComparisonContract) -> tuple[str, ...]:
        before_schema = self.inspect_schema(contract.before)
        after_schema = self.inspect_schema(contract.after)
        return self._engine.validate_contract(contract, before_schema, after_schema)

    def compare(self, contract: ComparisonContract) -> ComparisonResult:
        before_schema = self.inspect_schema(contract.before)
        after_schema = self.inspect_schema(contract.after)
        self._engine.require_valid_contract(contract, before_schema, after_schema)
        before_rows = self._select_rows(contract.before)
        after_rows = self._select_rows(contract.after)
        return self._engine.compare(contract, before_schema, after_schema, before_rows, after_rows)

    def _select_rows(self, dataset: DatasetReference) -> list[Row]:
        table_name = _quote_sqlite_identifier(dataset.object_name)
        limit_clause = "" if self._row_limit is None else " LIMIT ?"
        params: tuple[object, ...] = () if self._row_limit is None else (int(self._row_limit),)
        return self._query(f"SELECT * FROM {table_name}{limit_clause}", *params)

    def _query(self, sql: str, *params: object) -> list[Row]:
        with sqlite3.connect(self._database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]


def _quote_sqlite_identifier(value: str) -> str:
    validate_safe_identifier(value, label="sqlite_identifier")
    return f'"{value}"'


__all__ = ["SqliteDatasetSource"]
