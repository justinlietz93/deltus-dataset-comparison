# TODO: `0.3.x` Report Reader and Export Wave

## Purpose

Move from technically correct evidence output to a polished report-reading experience that recovers the practical value of the old SSRS report without depending on SSRS.

## Version intent

- `0.3.0`: usable web report reader and clean XLSX/HTML exports.
- `0.3.1+`: PDF export, formatting polish, and ticket-evidence presentation.

## Definition of Done

- [ ] A developer can open a completed run in a browser and understand pass/fail risk quickly.
- [ ] HTML and XLSX exports are clean enough to attach to a ticket.
- [ ] PDF export exists and preserves the important report sections.
- [ ] Warning states are visually obvious.
- [ ] Large detailed-difference sections remain navigable.

---

## Phase 1: Report information design

### Task 1.1: Define report page hierarchy

- [ ] Step 1.1.1: Create report landing summary.
- [ ] Step 1.1.2: Create schema section.
- [ ] Step 1.1.3: Create mismatch/type section.
- [ ] Step 1.1.4: Create column-stat section.
- [ ] Step 1.1.5: Create detailed-difference section.
- [ ] Step 1.1.6: Create missing-row section.
- [ ] Step 1.1.7: Create manifest/audit section.

### Task 1.2: Define evidence severity rules

- [ ] Step 1.2.1: Define clean comparison state.
- [ ] Step 1.2.2: Define warning state.
- [ ] Step 1.2.3: Define failure state.
- [ ] Step 1.2.4: Define duplicate-key state.
- [ ] Step 1.2.5: Define partial-result state.
- [ ] Step 1.2.6: Display severity in every export.

---

## Phase 2: Web report reader

### Task 2.1: Build run viewer shell

- [ ] Step 2.1.1: Route for run list.
- [ ] Step 2.1.2: Route for run detail.
- [ ] Step 2.1.3: Fetch result package from backend.
- [ ] Step 2.1.4: Add loading state.
- [ ] Step 2.1.5: Add error state.

### Task 2.2: Build report sections

- [ ] Step 2.2.1: Summary cards.
- [ ] Step 2.2.2: Source table metadata.
- [ ] Step 2.2.3: Key and exclusion display.
- [ ] Step 2.2.4: Schema overlap table.
- [ ] Step 2.2.5: Type mismatch table.
- [ ] Step 2.2.6: Column stats table.
- [ ] Step 2.2.7: Detailed differences table.
- [ ] Step 2.2.8: Missing rows tables.
- [ ] Step 2.2.9: Warnings panel.

### Task 2.3: Add navigation and filtering

- [ ] Step 2.3.1: Add section anchors.
- [ ] Step 2.3.2: Add table search.
- [ ] Step 2.3.3: Add changed-only filters.
- [ ] Step 2.3.4: Add warning-only filters.
- [ ] Step 2.3.5: Add large-table pagination.

---

## Phase 3: XLSX export polish

### Task 3.1: Workbook structure

- [ ] Step 3.1.1: Summary sheet first.
- [ ] Step 3.1.2: Manifest sheet last.
- [ ] Step 3.1.3: Freeze headers.
- [ ] Step 3.1.4: Auto-size columns where practical.
- [ ] Step 3.1.5: Use consistent section names.

### Task 3.2: Evidence usability

- [ ] Step 3.2.1: Add run timestamp.
- [ ] Step 3.2.2: Add source and target identifiers.
- [ ] Step 3.2.3: Add comparison options.
- [ ] Step 3.2.4: Add warning count.
- [ ] Step 3.2.5: Add result counts to sheet headers.
- [ ] Step 3.2.6: Add README sheet explaining how to read the workbook.

---

## Phase 4: HTML and PDF export polish

### Task 4.1: HTML export

- [ ] Step 4.1.1: Render standalone HTML with embedded summary data.
- [ ] Step 4.1.2: Add print-friendly styling.
- [ ] Step 4.1.3: Add table overflow handling.
- [ ] Step 4.1.4: Add section links.
- [ ] Step 4.1.5: Add evidence footer with run ID and generated timestamp.

### Task 4.2: PDF export

- [ ] Step 4.2.1: Generate PDF from stable HTML.
- [ ] Step 4.2.2: Add page headers and footers.
- [ ] Step 4.2.3: Keep summary and warnings near front.
- [ ] Step 4.2.4: Truncate or appendix large detail sections intentionally.
- [ ] Step 4.2.5: Document PDF limitations.

---

## Phase 5: Release `0.3.x`

### Task 5.1: Report QA

- [ ] Step 5.1.1: Generate report for every fixture.
- [ ] Step 5.1.2: Review HTML manually.
- [ ] Step 5.1.3: Review XLSX manually.
- [ ] Step 5.1.4: Review PDF manually.
- [ ] Step 5.1.5: Save sample artifacts under generated docs or release assets.

### Task 5.2: Ship release

- [ ] Step 5.2.1: Update screenshots or report examples.
- [ ] Step 5.2.2: Update user workflow docs.
- [ ] Step 5.2.3: Update release notes.
- [ ] Step 5.2.4: Tag `v0.3.0`.
