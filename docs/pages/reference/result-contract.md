---
title: "Result Contract"
status: current
authority: canonical
---

# Result Contract

Every comparison run produces the same logical sections regardless of source adapter.

## Required sections

| Section | Purpose |
|---|---|
| `manifest` | Run identity, source labels, options, and tool version. |
| `summary` | Counts and high-level evidence numbers. |
| `schema_overlap` | Common, comparable, before-only, after-only, excluded, and key columns. |
| `type_mismatches` | Shared columns whose data types differ. |
| `column_stats` | Per-column compared, matched, and different cell counts. |
| `detailed_differences` | Cell-level differences keyed by selected key columns. |
| `missing_before` | Rows present after but missing before. |
| `missing_after` | Rows present before but missing after. |
| `duplicate_keys` | Duplicate key occurrences by side. |
| `warnings` | Human-review warnings. |
| `failures` | Reserved for failed run evidence. |

## Export mapping

| Section | HTML | XLSX | JSON |
|---|---:|---:|---:|
| manifest | yes | yes | yes |
| summary | yes | yes | yes |
| schema overlap | yes | yes | yes |
| type mismatches | yes | yes | yes |
| column stats | yes | yes | yes |
| detailed differences | yes | yes | yes |
| missing before | yes | yes | yes |
| missing after | yes | yes | yes |
| duplicate keys | yes | no | yes |
| warnings | yes | yes | yes |
