---
title: "Comparison Suite"
status: current
authority: canonical
---

# Comparison Suite

A comparison suite compares one trusted baseline dataset against multiple candidate datasets.

```text
baseline
  -> candidate_a
  -> candidate_b
  -> candidate_c
```

The suite feature is source-agnostic. CSV, SQLite, SQL Server, or future adapters should all produce `DatasetReference` values and reuse the same suite contract.

## Purpose

Suites are useful when a developer wants to compare multiple implementation outputs against the same original result.

Example:

```text
original output
  -> output from implementation A
  -> output from implementation B
```

The suite report answers:

- which candidate preserved the baseline best
- which candidates introduced missing or extra rows
- which candidates changed cells
- which candidates produced warnings
- which individual comparison reports need review

## Result status

Candidate statuses are intentionally conservative:

| Status | Meaning |
| --- | --- |
| PASS | No changed cells and no warnings. |
| WARN | Changed cells or warnings exist, but no hard-fail condition was detected. |
| FAIL | Missing rows, duplicate keys, type mismatches, or failures were detected. |

Changed cells are `WARN` rather than `FAIL` because some regression tests intentionally change values. The suite records the evidence; the developer decides whether the change was expected.

## Output package

```text
exports/<suite_id>/
├─ suite_result.json
├─ suite_manifest.json
├─ suite_summary.json
├─ candidate_summaries.json
├─ suite_report.html
├─ suite_report.xlsx
└─ comparisons/
   ├─ candidate_a/
   │  ├─ result.json
   │  ├─ report.html
   │  └─ report.xlsx
   └─ candidate_b/
      ├─ result.json
      ├─ report.html
      └─ report.xlsx
```
