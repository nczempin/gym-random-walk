pip install -e .[dev]

ruff check .
pytest

python -m build
