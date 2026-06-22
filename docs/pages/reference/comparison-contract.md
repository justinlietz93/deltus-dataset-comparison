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
| `before` | yes | Dataset reference for the before side. |
| `after` | yes | Dataset reference for the after side. |
| `key_columns` | yes | Columns used to align rows. |
| `excluded_columns` | no | Columns ignored during value comparison. |
| `clear_nulls` | no | When true, `NULL` and blank string compare as equivalent. |
| `numeric_precision` | no | Optional decimal places used before numeric comparison. |
| `max_detail_rows` | no | Maximum detailed differences and missing rows to materialize. |

## Dataset reference

A SQL Server dataset reference uses:

- `source_id`
- `schema_name`
- `object_name`
- `display_name`

The MVP restricts identifiers to simple safe names. This prevents accidental unsafe dynamic SQL while the SQL Server adapter is being hardened.

## Projection rule

Different column counts are allowed. The value-comparable projection is:

```text
common columns
  minus excluded columns
  minus key columns
  minus type-mismatched columns
```

Before-only and after-only columns are reported but not value-compared.
