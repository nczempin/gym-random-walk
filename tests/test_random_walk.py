import gymnasium as gym
import gym_random_walk

_ = gym_random_walk  # ensure environment is registered


def test_reset_start_state():
    env = gym.make("random_walk-v0")
    state, _ = env.reset()
    assert 1 <= state <= 5


def test_episode_terminates_at_terminal_state():
    env = gym.make("random_walk-v0")
    state, _ = env.reset()
    for _ in range(100):
        state, _, terminated, truncated, _ = env.step(env.action_space.sample())
        done = terminated or truncated
        if done:
            break
    assert done, "episode did not terminate in 100 steps"
    assert int(state) in {0, 6}