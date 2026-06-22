from __future__ import annotations

from typing import Any

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import ComparisonResult
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.domain.models.schema_profile import ColumnProfile, SchemaProfile
from comparison_evidence.domain.services.comparison_engine import TabularComparisonEngine
from comparison_evidence.shared.identifiers import qualified_sqlserver_name, quote_sqlserver_identifier

Row = dict[str, Any]


class SqlServerDatasetSource:
    """Read-only SQL Server adapter for the MVP comparison path.

    The adapter keeps SQL Server and pyodbc concerns outside the domain. The MVP
    implementation reads bounded table data into the pure comparison engine. Later
    waves can replace this with server-side stored procedure execution for very
    large tables while preserving the same result contract.
    """

    def __init__(self, connection_string: str, *, row_limit: int | None = None):
        self._connection_string = connection_string
        self._row_limit = row_limit
        self._engine = TabularComparisonEngine()

    def list_tables(self, source_id: str) -> tuple[DatasetReference, ...]:
        rows = self._query(
            """
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
            """
        )
        return tuple(
            DatasetReference(
                source_id=source_id,
                schema_name=row["TABLE_SCHEMA"],
                object_name=row["TABLE_NAME"],
            )
            for row in rows
        )

    def inspect_schema(self, dataset: DatasetReference) -> SchemaProfile:
        rows = self._query(
            """
            SELECT
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                ORDINAL_POSITION,
                NUMERIC_PRECISION,
                NUMERIC_SCALE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """,
            dataset.schema_name or "dbo",
            dataset.object_name,
        )
        if not rows:
            raise ValueError(f"SQL Server table not found or has no columns: {dataset.qualified_name()}")
        return SchemaProfile(
            dataset_label=dataset.label(),
            columns=tuple(
                ColumnProfile(
                    name=row["COLUMN_NAME"],
                    data_type=row["DATA_TYPE"],
                    nullable=row["IS_NULLABLE"] == "YES",
                    ordinal=int(row["ORDINAL_POSITION"]),
                    precision=row.get("NUMERIC_PRECISION"),
                    scale=row.get("NUMERIC_SCALE"),
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
        table_name = qualified_sqlserver_name(dataset.schema_name or "dbo", dataset.object_name)
        top_clause = f"TOP ({int(self._row_limit)}) " if self._row_limit else ""
        return self._query(f"SELECT {top_clause}* FROM {table_name}")

    def _query(self, sql: str, *params: object) -> list[Row]:
        try:
            import pyodbc  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError(
                "pyodbc is required for SQL Server access. Install the project with SQL Server "
                "dependencies and configure SQLSERVER_DSN or SQLSERVER_CONNECTION_STRING."
            ) from exc

        with pyodbc.connect(self._connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


__all__ = ["SqlServerDatasetSource", "quote_sqlserver_identifier", "qualified_sqlserver_name"]
