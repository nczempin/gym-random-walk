import pytest

gym = pytest.importorskip("gymnasium")

# Import gym_random_walk to register the environment
import gym_random_walk  # noqa: E402, F401


def test_random_walk_step():
    env = gym.make("random_walk-v0")
    try:
        obs, _ = env.reset()
        # Access the unwrapped environment to get internal state
        unwrapped_env = env.unwrapped
        state = getattr(unwrapped_env, "state", None)
        assert state is not None
        assert 1 <= state <= unwrapped_env.size - 1

        obs, reward, terminated, truncated, _ = env.step(1)
        obs_val = int(obs)
        assert 0 <= obs_val <= unwrapped_env.size
        assert reward in (0, 1)
        # done could be True or False depending on the initial state
    finally:
        env.close()