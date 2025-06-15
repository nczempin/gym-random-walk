import numpy as np
import pytest

gym = pytest.importorskip("gym")
import gym_random_walk


def test_random_walk_step():
    env = gym.make("random_walk-v0")
    try:
        obs = env.reset()
        state = getattr(env, "state", None)
        assert state is not None
        assert 1 <= state <= env.size - 1

        obs, reward, done, _ = env.step(1)
        obs_val = int(obs)
        assert 0 <= obs_val <= env.size
        assert reward in (0, 1)
        # done could be True or False depending on the initial state
    finally:
        env.close()
