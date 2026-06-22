from comparison_evidence.domain.models.schema_profile import ColumnProfile, SchemaProfile
from comparison_evidence.domain.services.schema_projection import (
    resolve_common_columns,
    resolve_only_after_columns,
    resolve_only_before_columns,
)


def profile(label: str, names: list[str]) -> SchemaProfile:
    return SchemaProfile(
        dataset_label=label,
        columns=tuple(
            ColumnProfile(name=name, data_type="varchar", nullable=True, ordinal=i)
            for i, name in enumerate(names)
        ),
    )


def test_resolves_common_columns_with_exclusions() -> None:
    before = profile("before", ["id", "name", "load_date", "only_before"])
    after = profile("after", ["id", "name", "load_date", "only_after"])

    assert resolve_common_columns(before, after, excluded_columns=("load_date",)) == ("id", "name")


def test_resolves_one_sided_columns() -> None:
    before = profile("before", ["id", "only_before"])
    after = profile("after", ["id", "only_after"])

    assert resolve_only_before_columns(before, after) == ("only_before",)
    assert resolve_only_after_columns(before, after) == ("only_after",)
