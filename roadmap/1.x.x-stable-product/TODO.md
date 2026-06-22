# TODO: `1.x.x` Stable Product Wave

## Purpose

Finish Deltus as a stable, extensible comparison evidence product with a durable API, tested adapters, production-grade exports, and clear boundaries for future source integrations.

## Version intent

- `1.0.0`: stable local/self-hosted product.
- `1.1.x+`: deeper adapters, performance improvements, and enterprise/team features.

## Definition of Done

- [ ] The comparison contract is stable and versioned.
- [ ] The result package contract is stable and versioned.
- [ ] SQL Server and local file adapters are contract-tested.
- [ ] HTML, XLSX, PDF, JSON, and CSV exports are production quality.
- [ ] The frontend supports the full comparison workflow.
- [ ] Performance limits are documented and tested.
- [ ] Docs make the tool understandable without historical context.

---

## Phase 1: Stable contracts

### Task 1.1: Version comparison contract

- [ ] Step 1.1.1: Add `contract_version` to comparison requests.
- [ ] Step 1.1.2: Add migration policy for future contract versions.
- [ ] Step 1.1.3: Freeze required fields.
- [ ] Step 1.1.4: Freeze option names.
- [ ] Step 1.1.5: Add backward-compatibility tests.

### Task 1.2: Version result package

- [ ] Step 1.2.1: Add `result_contract_version` to manifest.
- [ ] Step 1.2.2: Freeze result section names.
- [ ] Step 1.2.3: Freeze warning code names.
- [ ] Step 1.2.4: Freeze export manifest shape.
- [ ] Step 1.2.5: Add schema validation to every generated result package.

### Task 1.3: Define extension rules

- [ ] Step 1.3.1: Define how new adapters identify source type.
- [ ] Step 1.3.2: Define how new comparison options are added.
- [ ] Step 1.3.3: Define how new report sections are added.
- [ ] Step 1.3.4: Define compatibility expectations for old runs.
- [ ] Step 1.3.5: Document extension boundaries.

---

## Phase 2: Production-grade comparison runtime

### Task 2.1: Performance and scale limits

- [ ] Step 2.1.1: Benchmark small fixture runs.
- [ ] Step 2.1.2: Benchmark medium generated datasets.
- [ ] Step 2.1.3: Benchmark large generated datasets.
- [ ] Step 2.1.4: Define recommended row-count ranges.
- [ ] Step 2.1.5: Define fallback strategies for very large detail output.

### Task 2.2: Streaming and paging

- [ ] Step 2.2.1: Page detailed differences.
- [ ] Step 2.2.2: Page missing rows.
- [ ] Step 2.2.3: Export large sections without loading everything into frontend memory.
- [ ] Step 2.2.4: Add artifact chunking if needed.
- [ ] Step 2.2.5: Document large-run behavior.

### Task 2.3: Failure recovery

- [ ] Step 2.3.1: Persist failed run metadata.
- [ ] Step 2.3.2: Preserve partial logs safely.
- [ ] Step 2.3.3: Mark partial artifacts clearly.
- [ ] Step 2.3.4: Add retry guidance.
- [ ] Step 2.3.5: Add failure-code taxonomy.

---

## Phase 3: Full workflow frontend

### Task 3.1: Comparison creation flow

- [ ] Step 3.1.1: Guided source setup.
- [ ] Step 3.1.2: Live schema inspection.
- [ ] Step 3.1.3: Key-column recommendations.
- [ ] Step 3.1.4: Exclusion selection.
- [ ] Step 3.1.5: Option selection.
- [ ] Step 3.1.6: Pre-run validation.
- [ ] Step 3.1.7: Run progress display.

### Task 3.2: Evidence review flow

- [ ] Step 3.2.1: Summary-first report layout.
- [ ] Step 3.2.2: Difference drilldown.
- [ ] Step 3.2.3: Column-focused review.
- [ ] Step 3.2.4: Missing-row review.
- [ ] Step 3.2.5: Warning review.
- [ ] Step 3.2.6: Manifest review.

### Task 3.3: Export flow

- [ ] Step 3.3.1: Export all artifacts.
- [ ] Step 3.3.2: Export single artifact.
- [ ] Step 3.3.3: Re-export historical run.
- [ ] Step 3.3.4: Download zipped evidence package.
- [ ] Step 3.3.5: Show export provenance.

---

## Phase 4: Stable adapter ecosystem

### Task 4.1: SQL Server adapter finalization

- [ ] Step 4.1.1: Confirm read-only mode.
- [ ] Step 4.1.2: Confirm snapshot/copy-to-slow-server mode.
- [ ] Step 4.1.3: Confirm indexing helper policy.
- [ ] Step 4.1.4: Confirm permissions model.
- [ ] Step 4.1.5: Confirm SQL Server docs.

### Task 4.2: Local file adapter finalization

- [ ] Step 4.2.1: Confirm CSV behavior.
- [ ] Step 4.2.2: Confirm Parquet behavior.
- [ ] Step 4.2.3: Confirm type inference warnings.
- [ ] Step 4.2.4: Confirm large file limits.
- [ ] Step 4.2.5: Confirm docs.

### Task 4.3: Future adapter candidates

- [ ] Step 4.3.1: Evaluate PostgreSQL adapter.
- [ ] Step 4.3.2: Evaluate DuckDB native adapter.
- [ ] Step 4.3.3: Evaluate SQLite adapter.
- [ ] Step 4.3.4: Evaluate S3/object storage file adapter.
- [ ] Step 4.3.5: Keep candidates behind explicit roadmap gates.

---

## Phase 5: Release `1.0.0`

### Task 5.1: Release readiness

- [ ] Step 5.1.1: All tests pass from clean checkout.
- [ ] Step 5.1.2: Docs build passes.
- [ ] Step 5.1.3: Sample evidence package generated.
- [ ] Step 5.1.4: Security/data-safety docs complete.
- [ ] Step 5.1.5: Known limitations complete.
- [ ] Step 5.1.6: API/contract compatibility policy complete.

### Task 5.2: Final release artifacts

- [ ] Step 5.2.1: Publish source release.
- [ ] Step 5.2.2: Publish sample reports.
- [ ] Step 5.2.3: Publish docs site.
- [ ] Step 5.2.4: Tag `v1.0.0`.

---

## Phase 6: `1.x.x` expansion backlog

### Task 6.1: Adapter expansion

- [ ] Step 6.1.1: Add PostgreSQL if demand is proven.
- [ ] Step 6.1.2: Add SQLite if useful for local app comparisons.
- [ ] Step 6.1.3: Add DuckDB-native source if local analytical workflows grow.
- [ ] Step 6.1.4: Add object-storage file source only after local file path is stable.

### Task 6.2: Team features

- [ ] Step 6.2.1: Add optional auth only if multi-user deployment becomes real.
- [ ] Step 6.2.2: Add role-based access only if shared environments require it.
- [ ] Step 6.2.3: Add shared run repository only after local run history is stable.
- [ ] Step 6.2.4: Add audit trail export for regulated workflows.

### Task 6.3: Advanced comparison features

- [ ] Step 6.3.1: Add column mapping for renamed columns.
- [ ] Step 6.3.2: Add computed comparison expressions.
- [ ] Step 6.3.3: Add tolerance profiles.
- [ ] Step 6.3.4: Add saved comparison templates.
- [ ] Step 6.3.5: Add trend/history comparisons across repeated runs.
