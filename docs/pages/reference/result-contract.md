---
title: "Result Contract"
status: current
authority: canonical
---

# Result Contract

Every comparison run produces the same logical sections regardless of source adapter.

## Required sections

- run manifest
- summary
- schema overlap
- type mismatches
- column stats
- detailed differences
- missing before
- missing after
- warnings

## Export mapping

| Section | HTML | XLSX | CSV | JSON |
|---|---:|---:|---:|---:|
| run manifest | yes | yes | no | yes |
| summary | yes | yes | no | yes |
| schema overlap | yes | yes | yes | yes |
| type mismatches | yes | yes | yes | yes |
| column stats | yes | yes | yes | yes |
| detailed differences | yes | yes | yes | yes |
| missing before | yes | yes | yes | yes |
| missing after | yes | yes | yes | yes |
| warnings | yes | yes | no | yes |
