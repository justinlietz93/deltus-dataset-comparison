from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    export_root: str
    sqlserver_connection_string: str | None
    sqlite_database_path: str | None
    fixture_source_path: str | None
    sqlserver_row_limit: int | None
    sqlite_row_limit: int | None


def load_settings() -> Settings:
    sqlserver_row_limit_raw = os.getenv("SQLSERVER_ROW_LIMIT")
    sqlite_row_limit_raw = os.getenv("SQLITE_ROW_LIMIT")
    return Settings(
        app_env=os.getenv("APP_ENV", "local"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./runs/comparison_evidence.db"),
        export_root=os.getenv("EXPORT_ROOT", "./exports"),
        sqlserver_connection_string=(
            os.getenv("SQLSERVER_CONNECTION_STRING")
            or os.getenv("SQLSERVER_DSN")
            or None
        ),
        sqlite_database_path=os.getenv("SQLITE_DATABASE_PATH") or None,
        fixture_source_path=os.getenv("FIXTURE_SOURCE_PATH") or _default_fixture_path(),
        sqlserver_row_limit=int(sqlserver_row_limit_raw) if sqlserver_row_limit_raw else None,
        sqlite_row_limit=int(sqlite_row_limit_raw) if sqlite_row_limit_raw else None,
    )


def _default_fixture_path() -> str | None:
    path = Path("tests/fixtures/mvp_cases.json")
    return str(path) if path.exists() else None
