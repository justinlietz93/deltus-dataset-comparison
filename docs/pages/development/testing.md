---
title: "Testing"
status: current
authority: canonical
---

# Testing

## Test layers

- Unit tests for domain projection and comparison rules.
- Application tests for run orchestration, persistence, and exports.
- Contract tests for result package shape.
- Adapter tests for fixture dataset inspection.
- Adapter tests for SQLite schema inspection and comparison behavior.
- SQLite e2e CLI tests for evidence export.
- Future SQL Server integration tests against real fixture tables.

## Current fixture cases

The MVP fixture file is `tests/fixtures/mvp_cases.json`. The SQLite fixture database is generated from the same file at `tests/fixtures/mvp_cases.sqlite`.

Covered cases:

1. identical tables
2. one changed value
3. different column counts
4. excluded column ignored
5. missing before row
6. missing after row
7. mismatched data type
8. duplicate key warning
9. null versus empty string behavior
10. numeric precision behavior

Expected summary fragments live in `tests/fixtures/expected_summaries.json`.

## SQLite fixture refresh

Run:

```bash
python scripts/create_sqlite_fixture.py --replace
```

## Local check

Run:

```bash
./scripts/dev_check.sh
```

The script always runs tests and docs front-matter checks. If `ruff` or `mypy` are installed, it also runs formatting, linting, and typing checks.
