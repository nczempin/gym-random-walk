# gym-random-walk

A minimal example of a custom environment for [OpenAI Gym](https://github.com/openai/gym).

This environment implements a one-dimensional random walk. The states are `0, 1, ..., 6` with `0` and `6` being terminal. The starting state is chosen uniformly from `1` through `5`.

You can move left or right by selecting a discrete action. Reaching the rightmost terminal yields a reward of `+1` while reaching the leftmost terminal gives a reward of `0`.

## Installation

Install the dependencies using pip:

```bash
pip install -r requirements.txt
=======
## Example

```python
import gym
import gym_random_walk

env = gym.make("random_walk-v0")
state, _ = env.reset()
done = False
while not done:
    state, reward, done, _ = env.step(env.action_space.sample())
```

## Development

Run the linter and tests with:

```bash
bash scripts/run.sh
```
