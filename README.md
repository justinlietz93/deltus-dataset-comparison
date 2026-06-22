![Deltus Comparison Tool](/assets/deltus-banner.png)

# Streamline Your Dataset Regression Testing Locally

A lightweight regression evidence generator for heterogeneous tabular data.

Deltus is the modern continuation of an earlier SQL Server + SSRS table comparison tool used for ETL regression testing. The original value is preserved: compare before/after datasets, tolerate non-identical table shapes, and produce attachable evidence.

## What the MVP does

The `0.1.x` MVP line provides:

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
- CSV pair ingestion through SQLite
- baseline-vs-candidate comparison suites
- CSV suite manifests for baseline plus N candidate datasets
- a read-only SQL Server adapter boundary

## First supported mode

The first implementation target is SQL Server table comparison. The MVP also includes local fixture and SQLite adapters so the result contract, exports, and test flow work without a live SQL Server.

Later adapters can add Parquet, DuckDB, PostgreSQL, or other sources without changing the domain model. CSV support already follows the adapter pattern by ingesting files into SQLite tables before comparison.

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


## Run a CSV comparison

Compare two CSV files by ingesting them into SQLite and reusing the normal comparison engine:

```bash
python -m comparison_evidence.adapters.driving.cli run-csv \
  --before-csv tests/fixtures/csv_suite/baseline.csv \
  --after-csv tests/fixtures/csv_suite/candidate_b.csv \
  --keys id \
  --exclude batch_id \
  --export-root exports
```

This creates the same JSON, HTML, and XLSX evidence package as the SQLite and fixture workflows.

## Run a baseline comparison suite

A suite compares one baseline dataset against multiple candidate datasets. This is useful when two or more dev scripts are intended to produce the same result and you want one evidence package that compares each candidate against the original.

```bash
python -m comparison_evidence.adapters.driving.cli run-csv-suite \
  --manifest tests/fixtures/csv_suite/manifest.json \
  --export-root exports
```

The suite output includes:

```text
exports/<suite_id>/
├─ suite_result.json
├─ suite_summary.json
├─ candidate_summaries.json
├─ suite_report.html
├─ suite_report.xlsx
└─ comparisons/
   ├─ candidate_a/
   │  ├─ result.json
   │  ├─ report.html
   │  └─ report.xlsx
   └─ candidate_b/
      ├─ result.json
      ├─ report.html
      └─ report.xlsx
```

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
