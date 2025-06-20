#!/usr/bin/env bash
set -euo pipefail

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Python version configuration
PYTHON_VERSION="3.12"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run scripts/setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Verify Python version in venv
VENV_PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
if [[ ! $VENV_PYTHON_VERSION == ${PYTHON_VERSION}.* ]]; then
    echo "Warning: Virtual environment has Python $VENV_PYTHON_VERSION but project recommends Python ${PYTHON_VERSION}"
    echo "Consider running scripts/setup.sh to recreate the virtual environment with Python ${PYTHON_VERSION}"
fi

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
