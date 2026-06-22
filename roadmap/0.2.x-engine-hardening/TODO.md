# TODO: `0.2.x` Engine Hardening Wave

## Purpose

Turn the `0.1.0` MVP into a reliable SQL Server comparison engine with stronger safety, clearer failure modes, and better parity against the original SSRS-era behavior.

## Version intent

- `0.2.0`: SQL Server comparison behavior hardened.
- `0.2.1+`: bug fixes, fixture expansion, and legacy parity gaps.

## Definition of Done

- [ ] SQL Server identifier handling is consistently safe.
- [ ] Duplicate-key behavior is explicit and tested.
- [ ] Large comparisons have predictable limits and warnings.
- [ ] Legacy report sections are either implemented, replaced, or intentionally deferred.
- [ ] Every adapter path used by the MVP has contract tests.

---

## Phase 1: Legacy parity review

### Task 1.1: Map legacy sections to modern result sections

- [ ] Step 1.1.1: Map legacy basic info output.
- [ ] Step 1.1.2: Map legacy overall stats output.
- [ ] Step 1.1.3: Map legacy column stats output.
- [ ] Step 1.1.4: Map legacy detailed differences output.
- [ ] Step 1.1.5: Map legacy missing-before output.
- [ ] Step 1.1.6: Map legacy missing-after output.
- [ ] Step 1.1.7: Map legacy mismatched-types output.
- [ ] Step 1.1.8: Mark any intentionally dropped SSRS-only behavior.

### Task 1.2: Build parity fixtures

- [ ] Step 1.2.1: Create fixture matching old identical-table case.
- [ ] Step 1.2.2: Create fixture matching old different-column-count case.
- [ ] Step 1.2.3: Create fixture matching old excluded-column case.
- [ ] Step 1.2.4: Create fixture matching old missing-row case.
- [ ] Step 1.2.5: Create fixture matching old type-mismatch case.
- [ ] Step 1.2.6: Compare modern result output to expected legacy behavior.

---

## Phase 2: SQL Server safety hardening

### Task 2.1: Validate all identifiers

- [ ] Step 2.1.1: Centralize SQL Server identifier validation.
- [ ] Step 2.1.2: Reject empty schema, table, and column names.
- [ ] Step 2.1.3: Reject names containing unsafe delimiter characters.
- [ ] Step 2.1.4: Validate identifiers against database metadata before dynamic SQL.
- [ ] Step 2.1.5: Add negative tests for malicious or malformed names.

### Task 2.2: Standardize query generation

- [ ] Step 2.2.1: Centralize quoted identifier construction.
- [ ] Step 2.2.2: Remove hand-built bracket syntax.
- [ ] Step 2.2.3: Parameterize comparison values and thresholds.
- [ ] Step 2.2.4: Log generated SQL only in safe debug mode.
- [ ] Step 2.2.5: Add review notes for every dynamic SQL entry point.

### Task 2.3: Add execution guardrails

- [ ] Step 2.3.1: Add configurable max detailed-difference rows.
- [ ] Step 2.3.2: Add configurable timeout.
- [ ] Step 2.3.3: Add row-count warning thresholds.
- [ ] Step 2.3.4: Add duplicate-key failure or warning policy.
- [ ] Step 2.3.5: Add clear error messages for missing permissions.

---

## Phase 3: Result correctness hardening

### Task 3.1: Null and empty value rules

- [ ] Step 3.1.1: Define whether null equals empty string.
- [ ] Step 3.1.2: Define whether trimmed strings are compared.
- [ ] Step 3.1.3: Define case-sensitive versus case-insensitive comparison option.
- [ ] Step 3.1.4: Add fixtures for each option.
- [ ] Step 3.1.5: Render the selected options in the manifest.

### Task 3.2: Numeric precision rules

- [ ] Step 3.2.1: Define decimal precision tolerance.
- [ ] Step 3.2.2: Define float comparison tolerance.
- [ ] Step 3.2.3: Define date/time precision rules.
- [ ] Step 3.2.4: Add fixtures for each precision mode.
- [ ] Step 3.2.5: Render precision policy in output artifacts.

### Task 3.3: Duplicate-key policy

- [ ] Step 3.3.1: Detect duplicate keys before value comparison.
- [ ] Step 3.3.2: Count duplicate keys on before side.
- [ ] Step 3.3.3: Count duplicate keys on after side.
- [ ] Step 3.3.4: Prevent duplicated joins from inflating stats silently.
- [ ] Step 3.3.5: Add a visible warning or fail-fast setting.

---

## Phase 4: Adapter contract tests

### Task 4.1: Dataset source contract tests

- [ ] Step 4.1.1: Contract test: inspect schema.
- [ ] Step 4.1.2: Contract test: validate comparison contract.
- [ ] Step 4.1.3: Contract test: run comparison.
- [ ] Step 4.1.4: Contract test: handle missing source.
- [ ] Step 4.1.5: Contract test: handle permissions failure.

### Task 4.2: Result store contract tests

- [ ] Step 4.2.1: Contract test: create run record.
- [ ] Step 4.2.2: Contract test: save result section.
- [ ] Step 4.2.3: Contract test: load run record.
- [ ] Step 4.2.4: Contract test: list recent runs.
- [ ] Step 4.2.5: Contract test: handle corrupt or missing run data.

---

## Phase 5: Release `0.2.x`

### Task 5.1: Update docs

- [ ] Step 5.1.1: Update SQL Server adapter docs.
- [ ] Step 5.1.2: Update result contract docs.
- [ ] Step 5.1.3: Update known limitations.
- [ ] Step 5.1.4: Add legacy parity matrix.

### Task 5.2: Ship release

- [ ] Step 5.2.1: Run all local checks.
- [ ] Step 5.2.2: Generate sample evidence package.
- [ ] Step 5.2.3: Update release notes.
- [ ] Step 5.2.4: Tag `v0.2.0`.
