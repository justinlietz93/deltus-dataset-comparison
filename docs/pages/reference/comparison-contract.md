---
title: "Comparison Contract"
status: current
authority: canonical
---

# Comparison Contract

The comparison contract is the input authority for a run.

## Fields

| Field | Required | Meaning |
|---|---:|---|
| `before` | yes | Dataset reference for the before side |
| `after` | yes | Dataset reference for the after side |
| `key_columns` | yes | Columns used to align rows |
| `excluded_columns` | no | Common columns ignored during value comparison |
| `clear_nulls` | no | Treat null/blank according to adapter policy |
| `numeric_precision` | no | Optional numeric rounding precision |
| `max_detail_rows` | no | Maximum detailed differences to materialize |

## Rule

Different column counts are allowed. The comparable value projection is the intersection of common columns minus excluded columns and key columns.
