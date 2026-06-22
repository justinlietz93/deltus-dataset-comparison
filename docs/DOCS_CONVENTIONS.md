# Docs Conventions

## Page front matter

Use this on non-trivial pages:

```yaml
---
title: "Page Title"
status: current
owner: docs
authority: canonical
---
```

## Status values

- `current`: implemented and supported
- `planned`: accepted but not implemented
- `experimental`: implemented but unstable
- `draft`: work in progress
- `legacy`: historical context
- `archived`: retained but not current

## Evidence wording

Use exact status labels:

- Implemented
- Planned
- Legacy behavior
- Inferred from legacy artifact
- To be verified

Do not use production claims until backed by tests or fixture output.
