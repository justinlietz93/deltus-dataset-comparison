---
title: "CSV Adapter"
status: current
authority: canonical
---

# CSV Adapter

The CSV adapter is an ingest adapter. It does not compare CSV files directly.

It materializes CSV files into SQLite tables, then routes comparison through the existing SQLite source adapter and shared comparison engine.

```text
CSV file(s)
  -> CSV ingest adapter
  -> SQLite tables
  -> SQLite dataset source
  -> comparison engine
  -> evidence package
```

## Pair mode

Use pair mode when comparing one baseline CSV to one candidate CSV.

```bash
python -m comparison_evidence.adapters.driving.cli run-csv \
  --before-csv data/before.csv \
  --after-csv data/after.csv \
  --keys id \
  --exclude batch_id,load_timestamp \
  --export-root exports
```

## Suite mode

Use suite mode when comparing one baseline CSV to multiple candidate CSVs.

```bash
python -m comparison_evidence.adapters.driving.cli run-csv-suite \
  --manifest tests/fixtures/csv_suite/manifest.json \
  --export-root exports
```

## Manifest format

```json
{
  "suite_name": "customer_change_suite",
  "baseline": {"name": "baseline", "path": "baseline.csv"},
  "candidates": [
    {"name": "candidate_a", "path": "candidate_a.csv"},
    {"name": "candidate_b", "path": "candidate_b.csv"}
  ],
  "key_columns": ["id"],
  "excluded_columns": ["batch_id"],
  "clear_nulls": true,
  "max_detail_rows": 100
}
```

## Current boundary

The MVP CSV adapter stores CSV columns as SQLite `TEXT` columns. This keeps the path predictable and lets numeric precision handling remain a comparison option. Later adapter polish can add explicit type hints, delimiter presets, encoding profiles, and large-file streaming.
