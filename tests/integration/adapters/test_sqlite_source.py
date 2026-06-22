from __future__ import annotations

from pathlib import Path

from comparison_evidence.adapters.driven.sqlite import SqliteDatasetSource
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference

SQLITE_FIXTURE = Path("tests/fixtures/mvp_cases.sqlite")


def ref(object_name: str) -> DatasetReference:
    return DatasetReference(source_id="sqlite", schema_name=None, object_name=object_name)


def contract(before: str, after: str, **kwargs) -> ComparisonContract:
    return ComparisonContract(
        before=ref(before),
        after=ref(after),
        key_columns=kwargs.get("key_columns", ("id",)),
        excluded_columns=kwargs.get("excluded_columns", ()),
        clear_nulls=kwargs.get("clear_nulls", True),
        numeric_precision=kwargs.get("numeric_precision"),
        max_detail_rows=kwargs.get("max_detail_rows", 10_000),
    )


def test_sqlite_source_lists_and_inspects_tables() -> None:
    source = SqliteDatasetSource(SQLITE_FIXTURE)

    tables = source.list_tables("sqlite")
    assert any(table.object_name == "identical_before" for table in tables)

    schema = source.inspect_schema(ref("identical_before"))
    assert schema.names() == {"id", "name", "amount", "load_date"}


def test_sqlite_source_compares_changed_value() -> None:
    source = SqliteDatasetSource(SQLITE_FIXTURE)

    result = source.compare(contract("identical_before", "changed_after"))

    assert result.summary.changed_cell_count == 1
    assert result.detailed_differences[0].key == {"id": 2}
    assert result.detailed_differences[0].column_name == "amount"
    assert result.summary.missing_before_count == 0
    assert result.summary.missing_after_count == 0


def test_sqlite_source_compares_different_column_counts() -> None:
    source = SqliteDatasetSource(SQLITE_FIXTURE)

    result = source.compare(contract("different_columns_before", "different_columns_after"))

    assert result.schema_overlap.before_only_columns == ("only_before",)
    assert result.schema_overlap.after_only_columns == ("only_after",)
    assert result.schema_overlap.comparable_columns == ("amount", "name")
    assert result.summary.changed_cell_count == 0


def test_sqlite_source_reports_duplicate_keys() -> None:
    source = SqliteDatasetSource(SQLITE_FIXTURE)

    result = source.compare(contract("duplicate_before", "duplicate_after"))

    assert result.summary.duplicate_key_count == 1
    assert result.duplicate_keys[0].side == "before"
    assert "Duplicate keys detected" in result.warnings[0]


def test_sqlite_row_limit_keeps_adapter_bounded() -> None:
    source = SqliteDatasetSource(SQLITE_FIXTURE, row_limit=1)

    result = source.compare(contract("identical_before", "identical_after"))

    assert result.summary.before_row_count == 1
    assert result.summary.after_row_count == 1
    assert result.summary.compared_row_count == 1
