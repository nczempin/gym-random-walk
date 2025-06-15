#!/usr/bin/env bash
set -euo pipefail

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if running on Ubuntu/Debian-based system
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" == "ubuntu" ]] || [[ "$ID_LIKE" == *"debian"* ]]; then
        IS_DEBIAN_BASED=true
    else
        IS_DEBIAN_BASED=false
    fi
else
    IS_DEBIAN_BASED=false
fi

# Check and install Python3 if not present
if ! command_exists python3; then
    echo "Python3 not found. Installing Python3..."
    if [ "$IS_DEBIAN_BASED" = true ]; then
        sudo apt-get update
        sudo apt-get install -y python3
    else
        echo "Please install Python3 manually for your system"
        exit 1
    fi
fi

# Check and install pip if not present
if ! command_exists pip3 && ! command_exists pip; then
    echo "pip not found. Installing pip..."
    if [ "$IS_DEBIAN_BASED" = true ]; then
        sudo apt-get install -y python3-pip
    else
        echo "Please install pip manually for your system"
        exit 1
    fi
fi

# Check if python3-venv is installed (required for creating virtual environments)
if ! python3 -m venv --help &> /dev/null; then
    echo "python3-venv not found. Installing python3-venv..."
    if [ "$IS_DEBIAN_BASED" = true ]; then
        sudo apt-get install -y python3-venv
    else
        echo "Please install python3-venv manually for your system"
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
pip install ruff pytest build

# Install the package in development mode
echo "Installing gym-random-walk in development mode..."
pip install -e .

echo "Setup complete! Virtual environment is activated."
echo "To activate the virtual environment manually, run: source venv/bin/activate"