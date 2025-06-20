"""
Tests for the Q-learning example script.

Ensures the example runs correctly and learns the optimal policy.
"""

import numpy as np
import subprocess
import sys
import os
import gymnasium as gym

# Add parent directory to path to import the example
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

from q_learning_agent import train_q_learning, epsilon_greedy_action, print_policy  # noqa: E402


def test_epsilon_greedy_action():
    """Test epsilon-greedy action selection."""
    # Create a simple Q-table
    q_table = np.array([[0.0, 1.0],  # State 0: action 1 is better
                        [2.0, 0.0]])  # State 1: action 0 is better
    
    # Test with epsilon=0 (always exploit)
    action = epsilon_greedy_action(q_table, state=0, epsilon=0.0, n_actions=2)
    assert action == 1  # Should pick action with highest Q-value
    
    action = epsilon_greedy_action(q_table, state=1, epsilon=0.0, n_actions=2)
    assert action == 0
    
    # Test with epsilon=1 (always explore)
    # Should return valid actions but random
    actions = []
    for _ in range(100):
        action = epsilon_greedy_action(q_table, state=0, epsilon=1.0, n_actions=2)
        actions.append(action)
        assert action in [0, 1]
    
    # With many samples, should have both actions
    assert 0 in actions and 1 in actions


def test_q_learning_convergence():
    """Test that Q-learning converges to optimal policy."""
    env = gym.make('random_walk-v0')
    
    # Train with enough episodes to converge
    q_table, rewards = train_q_learning(
        env, 
        n_episodes=300,
        learning_rate=0.1,
        discount_factor=0.95,
        initial_epsilon=1.0,
        final_epsilon=0.01,
        verbose=False
    )
    
    # Check Q-table has correct shape
    assert q_table.shape == (7, 2)  # 7 states, 2 actions
    
    # Check that agent learned to go right for non-terminal states
    # Optimal policy: always go right (action 1) except in terminal states
    for state in range(1, 6):  # States 1-5 (non-terminal)
        best_action = np.argmax(q_table[state])
        assert best_action == 1, f"State {state} should prefer right action"
    
    # Terminal states should have zero Q-values
    assert np.allclose(q_table[0], 0.0), "Left terminal state should have zero Q-values"
    assert np.allclose(q_table[6], 0.0), "Right terminal state should have zero Q-values"
    
    # Check that later episodes have higher average reward
    early_avg = np.mean(rewards[:50])
    late_avg = np.mean(rewards[-50:])
    assert late_avg > early_avg, "Agent should improve over time"
    
    # Late episodes should mostly succeed (reward > 0)
    success_rate = sum(r > 0 for r in rewards[-50:]) / 50
    assert success_rate > 0.8, "Agent should succeed in most late episodes"


def test_q_learning_with_different_parameters():
    """Test Q-learning with various hyperparameters."""
    env = gym.make('random_walk-v0')
    
    # Test with high learning rate
    q_table, _ = train_q_learning(
        env, 
        n_episodes=100,
        learning_rate=0.9,
        discount_factor=0.5,
        verbose=False
    )
    assert q_table.shape == (7, 2)
    
    # Test with low discount factor (myopic agent)
    q_table, _ = train_q_learning(
        env, 
        n_episodes=100,
        learning_rate=0.1,
        discount_factor=0.1,
        verbose=False
    )
    assert q_table.shape == (7, 2)


def test_example_script_runs():
    """Test that the example script runs without errors."""
    example_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'q_learning_agent.py')
    
    # Run with minimal episodes and no plotting
    result = subprocess.run(
        [sys.executable, example_path, '--episodes', '50', '--no-plot'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert "Training Q-Learning agent" in result.stdout
    assert "Episode 50/50" in result.stdout
    assert "Learned Policy:" in result.stdout
    assert "Test Results:" in result.stdout


def test_example_script_help():
    """Test that the example script shows help."""
    example_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'q_learning_agent.py')
    
    result = subprocess.run(
        [sys.executable, example_path, '--help'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert "Train Q-learning agent on Random Walk" in result.stdout
    assert "--episodes" in result.stdout
    assert "--lr" in result.stdout
    assert "--gamma" in result.stdout


def test_print_policy(capsys):
    """Test policy printing function."""
    # Create a simple Q-table where action 1 (right) is always better
    q_table = np.array([
        [0.0, 0.0],      # State 0 (terminal)
        [0.1, 0.9],      # State 1 -> right
        [0.2, 0.8],      # State 2 -> right
        [0.3, 0.7],      # State 3 -> right
        [0.4, 0.6],      # State 4 -> right
        [0.4, 0.7],      # State 5 -> right
        [0.0, 0.0],      # State 6 (terminal)
    ])
    
    print_policy(q_table)
    
    captured = capsys.readouterr()
    assert "Learned Policy:" in captured.out
    assert "State 0: Terminal (left)" in captured.out
    assert "State 6: Terminal (right/goal)" in captured.out
    
    # Check that states 1-5 all choose right
    for state in range(1, 6):
        assert f"State {state}: right" in captured.out