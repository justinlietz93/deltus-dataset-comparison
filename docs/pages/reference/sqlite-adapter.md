---
title: "SQLite Adapter"
status: current
authority: canonical
---

# SQLite Adapter

The SQLite adapter is the local database proof path for the MVP.

## Responsibilities

- list user tables from `sqlite_master`
- inspect table metadata with `PRAGMA table_info`
- validate selected keys and exclusions through the shared comparison engine
- read bounded table rows into the pure comparison engine
- produce the same result contract as the fixture and SQL Server adapters

## Why it exists

The original target remains SQL Server-style regression comparison. SQLite gives the repo a real database-backed test path that can run locally, in CI, and on GitHub without requiring a SQL Server instance.

## Fixture database

Create or refresh the local fixture database:

```bash
python scripts/create_sqlite_fixture.py --replace
```

The generated database is:

```text
tests/fixtures/mvp_cases.sqlite
```

It is built from:

```text
tests/fixtures/mvp_cases.json
```

## CLI usage

```bash
python -m comparison_evidence.adapters.driving.cli run-sqlite \
  --database tests/fixtures/mvp_cases.sqlite \
  --before identical_before \
  --after changed_after \
  --keys id \
  --export-root exports
```

## Environment usage

```bash
export SQLITE_DATABASE_PATH=tests/fixtures/mvp_cases.sqlite
export SQLITE_ROW_LIMIT=10000
```

When `SQLITE_DATABASE_PATH` is set and no SQL Server connection string is set, the API/container path uses SQLite as the dataset source.

## Current limitations

- SQLite schemas are not modeled; table names are treated as schema-less dataset references.
- The adapter reads bounded rows into the domain engine.
- High-volume pushdown comparison is deferred to later adapter-specific hardening.
