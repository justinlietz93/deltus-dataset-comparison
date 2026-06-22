# Deltus: Dataset Comparison Studio

A lightweight regression evidence generator for heterogeneous tabular data.

This project is the modern continuation of an earlier SQL Server + SSRS table comparison tool used for ETL regression testing. The goal is to preserve the original value while replacing the SSRS report surface with a small backend, report reader, and export pipeline.

## Core idea

Given two datasets, possibly with different schemas, produce ticket-ready comparison evidence:

- schema overlap
- selected key columns
- excluded columns
- type mismatches
- row counts
- missing rows
- changed rows
- column-level difference counts
- exportable HTML, PDF, XLSX, CSV, and JSON artifacts

## First supported mode

The first implementation target is SQL Server table comparison, because that preserves the original tool's strongest use case.

Later adapters can add CSV, Parquet, DuckDB, PostgreSQL, or other sources without changing the domain model.

## Architecture

The application uses a hexagonal structure:

- `domain`: comparison rules and result contracts
- `application`: use cases and orchestration
- `ports`: interfaces between the core and the outside world
- `adapters`: API, CLI, SQL Server, local files, export renderers
- `config`: wiring and runtime settings

The domain must not depend on SQL Server, FastAPI, React, report libraries, or filesystem details.

## Main workflow

1. Register or select source A and source B.
2. Inspect schemas.
3. Select key columns.
4. Select excluded columns.
5. Validate the comparison contract.
6. Run the comparison.
7. Persist a comparison run.
8. Render the evidence report.
9. Export HTML, XLSX, PDF, JSON, and CSV evidence.

## Current status

Scaffold only. The first build milestone is a tested SQL Server comparison contract with fixture tables.

## Repository map

```text
src/comparison_evidence/     Python backend and comparison core
apps/web/                    Lightweight frontend report reader
sql/legacy/                  Original SQL Server assets, kept as historical source material
sql/migrations/              Future install/upgrade scripts
docs/                        SGDA-style documentation system
scripts/                     Developer utilities
tests/                       Unit, contract, integration, and end-to-end tests
```
