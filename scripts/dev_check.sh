#!/usr/bin/env bash
set -euo pipefail
python -m pytest
python docs/governance/tools/check_front_matter.py
