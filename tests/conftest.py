from __future__ import annotations

from pathlib import Path

import pytest

from comparison_evidence.adapters.driven.local_files import FixtureDatasetSource
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "mvp_cases.json"


@pytest.fixture()
def fixture_source() -> FixtureDatasetSource:
    return FixtureDatasetSource.from_json_file(FIXTURE_PATH)


def ref(object_name: str) -> DatasetReference:
    return DatasetReference(source_id="fixture", schema_name="dbo", object_name=object_name)


def contract(
    before: str,
    after: str,
    *,
    key_columns: tuple[str, ...] = ("id",),
    excluded_columns: tuple[str, ...] = (),
    clear_nulls: bool = True,
    numeric_precision: int | None = None,
    max_detail_rows: int = 10_000,
) -> ComparisonContract:
    return ComparisonContract(
        before=ref(before),
        after=ref(after),
        key_columns=key_columns,
        excluded_columns=excluded_columns,
        clear_nulls=clear_nulls,
        numeric_precision=numeric_precision,
        max_detail_rows=max_detail_rows,
    )
