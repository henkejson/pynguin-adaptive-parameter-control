from reinforcement.abstracttransformationhandler import AbstractTransformationHandler

# TODO Should create a general one for probabilities [0, 1]

class TestChangeTransformationHandler(AbstractTransformationHandler):
    LOWER_BOUND = 0.0
    UPPER_BOUND = 1.0

    NEW_MIN = -0.05
    NEW_MAX = 0.05

    @staticmethod
    def normalize_observation(observation: float) -> float:
        normalized_observation = ((observation - TestChangeTransformationHandler.LOWER_BOUND) / (
            TestChangeTransformationHandler.UPPER_BOUND - TestChangeTransformationHandler.LOWER_BOUND)) * 2 - 1

        return normalized_observation

    @staticmethod
    def denormalize_action(normalized_action: float) -> float:
        action = ((normalized_action + 1) * (
            (TestChangeTransformationHandler.NEW_MAX - TestChangeTransformationHandler.NEW_MIN) / 2) +
                  TestChangeTransformationHandler.NEW_MIN)

        return action

    @staticmethod
    def calc_new_config_value(current_value: float, action: float) -> float:
        current_value += TestChangeTransformationHandler.denormalize_action(action)
        current_value = min(TestChangeTransformationHandler.UPPER_BOUND,
                            max(TestChangeTransformationHandler.LOWER_BOUND, current_value))

        return current_value

