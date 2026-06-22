from comparison_evidence.domain.models.comparison_suite_contract import ComparisonSuiteContract
from comparison_evidence.domain.models.dataset_reference import DatasetReference


def test_suite_contract_expands_to_binary_contracts():
    suite = ComparisonSuiteContract(
        suite_name="customer_suite",
        baseline=DatasetReference("sqlite", None, "baseline"),
        candidates=(
            DatasetReference("sqlite", None, "candidate_a"),
            DatasetReference("sqlite", None, "candidate_b"),
        ),
        key_columns=("id",),
        excluded_columns=("batch_id",),
    )

    contracts = suite.comparison_contracts()

    assert len(contracts) == 2
    assert contracts[0].before.object_name == "baseline"
    assert contracts[0].after.object_name == "candidate_a"
    assert contracts[1].after.object_name == "candidate_b"
    assert contracts[0].excluded_columns == ("batch_id",)


def test_suite_contract_requires_candidates():
    suite = ComparisonSuiteContract(
        suite_name="empty_suite",
        baseline=DatasetReference("sqlite", None, "baseline"),
        candidates=(),
        key_columns=("id",),
    )

    try:
        suite.require_valid()
    except ValueError as exc:
        assert "At least one candidate dataset is required" in str(exc)
    else:
        raise AssertionError("Expected suite validation to fail")
