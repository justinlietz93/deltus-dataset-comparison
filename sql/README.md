# SQL Assets

This directory preserves the SQL Server path without letting it define the whole product.

- `legacy/`: original stored procedures, functions, and SSRS/RDL-era assets copied from the old repo.
- `migrations/`: future install/upgrade scripts for the modern SQL Server adapter.
- `fixtures/`: tiny deterministic tables for regression tests.
- `contracts/`: expected result shapes and stored procedure contracts.

The first implementation milestone is to wrap the existing comparison behavior behind a stable result contract.
