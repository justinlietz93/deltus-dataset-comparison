from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from comparison_evidence.adapters.driven.export.html_exporter import HtmlReportExporter
from comparison_evidence.domain.models.comparison_suite_result import ComparisonSuiteResult


class HtmlSuiteReportExporter:
    artifact_name = "suite_report.html"

    def export(self, suite_result: ComparisonSuiteResult, output_dir: str) -> str:
        path = Path(output_dir) / self.artifact_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_html_suite_report(suite_result), encoding="utf-8")
        comparison_exporter = HtmlReportExporter()
        for result in suite_result.results:
            comparison_exporter.export(result, path.parent / "comparisons" / _safe_segment(result.manifest.after_label))
        return str(path)


def render_html_suite_report(suite_result: ComparisonSuiteResult) -> str:
    summary = suite_result.summary
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Deltus Suite Report - {escape(suite_result.suite_id)}</title>
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
    .PASS {{ color: #116329; font-weight: 700; }}
    .WARN {{ color: #8a5a00; font-weight: 700; }}
    .FAIL {{ color: #9b1c1c; font-weight: 700; }}
    code {{ background: #eef2f8; padding: 0.1rem 0.25rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Deltus Comparison Suite Report</h1>
  <p><strong>Suite:</strong> {escape(suite_result.manifest.suite_name)}<br />
     <strong>Suite ID:</strong> <code>{escape(suite_result.suite_id)}</code><br />
     <strong>Created:</strong> {escape(suite_result.created_at.isoformat())}<br />
     <strong>Baseline:</strong> {escape(suite_result.manifest.baseline_label)}<br />
     <strong>Keys:</strong> {escape(', '.join(suite_result.manifest.key_columns))}</p>

  <h2>Suite Summary</h2>
  <div class="cards">
    {_card('Candidates', summary.candidate_count)}
    {_card('Pass', summary.pass_count)}
    {_card('Warn', summary.warn_count)}
    {_card('Fail', summary.fail_count)}
    {_card('Changed cells', summary.total_changed_cell_count)}
    {_card('Missing before', summary.total_missing_before_count)}
    {_card('Missing after', summary.total_missing_after_count)}
    {_card('Best candidate', summary.best_candidate_label or 'n/a')}
  </div>

  <h2>Warnings</h2>
  {_warnings(suite_result.warnings)}

  <h2>Candidate Results</h2>
  {_candidate_table(suite_result)}
</body>
</html>
"""


def _card(label: str, value: Any) -> str:
    return f'<div class="card"><div class="label">{escape(str(label))}</div><div class="value">{escape(str(value))}</div></div>'


def _warnings(warnings: tuple[str, ...]) -> str:
    if not warnings:
        return "<p>No suite warnings.</p>"
    return "\n".join(f'<div class="warning">{escape(warning)}</div>' for warning in warnings)


def _candidate_table(suite_result: ComparisonSuiteResult) -> str:
    if not suite_result.candidate_summaries:
        return "<p>No candidate rows.</p>"
    rows = []
    for item in suite_result.candidate_summaries:
        detail_path = f"comparisons/{escape(_safe_segment(item.candidate_label))}/report.html"
        rows.append(
            "<tr>"
            f"<td>{escape(item.candidate_label)}</td>"
            f"<td class=\"{escape(item.status)}\">{escape(item.status)}</td>"
            f"<td>{item.difference_score}</td>"
            f"<td>{item.changed_cell_count}</td>"
            f"<td>{item.missing_before_count}</td>"
            f"<td>{item.missing_after_count}</td>"
            f"<td>{item.type_mismatch_count}</td>"
            f"<td>{item.duplicate_key_count}</td>"
            f"<td>{item.warning_count}</td>"
            f"<td>{item.cell_match_percent:.2f}%</td>"
            f"<td><a href=\"{detail_path}\">details</a></td>"
            "</tr>"
        )
    head = "".join(
        f"<th>{escape(header)}</th>"
        for header in [
            "Candidate",
            "Status",
            "Score",
            "Changed Cells",
            "Missing Before",
            "Missing After",
            "Type Mismatches",
            "Duplicate Keys",
            "Warnings",
            "Cell Match %",
            "Report",
        ]
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def _safe_segment(value: str) -> str:
    safe = "".join(character if character.isalnum() or character in "_-" else "_" for character in value)
    return safe.strip("_") or "candidate"
