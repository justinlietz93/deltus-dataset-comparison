---
title: "Quickstart"
status: current
authority: canonical
---

# Quickstart

The local quickstart compares fixture datasets and exports an evidence package without requiring SQL Server. A SQLite path is also available for real local database-backed testing.

## Install for development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Run checks

```bash
./scripts/dev_check.sh
```

## Run a fixture comparison

```bash
python -m comparison_evidence.adapters.driving.cli run-fixture \
  --before dbo.identical_before \
  --after dbo.changed_after \
  --keys id \
  --export-root exports
```

## Run a SQLite comparison

Create the local SQLite fixture database:

```bash
python scripts/create_sqlite_fixture.py --replace
```

Run the comparison through SQLite:

```bash
python -m comparison_evidence.adapters.driving.cli run-sqlite \
  --database tests/fixtures/mvp_cases.sqlite \
  --before identical_before \
  --after changed_after \
  --keys id \
  --export-root exports
```

## Expected outputs

The commands print the run ID and write a folder like:

```text
exports/run_YYYYMMDD_HHMMSS_xxxxxxxx/
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

## Start the API

```bash
uvicorn comparison_evidence.adapters.driving.api.main:app --reload
```

When no SQL Server or SQLite source is configured, the API uses `tests/fixtures/mvp_cases.json` as its local source. Set `SQLITE_DATABASE_PATH=tests/fixtures/mvp_cases.sqlite` to exercise the API through SQLite.
