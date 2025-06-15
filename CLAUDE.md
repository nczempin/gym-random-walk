# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal custom environment for OpenAI Gym implementing a one-dimensional random walk. The environment features configurable state space with terminal states at both ends, binary actions (left/right), and simple reward structure.

## Requirements

- Python 3.8 (required for numpy 1.22.0 security updates)
- Dependencies: gym==0.7.4, numpy==1.22.0, pytest==7.4.4

## Commands

### Setup and Installation
```bash
# Run the setup script (installs Python 3.6 if needed on Ubuntu)
bash scripts/setup.sh

# Or manually:
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Development Commands
```bash
# Run complete test suite with linting (recommended)
bash scripts/run.sh

# Run linter only
ruff check .

# Run tests only
pytest

# Run a single test
pytest tests/test_random_walk.py::test_function_name

# Build the package
python -m build
```

## Architecture

### Package Structure
The project follows standard Python package conventions with OpenAI Gym environment registration:

- **gym_random_walk/__init__.py**: Registers the environment with Gym using `register()` function
- **gym_random_walk/envs/random_walk_env.py**: Core environment implementation inheriting from `gym.Env`
- **tests/**: Pytest-based test suite
- **examples/**: Example usage scripts

### Core Environment Design
The `RandomWalkEnv` class implements:
- Configurable size parameter (default: 6)
- Discrete action and observation spaces
- Terminal states at positions 0 and size
- Random initialization between terminal states
- Debug mode for verbose output

### Key Implementation Details
- States: 0 to size (inclusive), with 0 and size as terminal states
- Actions: 0 (left), 1 (right)
- Rewards: +1 for reaching rightmost terminal, 0 for leftmost
- The environment follows OpenAI Gym's standard API: `step()`, `reset()`, `render()`

## Testing Approach
- Uses pytest framework
- Tests cover environment initialization, step mechanics, terminal conditions, and reward structure
- Includes test for README example code to ensure documentation stays accurate
- Run `scripts/run.sh` before committing to ensure linting and tests pass