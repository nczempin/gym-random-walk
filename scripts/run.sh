#!/usr/bin/env bash
set -euo pipefail

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run scripts/setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Ensure package is installed in development mode
pip install -e .

# Run code quality checks
echo "Running ruff checks..."
ruff check .

# Run tests
echo "Running tests..."
pytest

# Build the package
echo "Building the package..."
python -m build
