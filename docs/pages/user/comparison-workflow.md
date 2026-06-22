---
title: "Comparison Workflow"
status: current
authority: canonical
---

# Comparison Workflow

A comparison run has one contract and one evidence package.

## Contract inputs

- before dataset
- after dataset
- key columns
- excluded columns
- null handling
- numeric precision
- detail row limit

## Validation rules

- At least one key column is required.
- Key columns cannot be excluded.
- Duplicate keys must be reported as a warning or failure according to run policy.
- Different column counts are allowed.
- Only common, non-excluded columns are compared as value columns.
- Columns present only on one side are reported as schema differences.

## Result sections

- summary
- schema overlap
- mismatched types
- column stats
- detailed differences
- missing before
- missing after
- warnings
