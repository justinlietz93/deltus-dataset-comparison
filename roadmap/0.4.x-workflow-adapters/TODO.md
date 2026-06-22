# TODO: `0.4.x` Workflow and Adapter Wave

## Purpose

Expand Deltus beyond the first SQL Server path without breaking the core contract. This wave adds workflow convenience, local file comparison, run history, and adapter substitutability.

## Version intent

- `0.4.0`: local file adapters and stronger run management.
- `0.4.1+`: adapter fixes, CLI improvements, and workflow polish.

## Definition of Done

- [ ] The comparison core can run against at least one non-SQL source adapter.
- [ ] Completed runs can be listed, reopened, exported, and deleted locally.
- [ ] The CLI can execute a comparison from a contract file.
- [ ] Adapter contract tests prove substitutability.
- [ ] The domain model remains unchanged when new adapters are added.

---

## Phase 1: Local file source adapters

### Task 1.1: Add CSV adapter

- [ ] Step 1.1.1: Define CSV dataset reference fields.
- [ ] Step 1.1.2: Read header and infer schema profile.
- [ ] Step 1.1.3: Support delimiter option.
- [ ] Step 1.1.4: Support encoding option.
- [ ] Step 1.1.5: Run comparison through the same dataset source port.
- [ ] Step 1.1.6: Add CSV fixture contract tests.

### Task 1.2: Add Parquet adapter

- [ ] Step 1.2.1: Define Parquet dataset reference fields.
- [ ] Step 1.2.2: Read schema profile.
- [ ] Step 1.2.3: Run comparison through DuckDB or Polars.
- [ ] Step 1.2.4: Add Parquet fixture contract tests.
- [ ] Step 1.2.5: Document known type-mapping differences.

### Task 1.3: Normalize type profiles

- [ ] Step 1.3.1: Define source-native type field.
- [ ] Step 1.3.2: Define normalized comparison type field.
- [ ] Step 1.3.3: Map SQL Server numeric/text/date types.
- [ ] Step 1.3.4: Map CSV inferred types.
- [ ] Step 1.3.5: Map Parquet types.
- [ ] Step 1.3.6: Add fixtures for cross-source type behavior.

---

## Phase 2: Run management

### Task 2.1: Local run database

- [ ] Step 2.1.1: Add SQLite run metadata store.
- [ ] Step 2.1.2: Store run status.
- [ ] Step 2.1.3: Store run source labels.
- [ ] Step 2.1.4: Store artifact paths.
- [ ] Step 2.1.5: Store warning and difference counts for quick listing.

### Task 2.2: Run lifecycle

- [ ] Step 2.2.1: Create run.
- [ ] Step 2.2.2: Mark run completed.
- [ ] Step 2.2.3: Mark run failed.
- [ ] Step 2.2.4: Reopen run.
- [ ] Step 2.2.5: Delete run and artifacts.
- [ ] Step 2.2.6: Re-export run without recomparing.

### Task 2.3: Run search and filtering

- [ ] Step 2.3.1: Filter by source label.
- [ ] Step 2.3.2: Filter by date range.
- [ ] Step 2.3.3: Filter by status.
- [ ] Step 2.3.4: Filter by warnings.
- [ ] Step 2.3.5: Filter by changed rows.

---

## Phase 3: CLI workflow

### Task 3.1: Contract-file execution

- [ ] Step 3.1.1: Add `deltus validate contract.json`.
- [ ] Step 3.1.2: Add `deltus inspect contract.json`.
- [ ] Step 3.1.3: Add `deltus compare contract.json`.
- [ ] Step 3.1.4: Add `deltus export RUN_ID --format xlsx`.
- [ ] Step 3.1.5: Add useful exit codes.

### Task 3.2: CLI templates

- [ ] Step 3.2.1: Generate SQL Server contract template.
- [ ] Step 3.2.2: Generate CSV contract template.
- [ ] Step 3.2.3: Generate Parquet contract template.
- [ ] Step 3.2.4: Validate templates against schema.
- [ ] Step 3.2.5: Document CLI examples.

---

## Phase 4: Frontend workflow polish

### Task 4.1: New comparison wizard

- [ ] Step 4.1.1: Source type selector.
- [ ] Step 4.1.2: Source A configuration.
- [ ] Step 4.1.3: Source B configuration.
- [ ] Step 4.1.4: Schema inspection step.
- [ ] Step 4.1.5: Key-column selector.
- [ ] Step 4.1.6: Exclusion selector.
- [ ] Step 4.1.7: Options step.
- [ ] Step 4.1.8: Review and run step.

### Task 4.2: Run history page

- [ ] Step 4.2.1: List recent runs.
- [ ] Step 4.2.2: Show status and counts.
- [ ] Step 4.2.3: Reopen run.
- [ ] Step 4.2.4: Export run.
- [ ] Step 4.2.5: Delete run.

---

## Phase 5: Release `0.4.x`

### Task 5.1: Adapter QA

- [ ] Step 5.1.1: Run SQL Server contract tests.
- [ ] Step 5.1.2: Run CSV contract tests.
- [ ] Step 5.1.3: Run Parquet contract tests.
- [ ] Step 5.1.4: Run CLI smoke tests.
- [ ] Step 5.1.5: Run frontend smoke tests.

### Task 5.2: Ship release

- [ ] Step 5.2.1: Update adapter docs.
- [ ] Step 5.2.2: Update CLI docs.
- [ ] Step 5.2.3: Update release notes.
- [ ] Step 5.2.4: Tag `v0.4.0`.
