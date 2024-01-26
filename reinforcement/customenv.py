import sys
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


def close_and_clean_up(conn: connection.Connection):
    conn.send(None)
    conn.close()
    sys.exit()


class MyCustomEnv(gym.Env):

    def __init__(self, conn: connection.Connection):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(1, 100, dtype=np.int32)
        self.conn = conn

    def step(self, action):
        self.conn.send(action - 1)
        obs = np.array([])
        reward = -100
        done = True

        # 1) We exceed timeout = shutdown
        # 2) We receive a faulty combination of values = shutdown
        try:
            if self.conn.poll(timeout=10):
                obs, reward, done = self.conn.recv()
            else:
                raise ValueError("No value received, shutting down...")

            if not isinstance(obs, np.ndarray):
                raise TypeError(f"Expected type np.ndarray for Observations, got type: {type(obs)})")
            elif obs.shape != self.observation_space.shape:
                raise ValueError(f"Expected shape {self.observation_space.shape} for Observations, "
                                 f"instead got shape {obs.shape}")
            elif not isinstance(reward, int):
                raise TypeError(f"Expected type int for Reward, got type: {type(reward)}")
            elif not isinstance(done, bool):
                raise TypeError(f"Expected type bool for Done, got type {type(done)}")
            elif done:
                raise SystemExit("done is True, shutting down...")

        except (ValueError, TypeError, SystemExit) as e:
            print(f"Error encountered: {e}")
            close_and_clean_up(self.conn)

        return obs, reward, done, False, {}

    def reset(self, **kwargs):
        while self.conn.poll():
            self.conn.recv()
        return np.array([1], dtype=np.int32), {}


if __name__ == '__main__':
    conn_1, conn_2 = Pipe()
    env = MyCustomEnv(conn_2)
    check_env(env)
