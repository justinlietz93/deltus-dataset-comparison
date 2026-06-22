# Copy Legacy Assets

Suggested first migration step:

```bash
mkdir -p sql/legacy/ssrs sql/legacy/stored_procedures sql/legacy/functions
cp /path/to/old/*.sql sql/legacy/stored_procedures/
cp /path/to/old/*.rdl sql/legacy/ssrs/
cp /path/to/old/report_definition*.json sql/legacy/ssrs/
```

After copying, document what each legacy artifact owns in `docs/pages/legacy/original-ssrs-tool.md`.
