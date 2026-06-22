from __future__ import annotations

from comparison_evidence.adapters.driven.export import HtmlReportExporter, XlsxExporter
from comparison_evidence.adapters.driven.local_files import FixtureDatasetSource, LocalJsonResultStore
from comparison_evidence.adapters.driven.sqlite import SqliteDatasetSource
from comparison_evidence.adapters.driven.sqlserver import SqlServerDatasetSource
from comparison_evidence.application.use_cases.run_comparison import RunComparisonUseCase
from comparison_evidence.config.settings import Settings, load_settings
from comparison_evidence.ports.driven.dataset_source_port import DatasetSourcePort


def build_dataset_source(settings: Settings) -> DatasetSourcePort:
    if settings.sqlserver_connection_string:
        return SqlServerDatasetSource(
            settings.sqlserver_connection_string,
            row_limit=settings.sqlserver_row_limit,
        )
    if settings.sqlite_database_path:
        return SqliteDatasetSource(
            settings.sqlite_database_path,
            row_limit=settings.sqlite_row_limit,
        )
    if settings.fixture_source_path:
        return FixtureDatasetSource.from_json_file(settings.fixture_source_path)
    raise RuntimeError(
        "No dataset source configured. Set SQLSERVER_CONNECTION_STRING, SQLITE_DATABASE_PATH, or FIXTURE_SOURCE_PATH."
    )


def build_run_comparison_use_case(settings: Settings | None = None) -> RunComparisonUseCase:
    resolved = settings or load_settings()
    return RunComparisonUseCase(
        source=build_dataset_source(resolved),
        store=LocalJsonResultStore(resolved.export_root),
        exporters=(HtmlReportExporter(), XlsxExporter()),
    )
