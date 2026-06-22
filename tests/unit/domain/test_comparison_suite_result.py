from comparison_evidence.domain.models.comparison_result import (
    ComparisonResult,
    ComparisonSummary,
    EvidenceManifest,
    SchemaOverlap,
)
from comparison_evidence.domain.models.comparison_suite_result import (
    build_candidate_summary,
    build_suite_summary,
)
from datetime import UTC, datetime


def _result(label: str, changed: int, missing_before: int = 0, missing_after: int = 0, warnings=()):
    return ComparisonResult(
        manifest=EvidenceManifest(
            run_id=f"run_{label}",
            created_at=datetime.now(UTC),
            tool_name="Deltus",
            tool_version="test",
            before_label="baseline",
            after_label=label,
            key_columns=("id",),
            excluded_columns=(),
            clear_nulls=True,
            numeric_precision=None,
            max_detail_rows=100,
        ),
        summary=ComparisonSummary(
            before_row_count=2,
            after_row_count=2,
            matched_key_count=2,
            compared_row_count=2,
            missing_before_count=missing_before,
            missing_after_count=missing_after,
            changed_cell_count=changed,
            compared_cell_count=4,
            type_mismatch_count=0,
            duplicate_key_count=0,
            warning_count=len(warnings),
        ),
        schema_overlap=SchemaOverlap(
            common_columns=("id",),
            comparable_columns=(),
            before_only_columns=(),
            after_only_columns=(),
            excluded_columns=(),
            key_columns=("id",),
        ),
        warnings=tuple(warnings),
    )


def test_candidate_status_and_suite_best_candidate():
    pass_summary = build_candidate_summary(_result("candidate_a", changed=0))
    warn_summary = build_candidate_summary(_result("candidate_b", changed=1))
    fail_summary = build_candidate_summary(_result("candidate_c", changed=1, missing_after=1))

    suite_summary = build_suite_summary((warn_summary, fail_summary, pass_summary))

    assert pass_summary.status == "PASS"
    assert warn_summary.status == "WARN"
    assert fail_summary.status == "FAIL"
    assert suite_summary.pass_count == 1
    assert suite_summary.warn_count == 1
    assert suite_summary.fail_count == 1
    assert suite_summary.best_candidate_label == "candidate_a"
