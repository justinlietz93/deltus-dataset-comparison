from __future__ import annotations

import re

_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_safe_identifier(value: str) -> bool:
    return bool(_SAFE_IDENTIFIER.fullmatch(value))


def validate_safe_identifier(value: str, *, label: str = "identifier") -> None:
    if not value or not is_safe_identifier(value):
        raise ValueError(
            f"Unsafe {label}: {value!r}. Use letters, numbers, and underscores only; "
            "the first character must be a letter or underscore."
        )


def quote_sqlserver_identifier(value: str) -> str:
    validate_safe_identifier(value)
    return f"[{value}]"


def qualified_sqlserver_name(schema_name: str | None, object_name: str) -> str:
    if schema_name:
        return f"{quote_sqlserver_identifier(schema_name)}.{quote_sqlserver_identifier(object_name)}"
    return quote_sqlserver_identifier(object_name)
