# gym-random-walk

A minimal example of a custom environment for [OpenAI Gym](https://github.com/openai/gym).

This environment implements a one-dimensional random walk. The states are `0, 1, ..., 6` with `0` and `6` being terminal. The starting state is chosen uniformly from `1` through `5`.

You can move left or right by selecting a discrete action. Reaching the rightmost terminal yields a reward of `+1` while reaching the leftmost terminal gives a reward of `0`.

## Requirements

- **Python 3.8** (required for numpy 1.22.0)
- **OpenAI Gym 0.7.4** (original version from 2017)
- **NumPy 1.22.0** (minimum version to address security vulnerabilities)
- **pytest 7.4.4** (for running tests)

This project uses older versions of dependencies to maintain compatibility with the original codebase from 2017. The pinned versions are specified in `requirements.txt`.

## Installation

### Quick Setup (Ubuntu/Debian)

Run the setup script which will install Python 3.8 if needed:

```bash
bash scripts/setup.sh
```

### Manual Installation

1. Ensure you have Python 3.8 installed
2. Create a virtual environment:
   ```bash
   python3.8 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
## Example

```python
import gym
import gym_random_walk

env = gym.make("random_walk-v0")
state = env.reset()
done = False
while not done:
    state, reward, done, _ = env.step(env.action_space.sample())
```

## Development

Run the linter and tests with:

```bash
bash scripts/run.sh
```
