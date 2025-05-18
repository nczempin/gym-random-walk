#!/usr/bin/env bash
set -euo pipefail

pip install -e .[dev]

ruff check .
pytest

python -m build
