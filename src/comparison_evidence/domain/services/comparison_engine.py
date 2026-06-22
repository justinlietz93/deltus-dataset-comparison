from __future__ import annotations

from collections import Counter, defaultdict
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Iterable
from uuid import uuid4

from comparison_evidence.domain.exceptions import ContractValidationError
from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.comparison_result import (
    ColumnStat,
    ComparisonResult,
    ComparisonSummary,
    DuplicateKeyWarning,
    EvidenceManifest,
    MissingRow,
    RowDifference,
)
from comparison_evidence.domain.models.schema_profile import SchemaProfile
from comparison_evidence.domain.services.schema_projection import (
    resolve_schema_overlap,
    resolve_type_mismatches,
)

Row = dict[str, Any]


class TabularComparisonEngine:
    def validate_contract(
        self,
        contract: ComparisonContract,
        before_schema: SchemaProfile,
        after_schema: SchemaProfile,
    ) -> tuple[str, ...]:
        messages: list[str] = []
        try:
            contract.require_valid()
        except ValueError as exc:
            messages.extend(str(exc).split("; "))

        before_names = before_schema.names()
        after_names = after_schema.names()
        missing_before_keys = sorted(set(contract.key_columns) - before_names)
        missing_after_keys = sorted(set(contract.key_columns) - after_names)
        if missing_before_keys:
            messages.append(f"Before dataset missing key columns: {missing_before_keys}")
        if missing_after_keys:
            messages.append(f"After dataset missing key columns: {missing_after_keys}")

        missing_excluded = sorted(set(contract.excluded_columns) - (before_names | after_names))
        if missing_excluded:
            messages.append(
                "Excluded columns must exist on at least one side; missing: "
                f"{missing_excluded}"
            )

        return tuple(messages)

    def require_valid_contract(
        self,
        contract: ComparisonContract,
        before_schema: SchemaProfile,
        after_schema: SchemaProfile,
    ) -> None:
        messages = self.validate_contract(contract, before_schema, after_schema)
        if messages:
            raise ContractValidationError(list(messages))

    def compare(
        self,
        contract: ComparisonContract,
        before_schema: SchemaProfile,
        after_schema: SchemaProfile,
        before_rows: Iterable[Row],
        after_rows: Iterable[Row],
        *,
        run_id: str | None = None,
        created_at: datetime | None = None,
    ) -> ComparisonResult:
        self.require_valid_contract(contract, before_schema, after_schema)

        before_list = [dict(row) for row in before_rows]
        after_list = [dict(row) for row in after_rows]
        created = created_at or datetime.now(UTC)
        rid = run_id or f"run_{created.strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"

        schema_overlap = resolve_schema_overlap(
            before_schema,
            after_schema,
            key_columns=contract.key_columns,
            excluded_columns=contract.excluded_columns,
        )
        type_mismatches = resolve_type_mismatches(
            before_schema,
            after_schema,
            tuple(
                column
                for column in schema_overlap.common_columns
                if column not in set(contract.excluded_columns)
            ),
        )

        before_index = _index_rows(before_list, contract.key_columns)
        after_index = _index_rows(after_list, contract.key_columns)
        duplicate_keys = _duplicate_warnings(before_index, "before", contract.key_columns) + _duplicate_warnings(
            after_index, "after", contract.key_columns
        )

        before_keys = set(before_index)
        after_keys = set(after_index)
        common_keys = before_keys & after_keys
        missing_before_keys = sorted(after_keys - before_keys)
        missing_after_keys = sorted(before_keys - after_keys)

        column_counters: dict[str, dict[str, int]] = {
            column: {"compared": 0, "match": 0, "diff": 0}
            for column in schema_overlap.comparable_columns
        }
        detailed: list[RowDifference] = []
        changed_cell_count = 0
        compared_cell_count = 0

        for key in sorted(common_keys):
            before_row = before_index[key][0]
            after_row = after_index[key][0]
            for column in schema_overlap.comparable_columns:
                before_value = _normalize_value(before_row.get(column), contract)
                after_value = _normalize_value(after_row.get(column), contract)
                compared_cell_count += 1
                column_counters[column]["compared"] += 1
                if before_value == after_value:
                    column_counters[column]["match"] += 1
                else:
                    changed_cell_count += 1
                    column_counters[column]["diff"] += 1
                    if len(detailed) < contract.max_detail_rows:
                        detailed.append(
                            RowDifference(
                                key=_key_dict(key, contract.key_columns),
                                column_name=column,
                                before_value=before_row.get(column),
                                after_value=after_row.get(column),
                            )
                        )

        missing_before = tuple(
            MissingRow(key=_key_dict(key, contract.key_columns), side="before", row=after_index[key][0])
            for key in missing_before_keys[: contract.max_detail_rows]
        )
        missing_after = tuple(
            MissingRow(key=_key_dict(key, contract.key_columns), side="after", row=before_index[key][0])
            for key in missing_after_keys[: contract.max_detail_rows]
        )

        warnings: list[str] = []
        if duplicate_keys:
            warnings.append(
                "Duplicate keys detected. Row comparison uses the first row per key; "
                "treat this run as requiring review before using it as final evidence."
            )
        if len(detailed) < changed_cell_count:
            warnings.append(
                f"Detailed differences were capped at max_detail_rows={contract.max_detail_rows}."
            )
        if len(missing_before) < len(missing_before_keys):
            warnings.append("Missing-before rows were capped by max_detail_rows.")
        if len(missing_after) < len(missing_after_keys):
            warnings.append("Missing-after rows were capped by max_detail_rows.")
        if type_mismatches:
            warnings.append("Type mismatches were reported separately and not value-compared.")

        column_stats = tuple(
            ColumnStat(
                column_name=column,
                compared_count=counts["compared"],
                match_count=counts["match"],
                diff_count=counts["diff"],
            )
            for column, counts in sorted(column_counters.items())
        )

        manifest = EvidenceManifest(
            run_id=rid,
            created_at=created,
            tool_name="Deltus Dataset Comparison",
            tool_version="0.1.0",
            before_label=contract.before.label(),
            after_label=contract.after.label(),
            key_columns=contract.key_columns,
            excluded_columns=contract.excluded_columns,
            clear_nulls=contract.clear_nulls,
            numeric_precision=contract.numeric_precision,
            max_detail_rows=contract.max_detail_rows,
        )
        summary = ComparisonSummary(
            before_row_count=len(before_list),
            after_row_count=len(after_list),
            matched_key_count=len(common_keys),
            compared_row_count=len(common_keys),
            missing_before_count=len(missing_before_keys),
            missing_after_count=len(missing_after_keys),
            changed_cell_count=changed_cell_count,
            compared_cell_count=compared_cell_count,
            type_mismatch_count=len(type_mismatches),
            duplicate_key_count=len(duplicate_keys),
            warning_count=len(warnings),
        )
        return ComparisonResult(
            manifest=manifest,
            summary=summary,
            schema_overlap=schema_overlap,
            type_mismatches=type_mismatches,
            column_stats=column_stats,
            detailed_differences=tuple(detailed),
            missing_before=missing_before,
            missing_after=missing_after,
            duplicate_keys=tuple(duplicate_keys),
            warnings=tuple(warnings),
        )


def _index_rows(rows: list[Row], key_columns: tuple[str, ...]) -> dict[tuple[Any, ...], list[Row]]:
    index: dict[tuple[Any, ...], list[Row]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(column) for column in key_columns)
        index[key].append(row)
    return dict(index)


def _duplicate_warnings(
    index: dict[tuple[Any, ...], list[Row]],
    side: str,
    key_columns: tuple[str, ...],
) -> list[DuplicateKeyWarning]:
    warnings: list[DuplicateKeyWarning] = []
    counts = Counter({key: len(rows) for key, rows in index.items()})
    for key, count in sorted(counts.items()):
        if count > 1:
            warnings.append(
                DuplicateKeyWarning(side=side, key=_key_dict(key, key_columns), count=count)
            )
    return warnings


def _key_dict(key: tuple[Any, ...], key_columns: tuple[str, ...]) -> dict[str, Any]:
    return {column: key[index] for index, column in enumerate(key_columns)}


def _normalize_value(value: Any, contract: ComparisonContract) -> Any:
    if contract.clear_nulls and value is None:
        return ""
    if contract.clear_nulls and value == "":
        return ""
    if contract.numeric_precision is not None and _looks_numeric(value):
        return _round_decimal(value, contract.numeric_precision)
    return value


def _looks_numeric(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float, Decimal)):
        return True
    if isinstance(value, str):
        try:
            Decimal(value)
            return True
        except InvalidOperation:
            return False
    return False


def _round_decimal(value: Any, precision: int) -> Decimal:
    quantizer = Decimal("1") if precision == 0 else Decimal("1").scaleb(-precision)
    return Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP)
