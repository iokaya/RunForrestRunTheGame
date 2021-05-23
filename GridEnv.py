import gym
from gym import spaces


class GridEnv(gym.Env):
    def __init__(self, envArray):
        super(self).__init__()
        self.envArray = envArray
        self.originalState = envArray
        self.action_space = spaces.Box()

