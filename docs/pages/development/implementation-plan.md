---
title: "Implementation Plan"
status: current
authority: canonical
---

# Implementation Plan

## Phase 0: Preserve legacy assets

- Copy original stored procedures into `sql/legacy`.
- Copy original RDL/report definition into `sql/legacy/ssrs`.
- Document which behavior is legacy verified and which is to be retested.

## Phase 1: Define contracts

- Finalize comparison contract schema.
- Finalize result package schema.
- Create tiny fixture datasets.

## Phase 2: Stabilize SQL Server path

- Add schema-aware table references.
- Validate table and column names.
- Standardize identifier quoting.
- Add duplicate-key policy.
- Produce result contract outputs.

## Phase 3: Backend wrapper

- Add API endpoints for inspect, run, load, and export.
- Store run metadata.
- Save evidence packages.

## Phase 4: Report reader

- Build report pages from result contract.
- Add XLSX and HTML export.
- Add PDF export after HTML stabilizes.
