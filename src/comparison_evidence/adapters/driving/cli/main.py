from __future__ import annotations

import argparse
from pathlib import Path

from comparison_evidence.adapters.driven.export import HtmlReportExporter, XlsxExporter
from comparison_evidence.adapters.driven.local_files import FixtureDatasetSource, LocalJsonResultStore
from comparison_evidence.adapters.driven.sqlite import SqliteDatasetSource
from comparison_evidence.application.use_cases.run_comparison import RunComparisonUseCase
from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
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

    args = parser.parse_args(argv)
    if args.command == "run-fixture":
        return _run_with_source(args, FixtureDatasetSource.from_json_file(args.fixture), default_schema="dbo")
    if args.command == "run-sqlite":
        return _run_with_source(
            args,
            SqliteDatasetSource(args.database, source_id=args.source_id, row_limit=args.row_limit),
            default_schema=None,
        )
    return 2


def _add_common_run_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--before", required=True, help="Before dataset as schema.table or table.")
    parser.add_argument("--after", required=True, help="After dataset as schema.table or table.")
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
        for message in exc.messages:
            print(f"validation error: {message}")
        return 1
    run_dir = Path(store.run_dir(result.run_id))
    print(f"run_id={result.run_id}")
    print(f"changed_cells={result.summary.changed_cell_count}")
    print(f"missing_before={result.summary.missing_before_count}")
    print(f"missing_after={result.summary.missing_after_count}")
    print(f"artifact_dir={run_dir}")
    print(f"html={run_dir / 'report.html'}")
    print(f"xlsx={run_dir / 'report.xlsx'}")
    return 0


def _parse_ref(source_id: str, value: str, *, default_schema: str | None) -> DatasetReference:
    if "." in value:
        schema_name, object_name = value.split(".", 1)
    else:
        schema_name, object_name = default_schema, value
    return DatasetReference(source_id=source_id, schema_name=schema_name, object_name=object_name)


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())
