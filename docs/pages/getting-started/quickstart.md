---
title: "Quickstart"
status: planned
authority: canonical
---

# Quickstart

The first runnable quickstart will compare two small fixture datasets and export an evidence package.

## Planned command

```bash
compare-evidence run --contract examples/contracts/basic-sqlserver.json --export ./exports/basic-run
```

## Expected outputs

```text
exports/basic-run/
├─ report.html
├─ report.xlsx
├─ report.pdf
├─ manifest.json
├─ summary.json
├─ column_stats.csv
├─ detailed_differences.csv
├─ missing_before.csv
└─ missing_after.csv
```
