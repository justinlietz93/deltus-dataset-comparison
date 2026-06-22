# Release Notes

## v0.1.1 SQLite Verification

Deltus now has a SQLite adapter proof path for local testing without SQL Server.

### Added

- Read-only SQLite dataset source adapter.
- SQLite fixture database generator.
- SQLite CLI command: `run-sqlite`.
- SQLite integration tests for schema inspection, changed values, different column counts, duplicate keys, and bounded reads.
- SQLite e2e CLI export test.

### Verification

```bash
26 passed
```

## v0.1.0 MVP

Deltus now has a complete local-first MVP starting point.

### Added

- Pure tabular comparison engine.
- Validated comparison contracts.
- Schema projection for different-column-count tables.
- Type mismatch reporting.
- Duplicate key hard warnings.
- Missing-before and missing-after rows.
- Detailed cell differences.
- Column-level comparison statistics.
- JSON result package writer.
- HTML evidence report exporter.
- XLSX evidence workbook exporter.
- Local fixture dataset adapter.
- Read-only SQL Server adapter boundary.
- Minimal FastAPI surface.
- Fixture comparison CLI.
- MVP fixture datasets and expected summaries.
- Contract, unit, integration, and e2e tests.

### Notes

- The SQL Server adapter is implemented but not live-verified in this environment.
- The old SSRS/RDL path remains reference-only.
- PDF export is intentionally deferred to a later polish wave.

### Suggested local tag command

```bash
git tag -a v0.1.0 -m "Deltus 0.1.0 MVP"
git push origin v0.1.0
```
