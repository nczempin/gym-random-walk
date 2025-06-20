from setuptools import setup
from setuptools import find_packages
import os
import sys

# Add the package directory to sys.path so we can import _version
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gym_random_walk'))

from _version import __version__, PYTHON_REQUIRES, GYMNASIUM_VERSION, NUMPY_VERSION  # noqa: E402

setup(name='gym_random_walk',
      version=__version__,
      install_requires=[
          f'gymnasium=={GYMNASIUM_VERSION}',
          f'numpy=={NUMPY_VERSION}',
      ],
      python_requires=PYTHON_REQUIRES,
      url="https://github.com/nczempin/gym-random-walk",
      packages=find_packages()
)  
