import numpy as np

from reinforcement.abstracttransformationhandler import AbstractTransformationHandler
import pynguin.configuration as config
from reinforcement.crossovertransformationhandler import CrossoverTransformationHandler


class ConfigurationHandler:

    def __init__(self, normalizers: list[AbstractTransformationHandler]):
        self.normalizers = normalizers

    def apply_actions(self, actions):
        """Apply all actions retrieved to their respective configuration variable, after denormalizing them"""
        print("ACTIONS | ", end="")
        for i, action in enumerate(actions):
            normalizer = self.normalizers[i]

            normalizer.apply_action(action)

            print(f"{normalizer.get_name()}: {normalizer.denormalize_action(action)}, ", end="")
        print("")

    def get_normalized_observations(self):
        """Return a numpy array of all normalized observations"""
        observations = []

        print("OBSERVATIONS | ", end="")
        for normalizer in self.normalizers:
            observations.append(normalizer.normalize_observation(normalizer.get_value()))

            print(f"{normalizer.get_name()}: {normalizer.get_value()}, ", end="")
        print("")

        return np.array(observations, dtype=np.float32)


if __name__ == '__main__':
    print(f"Before:  {config.configuration.search_algorithm.crossover_rate}")
    a = ConfigurationHandler([CrossoverTransformationHandler(-0.05, 0.05)])
    a.apply_actions([-1])
    print(f"Normalized observations: {a.get_normalized_observations()}")
    print(f"After:  {config.configuration.search_algorithm.crossover_rate}")

    print(f"Before 2:  {config.configuration.search_algorithm.crossover_rate}")
    a = ConfigurationHandler([CrossoverTransformationHandler(-0.05, 0.05)])
    a.apply_actions([1])
    print(f"Normalized observations: {a.get_normalized_observations()}")
    print(f"After 2:  {config.configuration.search_algorithm.crossover_rate}")
