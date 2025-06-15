#!/usr/bin/env python3
"""Generate requirements.txt from version definitions."""

import sys
import os

# Add gym_random_walk directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gym_random_walk'))
from _version import GYM_VERSION, PYTEST_VERSION, NUMPY_VERSION

# Generate requirements.txt content
requirements = f"""gym=={GYM_VERSION}
pytest=={PYTEST_VERSION}
numpy=={NUMPY_VERSION}
"""

# Write to requirements.txt
with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("Updated requirements.txt with versions from gym_random_walk/_version.py")