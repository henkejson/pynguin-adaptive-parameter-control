import numpy as np

from reinforcement.crossovertransformationhandler import CrossoverTransformationHandler
from reinforcement.testchangetransformationhandler import TestChangeTransformationHandler
import pynguin.configuration as config


class NormalizationHandler:

    def __init__(self):
        crossover_rate_normalizer = Normalizer(
            "Crossover Rate",
            CrossoverTransformationHandler,
            lambda: config.configuration.search_algorithm.crossover_rate,
            lambda x: setattr(config.configuration.search_algorithm, 'crossover_rate', x)
        )

        test_change_probability_normalizer = Normalizer(
            "Test Change Probability",
            TestChangeTransformationHandler,
            lambda: config.configuration.search_algorithm.test_change_probability,
            lambda x: setattr(config.configuration.search_algorithm, 'test_change_probability', x)
        )

        self.normalizers = [
            crossover_rate_normalizer,
            test_change_probability_normalizer
        ]

    def apply_actions(self, actions):
        """Apply all actions retrieved to their respective configuration variable, after denormalizing them"""
        print("ACTIONS | ", end="")
        for i in range(max(len(actions), len(self.normalizers))):
            normalizer = self.normalizers[i]

            normalizer.set_value(normalizer.get_class().calc_new_config_value(normalizer.get_value(), actions[i]))

            print(f"{normalizer.get_name()}: {normalizer.get_class().denormalize_action(actions[i])}, ", end="")
        print("")

    def normalize_observations(self):
        """Return a numpy array of all normalized observations"""
        observations = []

        print("OBSERVATIONS | ", end="")
        for normalizer in self.normalizers:
            observations.append(normalizer.get_class().normalize_observation(normalizer.getter()))

            print(f"{normalizer.get_name()}: {normalizer.getter()}, ", end="")
        print("")

        return np.array(observations, dtype=np.float32)


class Normalizer:
    """Helper class to make NormalizationHandler more convenient to work with"""

    def __init__(self, readable_name, normalization_class, getter, setter):
        self.readable_name = readable_name
        self.normalization_class = normalization_class
        self.getter = getter
        self.setter = setter

    def get_name(self):
        return self.readable_name

    def get_class(self):
        return self.normalization_class

    def get_value(self):
        return self.getter()

    def set_value(self, value):
        self.setter(value)

# if __name__ == '__main__':
#     print(f"Before:  {config.configuration.search_algorithm.crossover_rate}")
#     a = NormalizationHandler()
#     a.apply_actions([-1])
#     print(f"Normalized observations: {a.normalize_observations()}")
#     print(f"After:  {config.configuration.search_algorithm.crossover_rate}")
#
#     print(f"Before 2:  {config.configuration.search_algorithm.crossover_rate}")
#     a = NormalizationHandler()
#     a.apply_actions([1])
#     print(f"Normalized observations: {a.normalize_observations()}")
#     print(f"After 2:  {config.configuration.search_algorithm.crossover_rate}")
