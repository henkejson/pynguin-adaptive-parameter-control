import sys
from multiprocessing import connection

import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO

from pynguin.reinforcement.mutablebool import MutableBool
from pynguin.reinforcement.stoppingcallback import StoppingCallback


# Process entry
def training(n_action: int, n_observations: int, conn: connection.Connection):
    stop_training = MutableBool(False)
    callback = StoppingCallback(stop_training)

    environment = APOEnvironment(n_action, n_observations, conn, stop_training)
    model = PPO("MlpPolicy", environment, verbose=1)
    model.learn(total_timesteps=10_000, callback=callback)
    print("Saving model...")


def close_and_clean_up(conn: connection.Connection):
    conn.send(None)
    conn.close()
    sys.exit()


class APOEnvironment(gym.Env):

    def __init__(self, n_action: int, n_observations: int, conn: connection.Connection, stop_training: MutableBool):
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(n_action,), dtype=np.float32)  # Crossover rate
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(n_observations,), dtype=np.float32)  # Crossover rate

        self.conn = conn
        self.stop_training = stop_training
        self.coverage_history = [0.0]

    def step(self, action):
        self.conn.send(action)
        obs = np.array([])
        reward = 0.0
        done = True

        try:
            obs, reward, done = self.get_observations()

        except (ValueError, TypeError, SystemExit) as e:
            print(f"Error encountered: {e}")
            close_and_clean_up(self.conn)

        return obs, reward, done, False, {}

    def get_observations(self):
        cont = False
        while not cont:
            if self.conn.poll(timeout=120):
                obs, reward, cont, done = self.conn.recv()
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
        elif not isinstance(reward, float):
            raise TypeError(f"Expected type float for Reward, got type: {type(reward)}")
        elif not isinstance(done, bool):
            raise TypeError(f"Expected type bool for Done, got type {type(done)}")

        return obs, reward, done

    def reset(self, **kwargs):
        while self.conn.poll():
            self.conn.recv()
        return np.array([1], dtype=np.int32), {}
