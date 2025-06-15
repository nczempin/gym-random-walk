#!/usr/bin/env bash
set -euo pipefail

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

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

# Check for Python 3.11
echo "Checking for Python 3.11..."
if command_exists python3.11; then
    PYTHON_CMD=python3.11
    echo -e "${GREEN}Found Python 3.11${NC}"
elif command_exists python3; then
    # Check if it's 3.11.x
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    if [[ $PYTHON_VERSION == 3.11.* ]]; then
        PYTHON_CMD=python3
        echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"
    else
        echo -e "${YELLOW}Python 3 found but version is $PYTHON_VERSION${NC}"
        echo -e "${YELLOW}This project recommends Python 3.11${NC}"
        
        if [ "$IS_DEBIAN_BASED" = true ]; then
            echo "Installing Python 3.11..."
            sudo apt-get update
            # Add deadsnakes PPA for Python versions
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
            PYTHON_CMD=python3.11
        else
            echo -e "${RED}Please install Python 3.11 manually and run this script again.${NC}"
            echo -e "${RED}This project recommends Python 3.11${NC}"
            exit 1
        fi
    fi
else
    echo "Python 3.11 is not installed."
    if [ "$IS_DEBIAN_BASED" = true ]; then
        echo "Installing Python 3.11..."
        sudo apt-get update
        sudo apt-get install -y software-properties-common
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
        PYTHON_CMD=python3.11
    else
        echo -e "${RED}Please install Python 3.11 manually and run this script again.${NC}"
        exit 1
    fi
fi

# Check for pip for Python 3.11
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    echo "pip for Python 3.11 is not installed."
    if [ "$IS_DEBIAN_BASED" = true ]; then
        echo "Installing pip for Python 3.11..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        sudo $PYTHON_CMD get-pip.py
        rm get-pip.py
    else
        echo -e "${RED}Please install pip for Python 3.11 manually and run this script again.${NC}"
        exit 1
    fi
fi

# Remove existing venv if it exists (to ensure we use Python 3.11)
if [ -d "venv" ]; then
    echo -e "${YELLOW}Removing existing virtual environment to recreate with Python 3.11...${NC}"
    rm -rf venv
fi

# Create virtual environment with Python 3.11
echo "Creating virtual environment with Python 3.11..."
$PYTHON_CMD -m venv venv

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

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${GREEN}Python version in venv: $(python --version)${NC}"
echo -e "${GREEN}To activate the virtual environment, run: source venv/bin/activate${NC}"
echo -e "${GREEN}To deactivate it later, run: deactivate${NC}"