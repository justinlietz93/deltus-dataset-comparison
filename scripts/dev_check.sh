#!/usr/bin/env bash
set -euo pipefail

python -m pytest
python docs/governance/tools/check_front_matter.py

if python -m ruff --version >/dev/null 2>&1; then
  python -m ruff format --check src tests
  python -m ruff check src tests
else
  echo "ruff not installed; skipping formatting and lint checks"
fi

if python -m mypy --version >/dev/null 2>&1; then
  python -m mypy src
else
  echo "mypy not installed; skipping type checks"
fi
