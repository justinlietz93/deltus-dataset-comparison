# Docs Architecture

## Published source

`docs/pages` is the canonical published tree.

## Authority classes

- `canonical`: current source of truth
- `generated`: produced by code or tests
- `draft`: not authoritative
- `legacy`: historical source material
- `archive`: historical docs not treated as current

## Project-specific rule

The original SSRS report and SQL assets are evidence and source material. They are not the modern architecture boundary.

The modern architecture boundary is the comparison result contract.
