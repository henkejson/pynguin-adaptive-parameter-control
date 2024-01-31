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


class Normalizer:
    def __init__(self, normalization_class, getter, setter):
        self.normalization_class = normalization_class
        self.getter = getter
        self.setter = setter

    def get_class(self):
        return self.normalization_class

    def get_value(self):
        print(f"Does the value update? {self.getter()}")
        return self.getter()

    def set_value(self, value):
        self.setter(value)


# if __name__ == '__main__':
#     print(f"Before:  {config.configuration.search_algorithm.crossover_rate}")
#     a = NormalizationHandler()
#     a.apply_actions([-1])
#     print(f"After:  {config.configuration.search_algorithm.crossover_rate}")
#
#     print(f"Before 2:  {config.configuration.search_algorithm.crossover_rate}")
#     a = NormalizationHandler()
#     a.apply_actions([1])
#     print(f"After 2:  {config.configuration.search_algorithm.crossover_rate}")
