from __future__ import annotations

from pathlib import Path

from comparison_evidence.adapters.driven.local_files import FixtureDatasetSource
from comparison_evidence.domain.models.dataset_reference import DatasetReference


def test_fixture_source_lists_and_inspects_tables() -> None:
    source = FixtureDatasetSource.from_json_file(Path("tests/fixtures/mvp_cases.json"))

    tables = source.list_tables("fixture")
    assert any(table.object_name == "identical_before" for table in tables)

    schema = source.inspect_schema(
        DatasetReference(source_id="fixture", schema_name="dbo", object_name="identical_before")
    )
    assert schema.names() == {"id", "name", "amount", "load_date"}
