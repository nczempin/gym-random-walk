# gym-random-walk

A minimal example of a custom environment for [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) (formerly OpenAI Gym).

## What is a Random Walk Environment?

This environment implements a one-dimensional random walk, which is one of the simplest possible reinforcement learning (RL) environments. Think of it as a game where an agent stands on a number line and can only move left or right:

```
Terminal ← 0 - 1 - 2 - 3 - 4 - 5 - 6 → Terminal (Goal)
```

The agent starts at a random position between 1 and 5, and must learn to reach the goal (position 6) to get a reward.

### Why is this useful for learning RL?

1. **Simplicity**: With only 7 states and 2 actions, it's easy to visualize and understand what's happening
2. **Quick to train**: Agents can learn the optimal policy in just a few episodes
3. **Easy to debug**: You can print out every step and see exactly what your algorithm is doing
4. **Benchmarking**: Great for testing if your RL implementation works correctly before moving to complex environments
5. **Educational**: Perfect for tutorials and learning the basics of RL concepts like:
   - States and actions
   - Rewards and episodes
   - Value functions and policies
   - Exploration vs exploitation

## Environment Details

- **States**: `0, 1, ..., 6` with `0` and `6` being terminal states
- **Actions**: 0 (move left) or 1 (move right)
- **Starting position**: Randomly chosen from states 1 through 5
- **Rewards**: +1 for reaching state 6 (goal), 0 for reaching state 0
- **Episode termination**: When the agent reaches either terminal state (0 or 6)

## Requirements

- **Python 3.9-3.12** (recommended: 3.12, tested with 3.9, 3.10, 3.11, 3.12)
- **Gymnasium 1.0.0** (modern fork of OpenAI Gym)
- **NumPy 1.26.4** (minimum version for Python 3.12 support)
- **pytest 7.4.4** (for running tests)

This project has been updated to use Gymnasium, the maintained fork of OpenAI Gym. The pinned versions are specified in `requirements.txt`.

## Installation

### Quick Setup (Ubuntu/Debian)

Run the setup script which will install Python 3.12 if needed:

```bash
bash scripts/setup.sh
```

### Manual Installation

1. Ensure you have Python 3.12 installed (3.9-3.12 are all supported)
2. Create a virtual environment:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
## Example

```python
import gymnasium as gym
import gym_random_walk

env = gym.make("random_walk-v0")
state, info = env.reset()
done = False
while not done:
    state, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated
```

## Development

Run the linter and tests with:

```bash
bash scripts/run.sh
```
