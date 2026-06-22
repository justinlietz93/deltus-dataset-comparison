# TODO: Deltus MVP `0.1.0`

## Purpose

Build the smallest useful version of Deltus: a local-first dataset comparison evidence generator that can compare two SQL Server tables through a validated comparison contract and produce reviewable evidence artifacts.

The MVP is not a universal data platform. It is the first modern replacement for the old SSRS workflow.

## MVP boundary

Included:

- SQL Server table comparison path.
- Schema inspection.
- Key-column and exclusion contract.
- Different-column-count support through shared-column projection.
- Type mismatch reporting.
- Missing-row reporting.
- Changed-row reporting.
- Column-level statistics.
- JSON result package.
- Basic HTML report.
- Basic XLSX export.
- Fixture-driven tests.

Excluded until later waves:

- CSV/Parquet adapters.
- PostgreSQL/MySQL adapters.
- Multi-user auth.
- Job queues/background workers.
- Full frontend polish.
- PDF parity with the old SSRS report.
- Cloud deployment packaging.

## Definition of Done

- [ ] A developer can define two SQL Server table references, key columns, and excluded columns.
- [ ] The system validates the comparison contract before running expensive work.
- [ ] The comparison handles different column counts without failure.
- [ ] Duplicate keys are detected and surfaced as a hard warning.
- [ ] The result package includes summary, schema overlap, type mismatches, column stats, detailed differences, missing-before rows, missing-after rows, and manifest metadata.
- [ ] The basic HTML report and XLSX export can be attached to a ticket as evidence.
- [ ] Unit and contract tests pass from a clean checkout.
- [ ] Legacy SQL/SSRS assets remain preserved but are not the active report surface.

---

## Phase 0: Baseline the repo

### Task 0.1: Freeze the legacy boundary

- [ ] Step 0.1.1: Confirm the legacy folder is ignored or explicitly marked historical.
- [ ] Step 0.1.2: Add a short inventory of legacy assets and what each file was used for.
- [ ] Step 0.1.3: Mark the old SSRS/RDL path as reference-only.
- [ ] Step 0.1.4: Identify which legacy stored procedures are still candidates for active reuse.

### Task 0.2: Confirm architecture boundaries

- [ ] Step 0.2.1: Verify domain models do not import SQL Server, FastAPI, filesystem, or export libraries.
- [ ] Step 0.2.2: Verify application use cases depend only on domain models and ports.
- [ ] Step 0.2.3: Verify SQL Server work is isolated to driven adapters or SQL assets.
- [ ] Step 0.2.4: Verify report/export work is isolated to export adapters.

### Task 0.3: Establish developer commands

- [ ] Step 0.3.1: Confirm `pytest` runs successfully from repo root.
- [ ] Step 0.3.2: Add or update `scripts/dev_check.sh` to run formatting, linting, typing, and tests.
- [ ] Step 0.3.3: Add a README section with the exact MVP development commands.
- [ ] Step 0.3.4: Make failed checks obvious and local-first.

---

## Phase 1: Define the comparison contract

### Task 1.1: Finalize input contract

- [ ] Step 1.1.1: Define `DatasetReference` fields for SQL Server sources.
- [ ] Step 1.1.2: Define explicit schema/table naming rules.
- [ ] Step 1.1.3: Define key-column selection rules.
- [ ] Step 1.1.4: Define excluded-column rules.
- [ ] Step 1.1.5: Define null-handling and numeric-precision options.
- [ ] Step 1.1.6: Define maximum detailed-difference row limits.

### Task 1.2: Finalize schema projection rules

- [ ] Step 1.2.1: Common columns are the comparable projection.
- [ ] Step 1.2.2: Before-only columns are reported, not compared.
- [ ] Step 1.2.3: After-only columns are reported, not compared.
- [ ] Step 1.2.4: Excluded columns are removed from comparison stats.
- [ ] Step 1.2.5: Key columns are validated before exclusions are applied.
- [ ] Step 1.2.6: Mismatched data types are reported separately from value differences.

### Task 1.3: Finalize output contract

- [ ] Step 1.3.1: Define `ComparisonResult` summary fields.
- [ ] Step 1.3.2: Define schema-overlap section.
- [ ] Step 1.3.3: Define type-mismatch section.
- [ ] Step 1.3.4: Define column-stat section.
- [ ] Step 1.3.5: Define detailed-difference section.
- [ ] Step 1.3.6: Define missing-before and missing-after sections.
- [ ] Step 1.3.7: Define warning and failure sections.
- [ ] Step 1.3.8: Define evidence manifest fields.

---

## Phase 2: Build fixture-driven test coverage

### Task 2.1: Create tiny fixture datasets

- [ ] Step 2.1.1: Fixture A: identical tables, no differences.
- [ ] Step 2.1.2: Fixture B: one changed value.
- [ ] Step 2.1.3: Fixture C: different column counts.
- [ ] Step 2.1.4: Fixture D: excluded column changed but ignored.
- [ ] Step 2.1.5: Fixture E: missing row in before table.
- [ ] Step 2.1.6: Fixture F: missing row in after table.
- [ ] Step 2.1.7: Fixture G: mismatched column type.
- [ ] Step 2.1.8: Fixture H: duplicate key on one side.
- [ ] Step 2.1.9: Fixture I: null-versus-empty-string behavior.
- [ ] Step 2.1.10: Fixture J: numeric precision/rounding behavior.

### Task 2.2: Write expected outputs

- [ ] Step 2.2.1: Add expected summary JSON for each fixture.
- [ ] Step 2.2.2: Add expected schema-overlap JSON for each fixture.
- [ ] Step 2.2.3: Add expected column-stats JSON for changed-value fixtures.
- [ ] Step 2.2.4: Add expected missing-row JSON for missing-row fixtures.
- [ ] Step 2.2.5: Add expected warning JSON for duplicate-key fixtures.

### Task 2.3: Add contract tests

- [ ] Step 2.3.1: Test schema projection with different column counts.
- [ ] Step 2.3.2: Test key validation.
- [ ] Step 2.3.3: Test exclusion validation.
- [ ] Step 2.3.4: Test duplicate-key warning behavior.
- [ ] Step 2.3.5: Test result package schema validity.

---

## Phase 3: Stabilize SQL Server adapter path

### Task 3.1: Implement schema inspection

- [ ] Step 3.1.1: Add SQL Server adapter method for available tables.
- [ ] Step 3.1.2: Add SQL Server adapter method for table columns.
- [ ] Step 3.1.3: Include column names, ordinal position, data type, nullability, precision, and scale.
- [ ] Step 3.1.4: Add tests or documented manual verification against fixture tables.

### Task 3.2: Implement contract validation

- [ ] Step 3.2.1: Validate source and target tables exist.
- [ ] Step 3.2.2: Validate selected key columns exist on both sides.
- [ ] Step 3.2.3: Validate excluded columns exist on at least one side.
- [ ] Step 3.2.4: Reject unsafe identifier strings.
- [ ] Step 3.2.5: Return actionable validation messages.

### Task 3.3: Implement comparison execution

- [ ] Step 3.3.1: Produce row counts.
- [ ] Step 3.3.2: Produce duplicate-key counts.
- [ ] Step 3.3.3: Produce schema overlap.
- [ ] Step 3.3.4: Produce type mismatches.
- [ ] Step 3.3.5: Produce missing-before rows.
- [ ] Step 3.3.6: Produce missing-after rows.
- [ ] Step 3.3.7: Produce changed-row details.
- [ ] Step 3.3.8: Produce column-level difference counts.

### Task 3.4: Harden SQL identifier handling

- [ ] Step 3.4.1: Use parameterization for values.
- [ ] Step 3.4.2: Use safe quoting for identifiers.
- [ ] Step 3.4.3: Never concatenate unvalidated schema, table, or column names.
- [ ] Step 3.4.4: Add tests or review notes for unsafe identifier rejection.

---

## Phase 4: Build the application workflow

### Task 4.1: Implement the primary use case

- [ ] Step 4.1.1: Implement `RunComparisonUseCase` orchestration.
- [ ] Step 4.1.2: Load schema profiles through the dataset source port.
- [ ] Step 4.1.3: Validate the comparison contract.
- [ ] Step 4.1.4: Run comparison through the dataset source port.
- [ ] Step 4.1.5: Store the result package through the result store port.
- [ ] Step 4.1.6: Return run ID and summary.

### Task 4.2: Implement run persistence

- [ ] Step 4.2.1: Store run metadata locally.
- [ ] Step 4.2.2: Store result sections as JSON.
- [ ] Step 4.2.3: Store generated artifacts under a run directory.
- [ ] Step 4.2.4: Add a load-run use case.
- [ ] Step 4.2.5: Add deterministic run folder naming.

### Task 4.3: Implement minimal API surface

- [ ] Step 4.3.1: Endpoint: health check.
- [ ] Step 4.3.2: Endpoint: inspect source schema.
- [ ] Step 4.3.3: Endpoint: validate comparison contract.
- [ ] Step 4.3.4: Endpoint: run comparison.
- [ ] Step 4.3.5: Endpoint: load run result.
- [ ] Step 4.3.6: Endpoint: export run artifact.

---

## Phase 5: Produce evidence artifacts

### Task 5.1: JSON result package

- [ ] Step 5.1.1: Write `manifest.json`.
- [ ] Step 5.1.2: Write `summary.json`.
- [ ] Step 5.1.3: Write `schema_overlap.json`.
- [ ] Step 5.1.4: Write `type_mismatches.json`.
- [ ] Step 5.1.5: Write `column_stats.json`.
- [ ] Step 5.1.6: Write `detailed_differences.json`.
- [ ] Step 5.1.7: Write `missing_before.json`.
- [ ] Step 5.1.8: Write `missing_after.json`.

### Task 5.2: Basic HTML report

- [ ] Step 5.2.1: Render run metadata.
- [ ] Step 5.2.2: Render summary cards.
- [ ] Step 5.2.3: Render schema overlap.
- [ ] Step 5.2.4: Render type mismatches.
- [ ] Step 5.2.5: Render column stats.
- [ ] Step 5.2.6: Render detailed differences.
- [ ] Step 5.2.7: Render missing rows.
- [ ] Step 5.2.8: Render warnings clearly.

### Task 5.3: Basic XLSX export

- [ ] Step 5.3.1: Sheet: Summary.
- [ ] Step 5.3.2: Sheet: Schema Overlap.
- [ ] Step 5.3.3: Sheet: Type Mismatches.
- [ ] Step 5.3.4: Sheet: Column Stats.
- [ ] Step 5.3.5: Sheet: Detailed Differences.
- [ ] Step 5.3.6: Sheet: Missing Before.
- [ ] Step 5.3.7: Sheet: Missing After.
- [ ] Step 5.3.8: Sheet: Manifest.

---

## Phase 6: Document and verify the MVP

### Task 6.1: Write user docs

- [ ] Step 6.1.1: Document the comparison workflow.
- [ ] Step 6.1.2: Document key selection.
- [ ] Step 6.1.3: Document excluded columns.
- [ ] Step 6.1.4: Document different-column-count behavior.
- [ ] Step 6.1.5: Document duplicate-key behavior.
- [ ] Step 6.1.6: Document export artifacts.

### Task 6.2: Write developer docs

- [ ] Step 6.2.1: Document hexagonal boundaries.
- [ ] Step 6.2.2: Document ports and adapters.
- [ ] Step 6.2.3: Document SQL Server adapter assumptions.
- [ ] Step 6.2.4: Document fixture test strategy.
- [ ] Step 6.2.5: Document how to add a future source adapter.

### Task 6.3: Release `0.1.0`

- [ ] Step 6.3.1: Run full local checks.
- [ ] Step 6.3.2: Update README current status.
- [ ] Step 6.3.3: Update changelog or release notes.
- [ ] Step 6.3.4: Tag `v0.1.0`.
- [ ] Step 6.3.5: Archive sample evidence package generated from fixtures.
