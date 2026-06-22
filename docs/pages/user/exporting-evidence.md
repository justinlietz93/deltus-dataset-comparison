---
title: "Exporting Evidence"
status: current
authority: canonical
---

# Exporting Evidence

The MVP replaces the old SSRS export surface with a local evidence package.

## Generated files

Every completed run writes a deterministic run folder under the configured export root.

Required JSON sections:

- `result.json`
- `manifest.json`
- `summary.json`
- `schema_overlap.json`
- `type_mismatches.json`
- `column_stats.json`
- `detailed_differences.json`
- `missing_before.json`
- `missing_after.json`
- `duplicate_keys.json`
- `warnings.json`

Required human-review artifacts:

- `report.html`
- `report.xlsx`

## Ticket evidence use

Attach `report.html` when reviewers need a readable snapshot. Attach `report.xlsx` when reviewers need sortable tables. Keep `manifest.json` with the evidence when the run settings need to be audited.

## Later export

PDF export should be generated from the same HTML report after the HTML layout is stable.
