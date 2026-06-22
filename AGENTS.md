# Agent Instructions

## Working rule

Preserve the comparison evidence invariant:

> Two datasets may differ in physical shape, but a developer still needs a repeatable before/after proof package.

## Code boundaries

- Keep domain logic free of framework, database, report-renderer, and filesystem dependencies.
- Define or update a port before implementing a new adapter.
- Keep SQL Server behavior inside SQL Server adapters or legacy SQL assets.
- Keep export details inside export adapters.
- Keep frontend concerns out of the application and domain layers.

## Documentation boundaries

- Current truth lives under `docs/pages`.
- Historical SSRS and original workplace context lives under `docs/pages/legacy` or `sql/legacy`.
- Drafts do not become current claims until promoted.
- Generated reports must not be hand-edited.

## Implementation priority

1. Stabilize the result contract.
2. Build fixture-driven tests.
3. Wrap the existing SQL logic safely.
4. Render one useful report.
5. Export XLSX and HTML.
6. Add PDF after the HTML report is stable.

## Avoid

- Rebuilding SSRS/RDL generation.
- Turning the MVP into a universal data platform.
- Letting adapters define the domain language.
- Treating duplicate keys as a minor warning.
- Producing evidence without a manifest.
