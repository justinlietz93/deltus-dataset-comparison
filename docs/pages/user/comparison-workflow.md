---
title: "Comparison Workflow"
status: current
authority: canonical
---

# Comparison Workflow

A comparison run has one contract and one evidence package.

## Contract inputs

- before dataset reference
- after dataset reference
- key columns
- excluded columns
- null handling
- numeric precision
- maximum detailed row count

## Validation rules

- At least one key column is required.
- Key columns must exist on both sides.
- Key columns cannot be excluded.
- Excluded columns must exist on at least one side.
- Dataset, schema, table, and column identifiers must use safe names: letters, numbers, and underscores only, starting with a letter or underscore.
- Different column counts are allowed.
- Only shared, non-excluded, non-key, type-compatible columns are value-compared.
- Columns present only on one side are reported as schema overlap differences.
- Type mismatches are reported separately and are not value-compared in the MVP.
- Duplicate keys create a hard warning because one-to-one row alignment is no longer guaranteed.

## Result sections

- manifest
- summary
- schema overlap
- type mismatches
- column stats
- detailed differences
- missing before
- missing after
- duplicate keys
- warnings
- failures

## Local fixture run

The default local app uses `tests/fixtures/mvp_cases.json` when no SQL Server connection string is configured. This lets a developer verify the result contract and report exports without a database server.
