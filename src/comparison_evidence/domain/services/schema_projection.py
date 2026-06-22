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
