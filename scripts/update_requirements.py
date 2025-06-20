#!/usr/bin/env python3
"""Generate requirements.txt from version definitions."""

import sys
import os

# Add gym_random_walk directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gym_random_walk'))

from _version import GYMNASIUM_VERSION, PYTEST_VERSION, NUMPY_VERSION, MATPLOTLIB_VERSION, RUFF_VERSION  # noqa: E402

# Generate requirements.txt content
requirements = f"""gymnasium=={GYMNASIUM_VERSION}
pytest=={PYTEST_VERSION}
numpy=={NUMPY_VERSION}
matplotlib=={MATPLOTLIB_VERSION}
ruff=={RUFF_VERSION}
"""

# Write to requirements.txt
with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("Updated requirements.txt with versions from gym_random_walk/_version.py")