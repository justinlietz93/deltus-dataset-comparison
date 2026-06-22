# Deltus: Dataset Comparison Studio

A lightweight regression evidence generator for heterogeneous tabular data.

Deltus is the modern continuation of an earlier SQL Server + SSRS table comparison tool used for ETL regression testing. The original value is preserved: compare before/after datasets, tolerate non-identical table shapes, and produce attachable evidence.

## What the MVP does

The `0.1.0` MVP provides:

- validated comparison contracts
- schema inspection through source adapters
- different-column-count support through shared-column projection
- type mismatch reporting
- duplicate-key warnings
- missing-before and missing-after row reporting
- changed-cell details
- column-level comparison stats
- JSON evidence packages
- HTML evidence reports
- XLSX evidence workbooks
- local fixture tests
- SQLite adapter and CLI proof path
- a read-only SQL Server adapter boundary

## First supported mode

The first implementation target is SQL Server table comparison. The MVP also includes local fixture and SQLite adapters so the result contract, exports, and test flow work without a live SQL Server.

Later adapters can add CSV, Parquet, DuckDB, PostgreSQL, or other sources without changing the domain model.

## Architecture

The application uses a hexagonal structure:

- `domain`: comparison rules and result contracts
- `application`: use cases and orchestration
- `ports`: interfaces between the core and the outside world
- `adapters`: API, CLI, SQL Server, SQLite, local files, export renderers
- `config`: wiring and runtime settings

The domain does not depend on SQL Server, FastAPI, report libraries, filesystems, or frontend details.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Run checks

```bash
./scripts/dev_check.sh
```

The script always runs tests and docs front-matter checks. It also runs `ruff` and `mypy` when those tools are installed.

## Run the fixture comparison CLI

```bash
python -m comparison_evidence.adapters.driving.cli run-fixture \
  --before dbo.identical_before \
  --after dbo.changed_after \
  --keys id \
  --export-root exports
```

This creates:

```text
exports/<run_id>/
├─ result.json
├─ manifest.json
├─ summary.json
├─ schema_overlap.json
├─ type_mismatches.json
├─ column_stats.json
├─ detailed_differences.json
├─ missing_before.json
├─ missing_after.json
├─ duplicate_keys.json
├─ warnings.json
├─ report.html
└─ report.xlsx
```


## Run the SQLite comparison CLI

Create or refresh the SQLite fixture database:

```bash
python scripts/create_sqlite_fixture.py --replace
```

Run the same comparison through SQLite instead of JSON fixtures:

```bash
python -m comparison_evidence.adapters.driving.cli run-sqlite \
  --database tests/fixtures/mvp_cases.sqlite \
  --before identical_before \
  --after changed_after \
  --keys id \
  --export-root exports
```

This proves the adapter path against a real SQL table source while still avoiding a live SQL Server dependency.

## Start the API

```bash
uvicorn comparison_evidence.adapters.driving.api.main:app --reload
```

Useful endpoints:

- `GET /health`
- `GET /sources/{source_id}/tables`
- `POST /schema/inspect`
- `POST /comparison/validate`
- `POST /comparison/run`
- `GET /runs/{run_id}`
- `GET /runs/{run_id}/artifacts`

## SQL Server configuration

Set a pyodbc connection string to use the SQL Server adapter:

```bash
export SQLSERVER_CONNECTION_STRING='Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=MyDb;Trusted_Connection=yes;TrustServerCertificate=yes;'
export SQLSERVER_ROW_LIMIT=10000
```

SQLite can be used as the configured source for API/local workflows:

```bash
export SQLITE_DATABASE_PATH=tests/fixtures/mvp_cases.sqlite
export SQLITE_ROW_LIMIT=10000
```

If no SQL Server or SQLite source is configured, Deltus uses `tests/fixtures/mvp_cases.json`.

## Repository map

```text
src/comparison_evidence/     Python backend and comparison core
apps/web/                    Lightweight frontend placeholder
legacy/                      Original SQL Server/SSRS assets, ignored by Git and reference-only
sql/                         SQL contracts, fixtures, and future migrations
docs/                        SGDA-style documentation system
scripts/                     Developer utilities
tests/                       Unit, contract, integration, and end-to-end tests
roadmap/                     Version-wave TODO lists
```
