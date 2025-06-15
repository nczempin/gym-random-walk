from setuptools import setup
from setuptools import find_packages

setup(name='gym_random_walk',
      version='0.0.1',
      install_requires=[
          'gym==0.7.4',
          'numpy==1.19.0',
      ],
      python_requires='>=3.7,<3.8',
      url="https://github.com/nczempin/gym-random-walk",
      packages=find_packages()
)  
