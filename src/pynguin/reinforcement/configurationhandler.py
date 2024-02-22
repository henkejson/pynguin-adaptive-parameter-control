import numpy as np

from pynguin.reinforcement.transformationhandlers.abstracttransformationhandler import AbstractTransformationHandler
import pynguin.configuration as config
from pynguin.reinforcement.transformationhandlers.crossovertransformationhandler import CrossoverTransformationHandler


class ConfigurationHandler:

    def __init__(self, normalizers: list[AbstractTransformationHandler]):
        self.normalizers = normalizers

    def apply_actions(self, actions):
        """Apply all actions retrieved to their respective configuration variable, after denormalizing them"""
        print("ACTIONS |",)
        for i, action in enumerate(actions):
            normalizer = self.normalizers[i]

            normalizer.apply_action(action)

            print(f"        | {normalizer.get_name()}: (DN) {round(normalizer.denormalize_action(action), 4)} "
                  f"(N) {round(float(action), 4)}, ",)
        #print("")

    def get_normalized_observations(self, handlers: list[AbstractTransformationHandler] = None):
        """Return a numpy array of all normalized observations"""
        observations = []

        if handlers is None:
            handlers = []

        print("OBSERVATIONS |",)
        for normalizer in handlers + self.normalizers:
            observations.append(normalizer.normalize_observation(normalizer.get_value()))

            print(f"             | {normalizer.get_name()}: (DN) {round(normalizer.get_value(), 4)}, "
                  f"(N) {round(normalizer.normalize_observation(normalizer.get_value()), 4)}",)
        #print("")

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
