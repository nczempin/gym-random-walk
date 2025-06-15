"""Test the example code from README.md to ensure it works correctly."""
import gym
import gym_random_walk

_ = gym_random_walk  # ensure environment is registered


def test_readme_example_runs():
    """Test that the example code from README.md runs without errors."""
    env = gym.make("random_walk-v0")
    state = env.reset()
    done = False
    
    # Run for a maximum of 100 steps to ensure test doesn't run forever
    steps = 0
    max_steps = 100
    
    while not done and steps < max_steps:
        state, reward, done, _ = env.step(env.action_space.sample())
        steps += 1
        
        # Verify state is within valid range
        assert 0 <= state <= env.size
        
        # Verify reward is correct based on terminal state
        if done:
            if state == env.size:
                assert reward == 1
            elif state == 0:
                assert reward == 0
    
    # Ensure the episode terminated
    assert done, "Episode should have terminated within 100 steps"


def test_readme_example_multiple_episodes():
    """Test running multiple episodes as one might do in practice."""
    env = gym.make("random_walk-v0")
    
    total_rewards = []
    num_episodes = 10
    
    for _ in range(num_episodes):
        state = env.reset()
        done = False
        episode_reward = 0
        steps = 0
        
        while not done and steps < 100:
            state, reward, done, _ = env.step(env.action_space.sample())
            episode_reward += reward
            steps += 1
        
        total_rewards.append(episode_reward)
    
    # Verify we collected rewards from all episodes
    assert len(total_rewards) == num_episodes
    
    # Verify all rewards are either 0 or 1 (only possible rewards)
    assert all(r in [0, 1] for r in total_rewards)
    
    # With random actions, we should get some successes and some failures
    # across 10 episodes (this could theoretically fail but is unlikely)
    assert any(r == 1 for r in total_rewards), "Should have at least one success"
    assert any(r == 0 for r in total_rewards), "Should have at least one failure"