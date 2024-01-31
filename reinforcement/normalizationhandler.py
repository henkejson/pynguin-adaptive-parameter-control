import numpy as np

from reinforcement.crossoverratenormalization import CrossoverRateNormalization
import pynguin.configuration as config


class NormalizationHandler:

    def __init__(self):
        crossover_rate_normalizer = Normalizer(CrossoverRateNormalization,
                                               lambda: config.configuration.search_algorithm.crossover_rate,
                                               lambda x: setattr(config.configuration.search_algorithm,
                                                                 'crossover_rate', x))

        self.normalizers = [
            crossover_rate_normalizer
        ]

    def apply_actions(self, actions):
        """Apply all actions retrieved to their respective configuration variable, after denormalizing them"""
        for i in range(max(len(actions), len(self.normalizers))):
            normalizer = self.normalizers[i]

            normalizer.set_value(
                normalizer.get_class().denormalize(
                    normalizer.get_value(), actions[i]
                )
            )

    def normalize_observations(self):
        """Return a numpy array of all normalized observations"""
        observations = []

        for normalizer in self.normalizers:
            observations.append(normalizer.get_class().normalize(normalizer.getter()))

        return np.array(observations, dtype=np.float32)


class Normalizer:
    """Helper class to make NormalizationHandler more convenient to work with"""
    def __init__(self, normalization_class, getter, setter):
        self.normalization_class = normalization_class
        self.getter = getter
        self.setter = setter

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
