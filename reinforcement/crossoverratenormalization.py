from reinforcement.normalizationfunction import NormalizationFunction


class CrossoverRateNormalization(NormalizationFunction):
    LOWER_BOUND = 0.0
    UPPER_BOUND = 1.0

    NEW_MIN = -0.05
    NEW_MAX = 0.05

    @staticmethod
    def normalize(observation: float) -> float:
        normalized_observation = ((observation - CrossoverRateNormalization.LOWER_BOUND) / (
                CrossoverRateNormalization.UPPER_BOUND - CrossoverRateNormalization.LOWER_BOUND)) * 2 - 1

        return normalized_observation

    @staticmethod
    def denormalize(current_value: float, normalized_action: float) -> float:
        action = ((normalized_action + 1) * (
            (CrossoverRateNormalization.NEW_MAX - CrossoverRateNormalization.NEW_MIN) / 2) +
                  CrossoverRateNormalization.NEW_MIN)

        current_value += action
        current_value = min(CrossoverRateNormalization.UPPER_BOUND,
                            max(CrossoverRateNormalization.LOWER_BOUND, current_value))

        return current_value


if __name__ == '__main__':
    print(CrossoverRateNormalization.denormalize(0, -1))
    print(CrossoverRateNormalization.normalize(0))
