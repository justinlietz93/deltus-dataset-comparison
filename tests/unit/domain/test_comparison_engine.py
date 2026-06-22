from __future__ import annotations

import json
from pathlib import Path

import pytest

from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference

from tests.conftest import contract

EXPECTED = json.loads((Path(__file__).parents[2] / "fixtures" / "expected_summaries.json").read_text())


def assert_summary(result, expected_key: str) -> None:
    expected = EXPECTED[expected_key]
    data = result.to_dict()["summary"]
    for key, value in expected.items():
        assert data[key] == value


def test_identical_tables_have_no_differences(fixture_source) -> None:
    result = fixture_source.compare(contract("identical_before", "identical_after"))

    assert_summary(result, "identical")
    assert result.summary.compared_cell_count == 6
    assert result.cell_match_percent == 100.0


def test_one_changed_value_is_reported(fixture_source) -> None:
    result = fixture_source.compare(contract("identical_before", "changed_after"))

    assert_summary(result, "one_changed_value")
    assert result.detailed_differences[0].key == {"id": 2}
    assert result.detailed_differences[0].column_name == "amount"


def test_different_column_counts_compare_shared_projection(fixture_source) -> None:
    result = fixture_source.compare(contract("different_columns_before", "different_columns_after"))

    assert_summary(result, "different_column_counts")
    assert result.schema_overlap.before_only_columns == ("only_before",)
    assert result.schema_overlap.after_only_columns == ("only_after",)
    assert result.schema_overlap.comparable_columns == ("amount", "name")


def test_excluded_column_change_is_ignored(fixture_source) -> None:
    result = fixture_source.compare(
        contract("identical_before", "excluded_after", excluded_columns=("load_date",))
    )

    assert_summary(result, "excluded_column_changed")
    assert "load_date" not in result.schema_overlap.comparable_columns


def test_missing_before_rows_are_reported(fixture_source) -> None:
    result = fixture_source.compare(contract("identical_before", "missing_before_after"))

    assert_summary(result, "missing_before")
    assert result.missing_before[0].key == {"id": 3}


def test_missing_after_rows_are_reported(fixture_source) -> None:
    result = fixture_source.compare(contract("missing_before_after", "missing_after_before"))

    assert_summary(result, "missing_after")
    assert result.missing_after[0].key == {"id": 3}


def test_mismatched_types_are_reported_not_value_compared(fixture_source) -> None:
    result = fixture_source.compare(contract("identical_before", "type_mismatch_after"))

    assert_summary(result, "mismatched_type")
    assert result.type_mismatches[0].column_name == "amount"
    assert "amount" not in result.schema_overlap.comparable_columns


def test_duplicate_key_is_a_hard_warning(fixture_source) -> None:
    result = fixture_source.compare(contract("duplicate_before", "duplicate_after"))

    assert_summary(result, "duplicate_key")
    assert result.duplicate_keys[0].side == "before"
    assert "Duplicate keys detected" in result.warnings[0]


def test_null_and_empty_are_equal_when_clear_nulls_is_enabled(fixture_source) -> None:
    result = fixture_source.compare(contract("null_before", "empty_after", clear_nulls=True))

    assert_summary(result, "null_vs_empty_clear")


def test_null_and_empty_are_different_when_clear_nulls_is_disabled(fixture_source) -> None:
    result = fixture_source.compare(contract("null_before", "empty_after", clear_nulls=False))

    assert_summary(result, "null_vs_empty_strict")


def test_numeric_precision_can_normalize_small_decimal_noise(fixture_source) -> None:
    result = fixture_source.compare(
        contract("precision_before", "precision_after", numeric_precision=2)
    )

    assert_summary(result, "numeric_precision")


def test_key_validation_rejects_missing_key(fixture_source) -> None:
    bad_contract = contract("identical_before", "identical_after", key_columns=("missing_id",))

    messages = fixture_source.validate_contract(bad_contract)

    assert "Before dataset missing key columns: ['missing_id']" in messages
    assert "After dataset missing key columns: ['missing_id']" in messages


def test_exclusion_validation_rejects_unknown_excluded_column(fixture_source) -> None:
    bad_contract = contract(
        "identical_before",
        "identical_after",
        excluded_columns=("does_not_exist",),
    )

    messages = fixture_source.validate_contract(bad_contract)

    assert "Excluded columns must exist on at least one side; missing: ['does_not_exist']" in messages


def test_unsafe_identifiers_are_rejected() -> None:
    with pytest.raises(ValueError):
        DatasetReference(source_id="fixture", schema_name="dbo", object_name="bad;drop")

    with pytest.raises(ValueError):
        ComparisonContract(
            before=DatasetReference(source_id="fixture", schema_name="dbo", object_name="a"),
            after=DatasetReference(source_id="fixture", schema_name="dbo", object_name="b"),
            key_columns=("bad column",),
        ).require_valid()
