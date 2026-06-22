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

- [x] A developer can define two SQL Server table references, key columns, and excluded columns.
- [x] The system validates the comparison contract before running expensive work.
- [x] The comparison handles different column counts without failure.
- [x] Duplicate keys are detected and surfaced as a hard warning.
- [x] The result package includes summary, schema overlap, type mismatches, column stats, detailed differences, missing-before rows, missing-after rows, and manifest metadata.
- [x] The basic HTML report and XLSX export can be attached to a ticket as evidence.
- [x] Unit and contract tests pass from a clean checkout.
- [x] Legacy SQL/SSRS assets remain preserved but are not the active report surface.

---

## Phase 0: Baseline the repo

### Task 0.1: Freeze the legacy boundary

- [x] Step 0.1.1: Confirm the legacy folder is ignored or explicitly marked historical.
- [x] Step 0.1.2: Add a short inventory of legacy assets and what each file was used for.
- [x] Step 0.1.3: Mark the old SSRS/RDL path as reference-only.
- [x] Step 0.1.4: Identify which legacy stored procedures are still candidates for active reuse.

### Task 0.2: Confirm architecture boundaries

- [x] Step 0.2.1: Verify domain models do not import SQL Server, FastAPI, filesystem, or export libraries.
- [x] Step 0.2.2: Verify application use cases depend only on domain models and ports.
- [x] Step 0.2.3: Verify SQL Server work is isolated to driven adapters or SQL assets.
- [x] Step 0.2.4: Verify report/export work is isolated to export adapters.

### Task 0.3: Establish developer commands

- [x] Step 0.3.1: Confirm `pytest` runs successfully from repo root.
- [x] Step 0.3.2: Add or update `scripts/dev_check.sh` to run formatting, linting, typing, and tests.
- [x] Step 0.3.3: Add a README section with the exact MVP development commands.
- [x] Step 0.3.4: Make failed checks obvious and local-first.

---

## Phase 1: Define the comparison contract

### Task 1.1: Finalize input contract

- [x] Step 1.1.1: Define `DatasetReference` fields for SQL Server sources.
- [x] Step 1.1.2: Define explicit schema/table naming rules.
- [x] Step 1.1.3: Define key-column selection rules.
- [x] Step 1.1.4: Define excluded-column rules.
- [x] Step 1.1.5: Define null-handling and numeric-precision options.
- [x] Step 1.1.6: Define maximum detailed-difference row limits.

### Task 1.2: Finalize schema projection rules

- [x] Step 1.2.1: Common columns are the comparable projection.
- [x] Step 1.2.2: Before-only columns are reported, not compared.
- [x] Step 1.2.3: After-only columns are reported, not compared.
- [x] Step 1.2.4: Excluded columns are removed from comparison stats.
- [x] Step 1.2.5: Key columns are validated before exclusions are applied.
- [x] Step 1.2.6: Mismatched data types are reported separately from value differences.

### Task 1.3: Finalize output contract

- [x] Step 1.3.1: Define `ComparisonResult` summary fields.
- [x] Step 1.3.2: Define schema-overlap section.
- [x] Step 1.3.3: Define type-mismatch section.
- [x] Step 1.3.4: Define column-stat section.
- [x] Step 1.3.5: Define detailed-difference section.
- [x] Step 1.3.6: Define missing-before and missing-after sections.
- [x] Step 1.3.7: Define warning and failure sections.
- [x] Step 1.3.8: Define evidence manifest fields.

---

## Phase 2: Build fixture-driven test coverage

### Task 2.1: Create tiny fixture datasets

- [x] Step 2.1.1: Fixture A: identical tables, no differences.
- [x] Step 2.1.2: Fixture B: one changed value.
- [x] Step 2.1.3: Fixture C: different column counts.
- [x] Step 2.1.4: Fixture D: excluded column changed but ignored.
- [x] Step 2.1.5: Fixture E: missing row in before table.
- [x] Step 2.1.6: Fixture F: missing row in after table.
- [x] Step 2.1.7: Fixture G: mismatched column type.
- [x] Step 2.1.8: Fixture H: duplicate key on one side.
- [x] Step 2.1.9: Fixture I: null-versus-empty-string behavior.
- [x] Step 2.1.10: Fixture J: numeric precision/rounding behavior.

### Task 2.2: Write expected outputs

- [x] Step 2.2.1: Add expected summary JSON for each fixture.
- [x] Step 2.2.2: Add expected schema-overlap JSON for each fixture.
- [x] Step 2.2.3: Add expected column-stats JSON for changed-value fixtures.
- [x] Step 2.2.4: Add expected missing-row JSON for missing-row fixtures.
- [x] Step 2.2.5: Add expected warning JSON for duplicate-key fixtures.

### Task 2.3: Add contract tests

- [x] Step 2.3.1: Test schema projection with different column counts.
- [x] Step 2.3.2: Test key validation.
- [x] Step 2.3.3: Test exclusion validation.
- [x] Step 2.3.4: Test duplicate-key warning behavior.
- [x] Step 2.3.5: Test result package schema validity.

---

## Phase 3: Stabilize SQL Server adapter path

### Task 3.1: Implement schema inspection

- [x] Step 3.1.1: Add SQL Server adapter method for available tables.
- [x] Step 3.1.2: Add SQL Server adapter method for table columns.
- [x] Step 3.1.3: Include column names, ordinal position, data type, nullability, precision, and scale.
- [x] Step 3.1.4: Add tests or documented manual verification against fixture tables.

### Task 3.2: Implement contract validation

- [x] Step 3.2.1: Validate source and target tables exist.
- [x] Step 3.2.2: Validate selected key columns exist on both sides.
- [x] Step 3.2.3: Validate excluded columns exist on at least one side.
- [x] Step 3.2.4: Reject unsafe identifier strings.
- [x] Step 3.2.5: Return actionable validation messages.

### Task 3.3: Implement comparison execution

- [x] Step 3.3.1: Produce row counts.
- [x] Step 3.3.2: Produce duplicate-key counts.
- [x] Step 3.3.3: Produce schema overlap.
- [x] Step 3.3.4: Produce type mismatches.
- [x] Step 3.3.5: Produce missing-before rows.
- [x] Step 3.3.6: Produce missing-after rows.
- [x] Step 3.3.7: Produce changed-row details.
- [x] Step 3.3.8: Produce column-level difference counts.

### Task 3.4: Harden SQL identifier handling

- [x] Step 3.4.1: Use parameterization for values.
- [x] Step 3.4.2: Use safe quoting for identifiers.
- [x] Step 3.4.3: Never concatenate unvalidated schema, table, or column names.
- [x] Step 3.4.4: Add tests or review notes for unsafe identifier rejection.

---

## Phase 4: Build the application workflow

### Task 4.1: Implement the primary use case

- [x] Step 4.1.1: Implement `RunComparisonUseCase` orchestration.
- [x] Step 4.1.2: Load schema profiles through the dataset source port.
- [x] Step 4.1.3: Validate the comparison contract.
- [x] Step 4.1.4: Run comparison through the dataset source port.
- [x] Step 4.1.5: Store the result package through the result store port.
- [x] Step 4.1.6: Return run ID and summary.

### Task 4.2: Implement run persistence

- [x] Step 4.2.1: Store run metadata locally.
- [x] Step 4.2.2: Store result sections as JSON.
- [x] Step 4.2.3: Store generated artifacts under a run directory.
- [x] Step 4.2.4: Add a load-run use case.
- [x] Step 4.2.5: Add deterministic run folder naming.

### Task 4.3: Implement minimal API surface

- [x] Step 4.3.1: Endpoint: health check.
- [x] Step 4.3.2: Endpoint: inspect source schema.
- [x] Step 4.3.3: Endpoint: validate comparison contract.
- [x] Step 4.3.4: Endpoint: run comparison.
- [x] Step 4.3.5: Endpoint: load run result.
- [x] Step 4.3.6: Endpoint: export run artifact.

---

## Phase 5: Produce evidence artifacts

### Task 5.1: JSON result package

- [x] Step 5.1.1: Write `manifest.json`.
- [x] Step 5.1.2: Write `summary.json`.
- [x] Step 5.1.3: Write `schema_overlap.json`.
- [x] Step 5.1.4: Write `type_mismatches.json`.
- [x] Step 5.1.5: Write `column_stats.json`.
- [x] Step 5.1.6: Write `detailed_differences.json`.
- [x] Step 5.1.7: Write `missing_before.json`.
- [x] Step 5.1.8: Write `missing_after.json`.

### Task 5.2: Basic HTML report

- [x] Step 5.2.1: Render run metadata.
- [x] Step 5.2.2: Render summary cards.
- [x] Step 5.2.3: Render schema overlap.
- [x] Step 5.2.4: Render type mismatches.
- [x] Step 5.2.5: Render column stats.
- [x] Step 5.2.6: Render detailed differences.
- [x] Step 5.2.7: Render missing rows.
- [x] Step 5.2.8: Render warnings clearly.

### Task 5.3: Basic XLSX export

- [x] Step 5.3.1: Sheet: Summary.
- [x] Step 5.3.2: Sheet: Schema Overlap.
- [x] Step 5.3.3: Sheet: Type Mismatches.
- [x] Step 5.3.4: Sheet: Column Stats.
- [x] Step 5.3.5: Sheet: Detailed Differences.
- [x] Step 5.3.6: Sheet: Missing Before.
- [x] Step 5.3.7: Sheet: Missing After.
- [x] Step 5.3.8: Sheet: Manifest.

---

## Phase 6: Document and verify the MVP

### Task 6.1: Write user docs

- [x] Step 6.1.1: Document the comparison workflow.
- [x] Step 6.1.2: Document key selection.
- [x] Step 6.1.3: Document excluded columns.
- [x] Step 6.1.4: Document different-column-count behavior.
- [x] Step 6.1.5: Document duplicate-key behavior.
- [x] Step 6.1.6: Document export artifacts.

### Task 6.2: Write developer docs

- [x] Step 6.2.1: Document hexagonal boundaries.
- [x] Step 6.2.2: Document ports and adapters.
- [x] Step 6.2.3: Document SQL Server adapter assumptions.
- [x] Step 6.2.4: Document fixture test strategy.
- [x] Step 6.2.5: Document how to add a future source adapter.

### Task 6.3: Release `0.1.0`

- [x] Step 6.3.1: Run full local checks.
- [x] Step 6.3.2: Update README current status.
- [x] Step 6.3.3: Update changelog or release notes.
- [x] Step 6.3.4: Prepare local Git tag command for `v0.1.0` in `RELEASE_NOTES.md`.
- [x] Step 6.3.5: Archive sample evidence package generated from fixtures.

---

## MVP completion notes

The root `0.1.0` MVP checklist is implemented as a local-first starting point. The pure comparison engine, fixture adapter, result store, API, CLI, JSON sections, HTML report, and XLSX export are active. The SQL Server adapter is implemented as a read-only boundary using metadata inspection and bounded table reads, but it has not been verified against a live SQL Server instance in this environment. Manual SQL Server smoke fixtures are provided under `sql/fixtures/`.

Validation command used for this checkpoint:

```bash
./scripts/dev_check.sh
```

Current automated result:

```text
20 passed
```

---

## MVP extension: `0.1.2` source-agnostic suites and CSV ingest

This extension was pulled forward before the later roadmap waves because it is small, high-value, and follows the existing hexagonal boundary.

### Phase 7: Add source-agnostic comparison suites

#### Task 7.1: Define suite contract

- [x] Step 7.1.1: Add a baseline dataset reference.
- [x] Step 7.1.2: Add one-or-more candidate dataset references.
- [x] Step 7.1.3: Reuse key-column, exclusion, null, precision, and detail-limit options.
- [x] Step 7.1.4: Expand the suite contract into ordinary binary comparison contracts.

#### Task 7.2: Run suite comparisons

- [x] Step 7.2.1: Add `RunComparisonSuiteUseCase` above the existing comparison engine.
- [x] Step 7.2.2: Validate every candidate comparison before emitting evidence.
- [x] Step 7.2.3: Run baseline-vs-candidate comparisons through the selected source adapter.
- [x] Step 7.2.4: Summarize candidate status as PASS, WARN, or FAIL.
- [x] Step 7.2.5: Compute best candidate by lowest difference score.

#### Task 7.3: Persist suite evidence

- [x] Step 7.3.1: Write `suite_result.json`.
- [x] Step 7.3.2: Write `suite_summary.json`.
- [x] Step 7.3.3: Write `candidate_summaries.json`.
- [x] Step 7.3.4: Write individual comparison evidence under `comparisons/<candidate>/`.
- [x] Step 7.3.5: Render suite-level HTML and XLSX reports.

### Phase 8: Add CSV ingestion without adding CSV-specific comparison logic

#### Task 8.1: Ingest CSV into SQLite

- [x] Step 8.1.1: Add CSV adapter that reads headered CSV files.
- [x] Step 8.1.2: Normalize CSV table and column names into safe identifiers.
- [x] Step 8.1.3: Materialize CSV rows into SQLite `TEXT` tables.
- [x] Step 8.1.4: Return normal `DatasetReference` objects for comparison.

#### Task 8.2: Add CSV pair command

- [x] Step 8.2.1: Add `run-csv` CLI command.
- [x] Step 8.2.2: Ingest before/after CSV files into SQLite.
- [x] Step 8.2.3: Reuse existing comparison, JSON, HTML, and XLSX paths.

#### Task 8.3: Add CSV suite command

- [x] Step 8.3.1: Define CSV suite manifest format.
- [x] Step 8.3.2: Add `run-csv-suite` CLI command.
- [x] Step 8.3.3: Ingest baseline plus N candidate CSV files into SQLite.
- [x] Step 8.3.4: Reuse the source-agnostic suite use case.

#### Task 8.4: Verify the feature

- [x] Step 8.4.1: Add unit tests for suite contracts and summaries.
- [x] Step 8.4.2: Add integration tests for CSV ingestion.
- [x] Step 8.4.3: Add integration tests for SQLite-backed suites.
- [x] Step 8.4.4: Add e2e CLI tests for CSV pair and CSV suite workflows.
- [x] Step 8.4.5: Update README, docs, and release notes.
