import sys
from multiprocessing import connection, Pipe

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from stable_baselines3 import A2C
from stable_baselines3.common.env_checker import check_env

from reinforcement.MutableBool import MutableBool
from reinforcement.StoppingCallback import StoppingCallback


# Process entry
def training(conn: connection.Connection):
    stop_training = MutableBool(False)
    callback = StoppingCallback(stop_training)
    environment = MyCustomEnv(conn, stop_training)
    model = A2C("MlpPolicy", environment, verbose=1)
    model.learn(total_timesteps=10_000, callback=callback)
    print("Saving model...")


def close_and_clean_up(conn: connection.Connection):
    conn.send(None)
    conn.close()
    sys.exit()


class MyCustomEnv(gym.Env):

    def __init__(self, conn: connection.Connection, stop_training: MutableBool):
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)  # Crossover rate
        self.observation_space = spaces.Box(low=-1, high=1, dtype=np.float32)  # Crossover rate

        self.conn = conn
        self.stop_training = stop_training
        self.coverage_history = [0.0]

    def step(self, action):
        self.conn.send(action)
        obs = np.array([])
        coverage = 0.0
        reward = 0.0
        done = True

        try:
            obs, coverage, done = self.get_observations()

        except (ValueError, TypeError, SystemExit) as e:
            print(f"Error encountered: {e}")
            close_and_clean_up(self.conn)

        # Add the latest coverage value to the history
        self.coverage_history.append(coverage)

        # Calculate reward from the coverage
        # Scale reward to give more as it approaches 1?
        if len(self.coverage_history) >= 2:
            reward = max(0.0, (self.coverage_history[-1] - self.coverage_history[-2])) * (
                    2 / (1 + np.exp(-9 * (self.coverage_history[-1] - 0.5))))
            # Scale the reward
            reward *= 100

        print(f"Normalized observations: {obs}")  # TODO probably remove at some point
        print(f"Reward: {reward}")  # TODO probably remove at some point

        return obs, reward, done, False, {}

    def get_observations(self):

        if self.conn.poll(timeout=60):
            obs, coverage, done = self.conn.recv()
        else:
            raise ValueError("No value received, shutting down...")

        if done:
            self.stop_training.set(True)
            print("Stop training signal received...")
            return None, 0.0, True

        elif not isinstance(obs, np.ndarray):
            raise TypeError(f"Expected type np.ndarray for Observations, got type: {type(obs)})")
        elif obs.shape != self.observation_space.shape:
            raise ValueError(f"Expected shape {self.observation_space.shape} for Observations, "
                             f"instead got shape {obs.shape}")
        elif not isinstance(coverage, float):
            raise TypeError(f"Expected type int for Coverage, got type: {type(coverage)}")
        elif not isinstance(done, bool):
            raise TypeError(f"Expected type bool for Done, got type {type(done)}")

        return obs, coverage, done

    def reset(self, **kwargs):
        while self.conn.poll():
            self.conn.recv()
        return np.array([1], dtype=np.int32), {}
