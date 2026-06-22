---
title: "Testing"
status: current
authority: canonical
---

# Testing

## Test layers

- Unit tests for domain projection rules.
- Contract tests for result shape and adapter behavior.
- SQL fixture tests for stored procedure behavior.
- Export golden tests for HTML/XLSX/CSV/JSON packages.
- End-to-end test for one complete comparison run.

## First fixture cases

1. same schema, one changed value
2. different column counts
3. excluded column ignored
4. missing before row
5. missing after row
6. mismatched data type
7. duplicate key warning
8. null handling
9. numeric precision handling
