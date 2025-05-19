#!/usr/bin/env bash
set -euo pipefail

pip install -e .

ruff check .
pytest

python -m build
