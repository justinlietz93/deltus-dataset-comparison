from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from comparison_evidence.domain.models.comparison_result import ComparisonResult


class HtmlReportExporter:
    artifact_name = "report.html"

    def export(self, result: ComparisonResult, output_dir: str) -> str:
        path = Path(output_dir) / self.artifact_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_html_report(result), encoding="utf-8")
        return str(path)


def render_html_report(result: ComparisonResult) -> str:
    summary = result.summary
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Deltus Evidence Report - {escape(result.run_id)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #172033; }}
    h1, h2 {{ margin-bottom: 0.35rem; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; }}
    .card {{ border: 1px solid #d5dae6; border-radius: 10px; padding: 0.85rem; background: #fbfcff; }}
    .label {{ color: #5f6b7a; font-size: 0.82rem; }}
    .value {{ font-size: 1.35rem; font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; margin: 0.75rem 0 1.5rem; }}
    th, td {{ border: 1px solid #d5dae6; padding: 0.45rem 0.55rem; text-align: left; vertical-align: top; }}
    th {{ background: #eef2f8; }}
    .warning {{ border-left: 4px solid #a66a00; background: #fff8e8; padding: 0.65rem 0.85rem; margin: 0.4rem 0; }}
    code {{ background: #eef2f8; padding: 0.1rem 0.25rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Deltus Evidence Report</h1>
  <p><strong>Run:</strong> <code>{escape(result.run_id)}</code><br />
     <strong>Created:</strong> {escape(result.created_at.isoformat())}<br />
     <strong>Before:</strong> {escape(result.manifest.before_label)}<br />
     <strong>After:</strong> {escape(result.manifest.after_label)}</p>

  <h2>Summary</h2>
  <div class="cards">
    {_card('Before rows', summary.before_row_count)}
    {_card('After rows', summary.after_row_count)}
    {_card('Matched keys', summary.matched_key_count)}
    {_card('Missing before', summary.missing_before_count)}
    {_card('Missing after', summary.missing_after_count)}
    {_card('Changed cells', summary.changed_cell_count)}
    {_card('Compared cells', summary.compared_cell_count)}
    {_card('Cell match %', f'{summary.cell_match_percent:.2f}%')}
  </div>

  <h2>Warnings</h2>
  {_warnings(result.warnings)}

  <h2>Schema Overlap</h2>
  {_schema_table(result)}

  <h2>Type Mismatches</h2>
  {_table(['Column', 'Before Type', 'After Type'], [[m.column_name, m.before_type, m.after_type] for m in result.type_mismatches])}

  <h2>Column Stats</h2>
  {_table(['Column', 'Compared', 'Matches', 'Differences', 'Match %'], [[s.column_name, s.compared_count, s.match_count, s.diff_count, f'{s.match_percent:.2f}%'] for s in result.column_stats])}

  <h2>Detailed Differences</h2>
  {_table(['Key', 'Column', 'Before', 'After'], [[d.key, d.column_name, d.before_value, d.after_value] for d in result.detailed_differences])}

  <h2>Missing Before</h2>
  {_table(['Key', 'Row'], [[r.key, r.row] for r in result.missing_before])}

  <h2>Missing After</h2>
  {_table(['Key', 'Row'], [[r.key, r.row] for r in result.missing_after])}

  <h2>Duplicate Keys</h2>
  {_table(['Side', 'Key', 'Count'], [[d.side, d.key, d.count] for d in result.duplicate_keys])}
</body>
</html>
"""


def _card(label: str, value: Any) -> str:
    return f'<div class="card"><div class="label">{escape(str(label))}</div><div class="value">{escape(str(value))}</div></div>'


def _warnings(warnings: tuple[str, ...]) -> str:
    if not warnings:
        return "<p>No warnings.</p>"
    return "\n".join(f'<div class="warning">{escape(warning)}</div>' for warning in warnings)


def _schema_table(result: ComparisonResult) -> str:
    overlap = result.schema_overlap
    rows = [
        ["Key columns", ", ".join(overlap.key_columns)],
        ["Common columns", ", ".join(overlap.common_columns)],
        ["Comparable columns", ", ".join(overlap.comparable_columns)],
        ["Before-only columns", ", ".join(overlap.before_only_columns)],
        ["After-only columns", ", ".join(overlap.after_only_columns)],
        ["Excluded columns", ", ".join(overlap.excluded_columns)],
    ]
    return _table(["Section", "Columns"], rows)


def _table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "<p>No rows.</p>"
    head = "".join(f"<th>{escape(str(header))}</th>" for header in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{escape(_format_cell(cell))}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def _format_cell(value: Any) -> str:
    if isinstance(value, dict):
        return ", ".join(f"{k}={v}" for k, v in value.items())
    return "" if value is None else str(value)
