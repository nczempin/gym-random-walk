# gym-random-walk

A minimal example of a custom environment for [Gymnasium](https://github.com/Farama-Foundation/Gymnasium) (formerly OpenAI Gym).

This environment implements a one-dimensional random walk. The states are `0, 1, ..., 6` with `0` and `6` being terminal. The starting state is chosen uniformly from `1` through `5`.

You can move left or right by selecting a discrete action. Reaching the rightmost terminal yields a reward of `+1` while reaching the leftmost terminal gives a reward of `0`.

## Requirements

- **Python 3.8-3.11** (tested with 3.8, 3.9, 3.10, 3.11)
- **Gymnasium 1.0.0** (modern fork of OpenAI Gym)
- **NumPy 1.22.0** (minimum version to address security vulnerabilities)
- **pytest 7.4.4** (for running tests)

This project has been updated to use Gymnasium, the maintained fork of OpenAI Gym. The pinned versions are specified in `requirements.txt`.

## Installation

### Quick Setup (Ubuntu/Debian)

Run the setup script which will install Python 3.11 if needed:

```bash
bash scripts/setup.sh
```

### Manual Installation

1. Ensure you have Python 3.11 installed (3.8-3.11 are all supported)
2. Create a virtual environment:
   ```bash
   python3.11 -m venv venv
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
