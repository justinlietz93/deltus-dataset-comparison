from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from tests.conftest import contract

SCHEMA_PATH = Path("docs/contracts/result-package.schema.json")


def test_result_package_matches_documented_contract(fixture_source) -> None:
    result = fixture_source.compare(contract("identical_before", "changed_after"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(result.to_dict())
