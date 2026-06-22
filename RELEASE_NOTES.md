# Release Notes

## 0.1.2

Adds the first source-agnostic comparison-suite workflow and CSV ingestion path.

- Added `ComparisonSuiteContract` for baseline-vs-candidate comparison suites.
- Added `ComparisonSuiteResult`, candidate summaries, suite status, and best-candidate scoring.
- Added `RunComparisonSuiteUseCase` above the existing binary comparison engine.
- Added CSV ingestion adapter that materializes CSV files into SQLite tables.
- Added `run-csv` CLI command for pair comparisons.
- Added `run-csv-suite` CLI command for baseline plus N candidate CSV comparisons.
- Added `run-suite-sqlite` CLI command for SQLite table suites.
- Added suite HTML and XLSX report exporters.
- Added CSV and suite docs.
- Added CSV fixture suite and tests.

Validation:

```text
34 passed
front matter check passed
```

## 0.1.1

- Added SQLite source adapter path.
- Added SQLite fixture database generation.
- Added SQLite CLI and integration tests.

## 0.1.0

Initial MVP:

- Pure comparison engine.
- Local fixture source.
- SQL Server source boundary.
- JSON result package.
- HTML report export.
- XLSX workbook export.
- Minimal API surface.
