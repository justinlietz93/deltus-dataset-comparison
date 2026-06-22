# TODO: `0.5.x` Team Polish Wave

## Purpose

Make Deltus feel like a tool another developer can pick up, trust, run locally, and use as ticket evidence without needing personal guidance from the original author.

## Version intent

- `0.5.0`: team-ready local usage and documentation.
- `0.5.1+`: onboarding polish, packaging, demos, and sample evidence.

## Definition of Done

- [ ] A new developer can install and run a fixture comparison in under 15 minutes.
- [ ] The README explains the value, workflow, and constraints clearly.
- [ ] Sample evidence packages demonstrate realistic use cases.
- [ ] Local packaging is repeatable.
- [ ] The tool has clear safety and data-handling guidance.

---

## Phase 1: Onboarding polish

### Task 1.1: Rewrite README for users

- [ ] Step 1.1.1: Add concise product description.
- [ ] Step 1.1.2: Add the original problem story without overexplaining.
- [ ] Step 1.1.3: Add supported source types.
- [ ] Step 1.1.4: Add quickstart.
- [ ] Step 1.1.5: Add evidence artifact examples.
- [ ] Step 1.1.6: Add limitations.

### Task 1.2: Add first-run guide

- [ ] Step 1.2.1: Explain fixture comparison.
- [ ] Step 1.2.2: Explain SQL Server comparison.
- [ ] Step 1.2.3: Explain local file comparison.
- [ ] Step 1.2.4: Explain exports.
- [ ] Step 1.2.5: Explain where run artifacts are stored.

### Task 1.3: Add troubleshooting guide

- [ ] Step 1.3.1: SQL Server connection failures.
- [ ] Step 1.3.2: ODBC driver issues.
- [ ] Step 1.3.3: Permission errors.
- [ ] Step 1.3.4: Duplicate-key warnings.
- [ ] Step 1.3.5: Large diff output.
- [ ] Step 1.3.6: Export failures.

---

## Phase 2: Packaging polish

### Task 2.1: Python package path

- [ ] Step 2.1.1: Confirm install from local checkout.
- [ ] Step 2.1.2: Confirm editable install.
- [ ] Step 2.1.3: Confirm CLI entry point.
- [ ] Step 2.1.4: Confirm dependency groups.
- [ ] Step 2.1.5: Add package metadata.

### Task 2.2: Local app run path

- [ ] Step 2.2.1: Add backend dev command.
- [ ] Step 2.2.2: Add frontend dev command.
- [ ] Step 2.2.3: Add single script for local dev startup.
- [ ] Step 2.2.4: Add environment example.
- [ ] Step 2.2.5: Add health checks.

### Task 2.3: Container path

- [ ] Step 2.3.1: Add backend Dockerfile.
- [ ] Step 2.3.2: Add frontend Dockerfile or static build path.
- [ ] Step 2.3.3: Add compose file for local demo.
- [ ] Step 2.3.4: Add volume mapping for artifacts.
- [ ] Step 2.3.5: Document container limitations.

---

## Phase 3: Evidence examples

### Task 3.1: Sample runs

- [ ] Step 3.1.1: Generate clean comparison sample.
- [ ] Step 3.1.2: Generate changed-values sample.
- [ ] Step 3.1.3: Generate different-schema sample.
- [ ] Step 3.1.4: Generate missing-rows sample.
- [ ] Step 3.1.5: Generate duplicate-key warning sample.

### Task 3.2: Sample artifacts

- [ ] Step 3.2.1: Save sample HTML.
- [ ] Step 3.2.2: Save sample XLSX.
- [ ] Step 3.2.3: Save sample PDF.
- [ ] Step 3.2.4: Save sample JSON manifest.
- [ ] Step 3.2.5: Add docs page explaining each sample.

---

## Phase 4: Safety and governance

### Task 4.1: Data safety docs

- [ ] Step 4.1.1: Explain local-first assumption.
- [ ] Step 4.1.2: Explain secrets handling.
- [ ] Step 4.1.3: Explain artifact storage.
- [ ] Step 4.1.4: Explain sensitive-data risks in exports.
- [ ] Step 4.1.5: Explain recommended use on copied/snapshot tables.

### Task 4.2: Result authority docs

- [ ] Step 4.2.1: Define what the report proves.
- [ ] Step 4.2.2: Define what the report does not prove.
- [ ] Step 4.2.3: Define how duplicate keys limit interpretation.
- [ ] Step 4.2.4: Define how excluded columns affect evidence.
- [ ] Step 4.2.5: Define how type mismatches affect value comparison.

---

## Phase 5: Release `0.5.x`

### Task 5.1: New-user test

- [ ] Step 5.1.1: Run install from clean checkout.
- [ ] Step 5.1.2: Run fixture comparison.
- [ ] Step 5.1.3: Run SQL Server smoke path if available.
- [ ] Step 5.1.4: Open report reader.
- [ ] Step 5.1.5: Export artifacts.

### Task 5.2: Ship release

- [ ] Step 5.2.1: Update README screenshots or examples.
- [ ] Step 5.2.2: Update docs index.
- [ ] Step 5.2.3: Update release notes.
- [ ] Step 5.2.4: Tag `v0.5.0`.
