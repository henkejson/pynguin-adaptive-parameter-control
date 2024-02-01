from reinforcement.abstracttransformationhandler import AbstractTransformationHandler
import pynguin.configuration as config


# TODO Should create a general one for probabilities [0, 1]

class TestChangeTransformationHandler(AbstractTransformationHandler):

    def __init__(self, min_value=-0.05, max_value=0.05):
        self.min_value = min_value
        self.max_value = max_value

        self.config_lower_bound = 0.0
        self.config_upper_bound = 1.0

    def normalize_observation(self, denormalized_observation: float) -> float:
        return self.convert_to_normalized(denormalized_observation, self.config_lower_bound, self.config_upper_bound)

    def denormalize_action(self, normalized_action: float) -> float:
        return self.convert_from_normalized(normalized_action, self.min_value, self.max_value)

    def get_value(self):
        return config.configuration.search_algorithm.test_change_probability

    def apply_action(self, normalized_action):
        current_value = self.get_value() + self.denormalize_action(normalized_action)
        current_value = min(self.config_upper_bound,
                            max(self.config_lower_bound, current_value))
        config.configuration.search_algorithm.test_change_probability = current_value

    def get_name(self):
        return "Test Change Probability"
