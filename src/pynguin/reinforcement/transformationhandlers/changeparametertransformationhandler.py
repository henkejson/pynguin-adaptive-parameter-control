from pynguin.reinforcement.transformationhandlers.abstracttransformationhandler import AbstractTransformationHandler
import pynguin.configuration as config
from pynguin.reinforcement.transformationhandlers.basictransformationhandler import BasicTransformationHandler


class ChangeParameterTransformationHandler(AbstractTransformationHandler):
    """Transformation handler for the parameter ChangeParameterProbability"""
    def __init__(self, min_value: float = -0.05, max_value: float = 0.05):
        self.min_value = min_value
        self.max_value = max_value

        self.config_lower_bound = 0.0
        self.config_upper_bound = 1.0

        self.transformation_handler = BasicTransformationHandler(self.config_lower_bound, self.config_upper_bound,
                                                                 self.min_value, self.max_value)

    def normalize_observation(self, denormalized_observation: float) -> float:
        return self.transformation_handler.normalize_observation(denormalized_observation)

    def denormalize_action(self, normalized_action: float) -> float:
        return self.transformation_handler.denormalize_action(normalized_action)

    def get_value(self):
        return config.configuration.search_algorithm.change_parameter_probability

    def apply_action(self, normalized_action):
        new_value = self.get_value() + self.denormalize_action(normalized_action)
        new_value = self.transformation_handler.clamp(new_value)

        config.configuration.search_algorithm.change_parameter_probability = new_value

    def get_name(self):
        return "Change Parameter Probability"
