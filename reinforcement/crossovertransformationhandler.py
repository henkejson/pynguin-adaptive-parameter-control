from reinforcement.abstracttransformationhandler import AbstractTransformationHandler

# TODO Should create a general one for probabilities [0, 1]

class CrossoverTransformationHandler(AbstractTransformationHandler):
    LOWER_BOUND = 0.0
    UPPER_BOUND = 1.0

    NEW_MIN = -0.05
    NEW_MAX = 0.05

    @staticmethod
    def normalize_observation(observation: float) -> float:
        normalized_observation = ((observation - CrossoverTransformationHandler.LOWER_BOUND) / (
            CrossoverTransformationHandler.UPPER_BOUND - CrossoverTransformationHandler.LOWER_BOUND)) * 2 - 1

        return normalized_observation

    @staticmethod
    def denormalize_action(normalized_action: float) -> float:
        action = ((normalized_action + 1) * (
            (CrossoverTransformationHandler.NEW_MAX - CrossoverTransformationHandler.NEW_MIN) / 2) +
                  CrossoverTransformationHandler.NEW_MIN)

        return action

    @staticmethod
    def calc_new_config_value(current_value: float, action: float) -> float:
        current_value += CrossoverTransformationHandler.denormalize_action(action)
        current_value = min(CrossoverTransformationHandler.UPPER_BOUND,
                            max(CrossoverTransformationHandler.LOWER_BOUND, current_value))

        return current_value


