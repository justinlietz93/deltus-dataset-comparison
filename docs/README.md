# Documentation Maintainer Guide

The documentation follows a narrowed Standards-Governed Documentation Architecture.

Current truth belongs under `docs/pages`. Drafts, legacy material, generated outputs, and validation reports must not compete with current docs.

## Main reader paths

- `getting-started`: install and first run
- `user`: comparison workflow and evidence export
- `architecture`: system design and decisions
- `reference`: stable contracts and result schemas
- `development`: implementation plan and testing
- `legacy`: historical SSRS tool context

## Rule

Every claim about implemented behavior must be tied to code, tests, fixture output, a result contract, or a specific legacy artifact.
