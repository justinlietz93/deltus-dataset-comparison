---
title: "SQL Server Adapter"
status: current
authority: canonical
---

# SQL Server Adapter

The SQL Server adapter is the first source adapter.

## Responsibilities

- list available base tables
- inspect table metadata from `INFORMATION_SCHEMA.COLUMNS`
- validate selected keys and exclusions through the shared comparison engine
- read table rows through a read-only adapter path
- translate SQL Server rows and metadata into the domain result contract

## MVP behavior

The MVP adapter can read bounded SQL Server table rows into the pure comparison engine. This is enough for a small starting point and fixture-style verification, but it is not the final high-volume execution model.

Set:

```text
SQLSERVER_CONNECTION_STRING=<pyodbc connection string>
SQLSERVER_ROW_LIMIT=<optional integer>
```

If no SQL Server connection string is configured, the local fixture adapter is used.

## Non-responsibilities

- rendering reports
- choosing UI layout
- defining domain terms
- owning the result contract
- reintroducing SSRS/RDL generation

## Later hardening

The `0.2.x` wave should move expensive comparisons server-side or snapshot-side while preserving the current result contract.
