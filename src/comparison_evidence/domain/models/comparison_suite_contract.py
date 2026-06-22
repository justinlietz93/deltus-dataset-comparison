from __future__ import annotations

from dataclasses import asdict, dataclass

from comparison_evidence.domain.models.comparison_contract import ComparisonContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference
from comparison_evidence.shared.identifiers import validate_safe_identifier


@dataclass(frozen=True)
class ComparisonSuiteContract:
    suite_name: str
    baseline: DatasetReference
    candidates: tuple[DatasetReference, ...]
    key_columns: tuple[str, ...]
    excluded_columns: tuple[str, ...] = ()
    clear_nulls: bool = True
    numeric_precision: int | None = None
    max_detail_rows: int = 10_000

    def require_valid(self) -> None:
        messages: list[str] = []
        try:
            validate_safe_identifier(self.suite_name, label="suite_name")
        except ValueError as exc:
            messages.append(str(exc))
        if not self.candidates:
            messages.append("At least one candidate dataset is required.")
        candidate_labels = [candidate.label() for candidate in self.candidates]
        if len(set(candidate_labels)) != len(candidate_labels):
            messages.append("Candidate dataset labels must be unique within a suite.")
        for index, candidate in enumerate(self.candidates, start=1):
            if candidate == self.baseline:
                messages.append(f"Candidate {index} cannot be the same dataset as the baseline.")
        probe = ComparisonContract(
            before=self.baseline,
            after=self.candidates[0] if self.candidates else self.baseline,
            key_columns=self.key_columns,
            excluded_columns=self.excluded_columns,
            clear_nulls=self.clear_nulls,
            numeric_precision=self.numeric_precision,
            max_detail_rows=self.max_detail_rows,
        )
        try:
            probe.require_valid()
        except ValueError as exc:
            messages.extend(str(exc).split("; "))
        if messages:
            raise ValueError("; ".join(messages))

    def comparison_contracts(self) -> tuple[ComparisonContract, ...]:
        self.require_valid()
        return tuple(
            ComparisonContract(
                before=self.baseline,
                after=candidate,
                key_columns=self.key_columns,
                excluded_columns=self.excluded_columns,
                clear_nulls=self.clear_nulls,
                numeric_precision=self.numeric_precision,
                max_detail_rows=self.max_detail_rows,
            )
            for candidate in self.candidates
        )

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["baseline"] = asdict(self.baseline)
        data["candidates"] = [asdict(candidate) for candidate in self.candidates]
        data["key_columns"] = list(self.key_columns)
        data["excluded_columns"] = list(self.excluded_columns)
        return data
