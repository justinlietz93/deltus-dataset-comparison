---
title: "Adding Source Adapters"
status: current
authority: canonical
---

# Adding Source Adapters

A source adapter connects an external dataset system to the Deltus comparison core.

## Required port

Implement `DatasetSourcePort`:

- `list_tables(source_id)`
- `inspect_schema(dataset)`
- `validate_contract(contract)`
- `compare(contract)`

## Boundary rule

The adapter translates external metadata and rows into domain objects. It must not change the result contract or define new comparison semantics.

## Minimum implementation steps

1. Add the adapter under `src/comparison_evidence/adapters/driven/<source>/`.
2. Convert source metadata into `SchemaProfile` and `ColumnProfile`.
3. Reuse `TabularComparisonEngine` for local/small comparisons or map server-side results back into `ComparisonResult`.
4. Add contract tests for the adapter behavior.
5. Add docs under `docs/pages/reference/` if the adapter has runtime assumptions.
6. Wire the adapter in `config/container.py` only after the port contract is satisfied.

## Adapter examples

- SQL Server: metadata through `INFORMATION_SCHEMA.COLUMNS`, rows through read-only table reads.
- SQLite: metadata through `PRAGMA table_info`, rows through bounded local table reads.
- Future CSV: schema inferred from file headers and optional type hints.
- Future Parquet: schema read from Parquet metadata.
- Future Postgres: metadata from `information_schema.columns`.
