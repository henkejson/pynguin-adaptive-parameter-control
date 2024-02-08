from reinforcement.transformationhandlers.abstracttransformationhandler import AbstractTransformationHandler
from reinforcement.transformationhandlers.basictransformationhandler import BasicTransformationHandler
import pynguin.configuration as config


class EliteTransformationHandler(AbstractTransformationHandler):

    def __init__(self, min_value: int = -1, max_value: int = 1):
        self.min_value = float(min_value)
        self.max_value = float(max_value)

        self.config_lower_bound = 0.0
        self.config_upper_bound = 10.0

        self.transformation_handler = BasicTransformationHandler(self.config_lower_bound, self.config_upper_bound,
                                                                 self.min_value, self.max_value)

    def normalize_observation(self, denormalized_observation: float) -> float:
        return self.transformation_handler.normalize_observation(denormalized_observation)

    def denormalize_action(self, normalized_action: float) -> float:
        return self.transformation_handler.denormalize_action(normalized_action)

    def get_value(self):
        return config.configuration.search_algorithm.elite

    def apply_action(self, normalized_action):
        current_value = self.get_value() + self.denormalize_action(normalized_action)
        current_value = self.transformation_handler.clamp(current_value)

        config.configuration.search_algorithm.elite = int(round(current_value, 0))

    def get_name(self):
        return "Elite"
