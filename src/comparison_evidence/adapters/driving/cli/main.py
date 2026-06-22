from __future__ import annotations

import argparse
from pathlib import Path

from comparison_evidence.adapters.driven.csv import CsvToSqliteIngestAdapter
from comparison_evidence.adapters.driven.export import (
    HtmlReportExporter,
    HtmlSuiteReportExporter,
    XlsxExporter,
    XlsxSuiteExporter,
)
from comparison_evidence.adapters.driven.local_files import (
    FixtureDatasetSource,
    LocalJsonResultStore,
    LocalJsonSuiteResultStore,
)
from comparison_evidence.adapters.driven.sqlite import SqliteDatasetSource
from comparison_evidence.application.use_cases.run_comparison import RunComparisonUseCase
from comparison_evidence.application.use_cases.run_comparison_suite import RunComparisonSuiteUseCase
from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_suite_contract import ComparisonSuiteContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.ports.driven.dataset_source_port import DatasetSourcePort


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="deltus", description="Run Deltus comparison evidence workflows.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    fixture = subcommands.add_parser("run-fixture", help="Run a local fixture-backed comparison.")
    fixture.add_argument("--fixture", default="tests/fixtures/mvp_cases.json")
    fixture.add_argument("--source-id", default="fixture")
    _add_common_run_args(fixture)

    sqlite = subcommands.add_parser("run-sqlite", help="Run a SQLite-backed comparison.")
    sqlite.add_argument("--database", required=True, help="Path to a SQLite database file.")
    sqlite.add_argument("--source-id", default="sqlite")
    sqlite.add_argument("--row-limit", type=int)
    _add_common_run_args(sqlite)

    csv_pair = subcommands.add_parser("run-csv", help="Ingest two CSV files into SQLite and compare them.")
    csv_pair.add_argument("--before-csv", required=True, help="Path to the baseline/before CSV file.")
    csv_pair.add_argument("--after-csv", required=True, help="Path to the candidate/after CSV file.")
    csv_pair.add_argument("--before-name", default="before")
    csv_pair.add_argument("--after-name", default="after")
    csv_pair.add_argument("--database", help="Optional SQLite database path for ingested CSV tables.")
    csv_pair.add_argument("--delimiter", default=",")
    csv_pair.add_argument("--encoding", default="utf-8")
    csv_pair.add_argument("--source-id", default="csv_sqlite")
    _add_common_option_args(csv_pair)

    sqlite_suite = subcommands.add_parser("run-suite-sqlite", help="Run a baseline-vs-candidates suite from SQLite tables.")
    sqlite_suite.add_argument("--database", required=True, help="Path to a SQLite database file.")
    sqlite_suite.add_argument("--suite-name", required=True)
    sqlite_suite.add_argument("--baseline", required=True, help="Baseline table name.")
    sqlite_suite.add_argument("--candidates", required=True, help="Comma-separated candidate table names.")
    sqlite_suite.add_argument("--source-id", default="sqlite")
    sqlite_suite.add_argument("--row-limit", type=int)
    _add_common_option_args(sqlite_suite)

    csv_suite = subcommands.add_parser("run-csv-suite", help="Run a baseline-vs-candidates suite from a CSV manifest.")
    csv_suite.add_argument("--manifest", required=True, help="Path to a CSV suite manifest JSON file.")
    csv_suite.add_argument("--database", help="Optional SQLite database path for ingested CSV tables.")
    csv_suite.add_argument("--source-id", default="csv_sqlite")
    csv_suite.add_argument("--export-root", default="exports")

    args = parser.parse_args(argv)
    if args.command == "run-fixture":
        return _run_with_source(args, FixtureDatasetSource.from_json_file(args.fixture), default_schema="dbo")
    if args.command == "run-sqlite":
        return _run_with_source(
            args,
            SqliteDatasetSource(args.database, source_id=args.source_id, row_limit=args.row_limit),
            default_schema=None,
        )
    if args.command == "run-csv":
        return _run_csv_pair(args)
    if args.command == "run-suite-sqlite":
        return _run_sqlite_suite(args)
    if args.command == "run-csv-suite":
        return _run_csv_suite(args)
    return 2


def _add_common_run_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--before", required=True, help="Before dataset as schema.table or table.")
    parser.add_argument("--after", required=True, help="After dataset as schema.table or table.")
    _add_common_option_args(parser)


def _add_common_option_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--keys", required=True, help="Comma-separated key columns.")
    parser.add_argument("--exclude", default="", help="Comma-separated excluded columns.")
    parser.add_argument("--export-root", default="exports")
    parser.add_argument("--strict-nulls", action="store_true")
    parser.add_argument("--numeric-precision", type=int)
    parser.add_argument("--max-detail-rows", type=int, default=10_000)


def _run_with_source(args: argparse.Namespace, source: DatasetSourcePort, *, default_schema: str | None) -> int:
    store = LocalJsonResultStore(args.export_root)
    use_case = RunComparisonUseCase(
        source=source,
        store=store,
        exporters=(HtmlReportExporter(), XlsxExporter()),
    )
    contract = ComparisonContract(
        before=_parse_ref(args.source_id, args.before, default_schema=default_schema),
        after=_parse_ref(args.source_id, args.after, default_schema=default_schema),
        key_columns=_split_csv(args.keys),
        excluded_columns=_split_csv(args.exclude),
        clear_nulls=not args.strict_nulls,
        numeric_precision=args.numeric_precision,
        max_detail_rows=args.max_detail_rows,
    )
    try:
        result = use_case.run_comparison(contract)
    except ContractValidationError as exc:
        _print_validation_errors(exc.messages)
        return 1
    _print_comparison_result(store, result)
    return 0


def _run_csv_pair(args: argparse.Namespace) -> int:
    database = args.database or str(Path(args.export_root) / "csv_ingest.sqlite")
    ingester = CsvToSqliteIngestAdapter(
        database,
        source_id=args.source_id,
        delimiter=args.delimiter,
        encoding=args.encoding,
    )
    contract = ingester.ingest_pair(
        args.before_csv,
        args.after_csv,
        before_name=args.before_name,
        after_name=args.after_name,
        key_columns=_split_csv(args.keys),
        excluded_columns=_split_csv(args.exclude),
        clear_nulls=not args.strict_nulls,
        numeric_precision=args.numeric_precision,
        max_detail_rows=args.max_detail_rows,
    )
    source = ingester.sqlite_source()
    temp_args = argparse.Namespace(export_root=args.export_root)
    store = LocalJsonResultStore(args.export_root)
    use_case = RunComparisonUseCase(source=source, store=store, exporters=(HtmlReportExporter(), XlsxExporter()))
    try:
        result = use_case.run_comparison(contract)
    except ContractValidationError as exc:
        _print_validation_errors(exc.messages)
        return 1
    _print_comparison_result(store, result)
    print(f"sqlite_ingest_database={database}")
    return 0


def _run_sqlite_suite(args: argparse.Namespace) -> int:
    source = SqliteDatasetSource(args.database, source_id=args.source_id, row_limit=args.row_limit)
    suite = ComparisonSuiteContract(
        suite_name=args.suite_name,
        baseline=_parse_ref(args.source_id, args.baseline, default_schema=None),
        candidates=tuple(_parse_ref(args.source_id, item, default_schema=None) for item in _split_csv(args.candidates)),
        key_columns=_split_csv(args.keys),
        excluded_columns=_split_csv(args.exclude),
        clear_nulls=not args.strict_nulls,
        numeric_precision=args.numeric_precision,
        max_detail_rows=args.max_detail_rows,
    )
    return _run_suite_with_source(args.export_root, source, suite)


def _run_csv_suite(args: argparse.Namespace) -> int:
    database = args.database or str(Path(args.export_root) / "csv_suite_ingest.sqlite")
    ingester = CsvToSqliteIngestAdapter(database, source_id=args.source_id)
    suite = ingester.ingest_suite_manifest(args.manifest)
    result_code = _run_suite_with_source(args.export_root, ingester.sqlite_source(), suite)
    if result_code == 0:
        print(f"sqlite_ingest_database={database}")
    return result_code


def _run_suite_with_source(export_root: str, source: DatasetSourcePort, suite: ComparisonSuiteContract) -> int:
    store = LocalJsonSuiteResultStore(export_root)
    use_case = RunComparisonSuiteUseCase(source=source)
    try:
        suite_result = use_case.run_suite(suite)
    except ContractValidationError as exc:
        _print_validation_errors(exc.messages)
        return 1
    store.save(suite_result)
    suite_dir = Path(store.suite_dir(suite_result.suite_id))
    HtmlSuiteReportExporter().export(suite_result, str(suite_dir))
    XlsxSuiteExporter().export(suite_result, str(suite_dir))
    print(f"suite_id={suite_result.suite_id}")
    print(f"candidates={suite_result.summary.candidate_count}")
    print(f"pass={suite_result.summary.pass_count}")
    print(f"warn={suite_result.summary.warn_count}")
    print(f"fail={suite_result.summary.fail_count}")
    print(f"best_candidate={suite_result.summary.best_candidate_label or ''}")
    print(f"artifact_dir={suite_dir}")
    print(f"html={suite_dir / 'suite_report.html'}")
    print(f"xlsx={suite_dir / 'suite_report.xlsx'}")
    return 0


def _parse_ref(source_id: str, value: str, *, default_schema: str | None) -> DatasetReference:
    if "." in value:
        schema_name, object_name = value.split(".", 1)
    else:
        schema_name, object_name = default_schema, value
    return DatasetReference(source_id=source_id, schema_name=schema_name, object_name=object_name)


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


def _print_validation_errors(messages: tuple[str, ...] | list[str]) -> None:
    for message in messages:
        print(f"validation error: {message}")


def _print_comparison_result(store: LocalJsonResultStore, result) -> None:
    run_dir = Path(store.run_dir(result.run_id))
    print(f"run_id={result.run_id}")
    print(f"changed_cells={result.summary.changed_cell_count}")
    print(f"missing_before={result.summary.missing_before_count}")
    print(f"missing_after={result.summary.missing_after_count}")
    print(f"artifact_dir={run_dir}")
    print(f"html={run_dir / 'report.html'}")
    print(f"xlsx={run_dir / 'report.xlsx'}")
