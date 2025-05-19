import gym
from gym import spaces
import numpy as np

class RandomWalkEnv(gym.Env):
    """Simple random walk environment."""

    metadata = {"render.modes": ["human"]}

    def __init__(self, size: int = 6, debug: bool = False) -> None:
        super().__init__()
        self.size = size
        self.debug = debug
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(self.size + 1)
        self.state = None

    def step(self, action):
        reward = 0
        done = False
        if action == 0:
            self.state -= 1
        if action == 1:
            self.state += 1
        if self.state >= self.size:
            reward = 1
            done = True
        if self.state <= 0:
            done = True
        if self.debug:
            print("current state:", self.state)
        return np.array(self.state), reward, done, {}

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        if self.debug:
            print("#self.size:", self.size)
        self.state = np.random.randint(1, self.size - 1)
        if self.debug:
            print("starting:", self.state)
        return np.array(self.state), {}

    def render(self, mode: str = "human"):
        if not self.debug:
            return
        print("current state:", self.state)
