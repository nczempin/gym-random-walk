from gym.envs.registration import register
from ._version import __version__

register(
    id='random_walk-v0',
    entry_point='gym_random_walk.envs:RandomWalkEnv',
)

__all__ = ['__version__']
