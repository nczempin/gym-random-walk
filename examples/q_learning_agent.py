"""
Simple Q-Learning Agent for Random Walk Environment

This example demonstrates how to train a Q-learning agent on the gym-random-walk environment.
Q-learning is a model-free reinforcement learning algorithm that learns the value of actions
in different states to find the optimal policy.

Key concepts:
- Q-table: Stores estimated values Q(s,a) for each state-action pair
- Epsilon-greedy: Balances exploration (trying new actions) vs exploitation (using known good actions)
- Temporal Difference Learning: Updates Q-values based on immediate reward and future expected value
"""

import gymnasium as gym
import numpy as np
import argparse
import gym_random_walk  # noqa: F401 - Register the environment

# Try to import matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not installed. Visualization will be skipped.")
    print("Install with: pip install matplotlib")


def epsilon_greedy_action(q_table, state, epsilon, n_actions):
    """
    Select action using epsilon-greedy strategy.
    
    With probability epsilon: explore (random action)
    With probability 1-epsilon: exploit (best known action)
    """
    if np.random.random() < epsilon:
        return np.random.randint(n_actions)
    else:
        return np.argmax(q_table[state])


def train_q_learning(env, n_episodes=500, learning_rate=0.1, discount_factor=0.95,
                     initial_epsilon=1.0, final_epsilon=0.01, verbose=True):
    """
    Train a Q-learning agent on the environment.
    
    Parameters:
    - n_episodes: Number of training episodes
    - learning_rate (α): How much to update Q-values each step
    - discount_factor (γ): How much to value future rewards vs immediate rewards
    - initial_epsilon: Starting exploration rate
    - final_epsilon: Final exploration rate
    - verbose: Print progress during training
    """
    # Initialize Q-table with zeros
    # Shape: (n_states, n_actions) = (7, 2) for random walk
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q_table = np.zeros((n_states, n_actions))
    
    # Track rewards for each episode
    episode_rewards = []
    
    # Calculate epsilon decay rate
    epsilon_decay = (initial_epsilon - final_epsilon) / n_episodes
    epsilon = initial_epsilon
    
    for episode in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            # Select action using epsilon-greedy
            action = epsilon_greedy_action(q_table, state, epsilon, n_actions)
            
            # Take action and observe result
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            # Q-learning update rule:
            # Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
            # This is the temporal difference (TD) error
            td_target = reward + discount_factor * np.max(q_table[next_state]) * (not done)
            td_error = td_target - q_table[state, action]
            q_table[state, action] += learning_rate * td_error
            
            state = next_state
            total_reward += reward
        
        episode_rewards.append(total_reward)
        
        # Decay epsilon
        epsilon = max(final_epsilon, epsilon - epsilon_decay)
        
        # Print progress
        if verbose and (episode + 1) % 50 == 0:
            avg_reward = np.mean(episode_rewards[-50:])
            print(f"Episode {episode + 1}/{n_episodes} - "
                  f"Average Reward (last 50): {avg_reward:.3f} - "
                  f"Epsilon: {epsilon:.3f}")
    
    return q_table, episode_rewards


def print_policy(q_table):
    """
    Print the learned policy (best action for each state).
    """
    print("\nLearned Policy:")
    print("State -> Action (0=left, 1=right)")
    print("-" * 30)
    
    for state in range(len(q_table)):
        if state == 0:
            print(f"State {state}: Terminal (left)")
        elif state == len(q_table) - 1:
            print(f"State {state}: Terminal (right/goal)")
        else:
            best_action = np.argmax(q_table[state])
            action_name = "left" if best_action == 0 else "right"
            q_values = q_table[state]
            print(f"State {state}: {action_name} (Q-values: {q_values})")


def plot_learning_curve(episode_rewards, save_path=None):
    """
    Plot the learning curve showing rewards over episodes.
    """
    if not MATPLOTLIB_AVAILABLE:
        print("\nCannot plot learning curve - matplotlib not installed")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Plot raw rewards
    plt.plot(episode_rewards, alpha=0.3, label='Episode rewards')
    
    # Plot moving average
    window_size = 50
    if len(episode_rewards) >= window_size:
        moving_avg = np.convolve(episode_rewards, np.ones(window_size)/window_size, mode='valid')
        plt.plot(range(window_size-1, len(episode_rewards)), moving_avg, 
                label=f'{window_size}-episode moving average', linewidth=2)
    
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Q-Learning Performance on Random Walk Environment')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")
    else:
        plt.show()


def test_trained_agent(env, q_table, n_episodes=10):
    """
    Test the trained agent using the learned Q-table (no exploration).
    """
    print(f"\nTesting trained agent for {n_episodes} episodes...")
    total_rewards = []
    
    for episode in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False
        steps = 0
        
        while not done and steps < 20:  # Prevent infinite loops
            # Always take the best action (no exploration)
            action = np.argmax(q_table[state])
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            total_reward += reward
            steps += 1
        
        total_rewards.append(total_reward)
    
    print(f"Test Results: Average reward = {np.mean(total_rewards):.3f}")
    print(f"Success rate: {sum(r > 0 for r in total_rewards) / n_episodes * 100:.1f}%")


def main():
    parser = argparse.ArgumentParser(description='Train Q-learning agent on Random Walk')
    parser.add_argument('--episodes', type=int, default=500,
                       help='Number of training episodes (default: 500)')
    parser.add_argument('--lr', type=float, default=0.1,
                       help='Learning rate (default: 0.1)')
    parser.add_argument('--gamma', type=float, default=0.95,
                       help='Discount factor (default: 0.95)')
    parser.add_argument('--save-plot', type=str, default=None,
                       help='Path to save learning curve plot')
    parser.add_argument('--no-plot', action='store_true',
                       help='Disable plotting')
    
    args = parser.parse_args()
    
    # Create environment
    env = gym.make('random_walk-v0')
    
    print(f"Training Q-Learning agent for {args.episodes} episodes...")
    print("Environment: Random Walk (states: 0-6, actions: 0=left, 1=right)")
    print("Goal: Reach state 6 (rightmost) for reward of +1")
    print("-" * 50)
    
    # Train agent
    q_table, episode_rewards = train_q_learning(
        env, 
        n_episodes=args.episodes,
        learning_rate=args.lr,
        discount_factor=args.gamma
    )
    
    # Print final Q-table
    print("\nFinal Q-table:")
    print(q_table)
    
    # Print learned policy
    print_policy(q_table)
    
    # Test trained agent
    test_trained_agent(env, q_table)
    
    # Plot learning curve
    if not args.no_plot:
        plot_learning_curve(episode_rewards, args.save_plot)
    
    env.close()


if __name__ == "__main__":
    main()