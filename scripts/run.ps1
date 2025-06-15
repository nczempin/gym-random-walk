pip install -e .

ruff check .
pytest

python -m build
