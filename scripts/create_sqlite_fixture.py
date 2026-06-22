from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from comparison_evidence.shared.identifiers import validate_safe_identifier


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a SQLite fixture database from a Deltus fixture JSON file.")
    parser.add_argument("--fixture", default="tests/fixtures/mvp_cases.json")
    parser.add_argument("--database", default="tests/fixtures/mvp_cases.sqlite")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    database_path = Path(args.database)
    if args.replace and database_path.exists():
        database_path.unlink()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    with sqlite3.connect(database_path) as connection:
        for dataset in data["datasets"]:
            _write_dataset(connection, dataset)
    print(database_path)
    return 0


def _write_dataset(connection: sqlite3.Connection, dataset: dict[str, Any]) -> None:
    table = _quote(dataset["object_name"])
    columns = dataset["columns"]
    column_defs = ", ".join(
        f"{_quote(column['name'])} {column.get('data_type') or 'text'}"
        for column in columns
    )
    connection.execute(f"DROP TABLE IF EXISTS {table}")
    connection.execute(f"CREATE TABLE {table} ({column_defs})")
    if not dataset.get("rows"):
        return
    names = [column["name"] for column in columns]
    quoted_names = ", ".join(_quote(name) for name in names)
    placeholders = ", ".join("?" for _ in names)
    values = [tuple(row.get(name) for name in names) for row in dataset["rows"]]
    connection.executemany(
        f"INSERT INTO {table} ({quoted_names}) VALUES ({placeholders})",
        values,
    )


def _quote(value: str) -> str:
    validate_safe_identifier(value, label="sqlite_identifier")
    return f'"{value}"'


if __name__ == "__main__":
    raise SystemExit(main())
