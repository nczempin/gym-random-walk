import gymnasium as gym
from gymnasium import spaces
from typing import Optional, Dict, Tuple, Any

class RandomWalkEnv(gym.Env):
    """Simple random walk environment."""

    metadata = {"render_modes": ["human"]}

    def __init__(self, size=6, debug=False, render_mode=None):
        super().__init__()
        self.size = size
        self.debug = debug
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(self.size + 1)
        self.state = None

    def step(self, action) -> Tuple[int, float, bool, bool, Dict[str, Any]]:
        reward = 0
        terminated = False
        truncated = False
        
        if action == 0:
            self.state -= 1
        if action == 1:
            self.state += 1
            
        if self.state >= self.size:
            reward = 1
            terminated = True
        if self.state <= 0:
            terminated = True
            
        if self.debug:
            print("current state:", self.state)
            
        # Render if mode is set
        if self.render_mode == "human":
            self.render()
            
        # Return the new Gymnasium API format (5 values)
        return self.state, reward, terminated, truncated, {}

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[int, Dict]:
        # Properly handle seeding in Gymnasium
        super().reset(seed=seed)
        
        if self.debug:
            print("#self.size:", self.size)
            
        # Use the environment's random number generator
        self.state = self.np_random.integers(1, self.size)
        
        if self.debug:
            print("starting:", self.state)
            
        # Return observation and info dict
        return self.state, {}

    def render(self):
        if self.render_mode == "human" or self.debug:
            print("current state:", self.state)