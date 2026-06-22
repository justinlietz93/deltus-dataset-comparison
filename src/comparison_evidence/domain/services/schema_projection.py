from __future__ import annotations

from comparison_evidence.domain.models.comparison_result import SchemaOverlap, TypeMismatch
from comparison_evidence.domain.models.schema_profile import SchemaProfile


def resolve_common_columns(
    before: SchemaProfile,
    after: SchemaProfile,
    excluded_columns: tuple[str, ...] = (),
) -> tuple[str, ...]:
    excluded = set(excluded_columns)
    common = before.names().intersection(after.names())
    return tuple(sorted(common - excluded))


def resolve_only_before_columns(before: SchemaProfile, after: SchemaProfile) -> tuple[str, ...]:
    return tuple(sorted(before.names() - after.names()))


def resolve_only_after_columns(before: SchemaProfile, after: SchemaProfile) -> tuple[str, ...]:
    return tuple(sorted(after.names() - before.names()))


def resolve_type_mismatches(
    before: SchemaProfile,
    after: SchemaProfile,
    columns: tuple[str, ...],
) -> tuple[TypeMismatch, ...]:
    before_map = before.column_map()
    after_map = after.column_map()
    mismatches: list[TypeMismatch] = []
    for column in columns:
        before_column = before_map[column]
        after_column = after_map[column]
        if before_column.normalized_type() != after_column.normalized_type():
            mismatches.append(
                TypeMismatch(
                    column_name=column,
                    before_type=before_column.data_type,
                    after_type=after_column.data_type,
                )
            )
    return tuple(mismatches)


def resolve_schema_overlap(
    before: SchemaProfile,
    after: SchemaProfile,
    *,
    key_columns: tuple[str, ...],
    excluded_columns: tuple[str, ...] = (),
) -> SchemaOverlap:
    common = resolve_common_columns(before, after, excluded_columns=())
    common_after_exclusions = resolve_common_columns(before, after, excluded_columns=excluded_columns)
    type_mismatches = resolve_type_mismatches(before, after, common_after_exclusions)
    mismatched = {item.column_name for item in type_mismatches}
    comparable = tuple(
        sorted(set(common_after_exclusions) - set(key_columns) - mismatched)
    )
    return SchemaOverlap(
        common_columns=tuple(sorted(common)),
        comparable_columns=comparable,
        before_only_columns=resolve_only_before_columns(before, after),
        after_only_columns=resolve_only_after_columns(before, after),
        excluded_columns=tuple(sorted(excluded_columns)),
        key_columns=tuple(key_columns),
    )
