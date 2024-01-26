import numpy as np

from multiprocessing import connection, Pipe

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from stable_baselines3 import A2C
from stable_baselines3.common.env_checker import check_env


# Process entry
def training(conn: connection.Connection):
    environment = MyCustomEnv(conn)
    model = A2C("MlpPolicy", environment, verbose=1)
    model.learn(total_timesteps=10_000)


class MyCustomEnv(gym.Env):

    def __init__(self, conn: connection.Connection):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(1, 100, dtype=np.int32)
        self.conn = conn

    def step(self, action):
        self.conn.send(action-1)
        done = True
        if self.conn.poll(timeout=10):
            obs, reward, done = self.conn.recv()

        # More reward calcs?

        if done:
            return None, None, True, True, None

        return obs, reward, done, False, {}

    def reset(self, **kwargs):
        while self.conn.poll():
            self.conn.recv()
        return np.array([1], dtype=np.int32), {}


if __name__ == '__main__':
    conn_1, conn_2 = Pipe()
    env = MyCustomEnv(conn_2)
    check_env(env)