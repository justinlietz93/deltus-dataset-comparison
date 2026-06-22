---
title: "ADR-0001: Use a Hexagonal Core"
status: current
authority: canonical
---

# ADR-0001: Use a Hexagonal Core

## Status

Accepted.

## Context

The original tool was SQL Server and SSRS-centered. The modern version should preserve the comparison invariant while allowing the report surface and source adapters to change.

## Decision

Use a hexagonal architecture with a domain-owned comparison contract and adapter-owned infrastructure.

## Consequences

- SQL Server remains a first-class adapter.
- SSRS/RDL becomes legacy context, not an architectural dependency.
- CSV, Parquet, DuckDB, or other sources can be added later as adapters.
- Exports are renderers over the result contract, not custom comparison implementations.
