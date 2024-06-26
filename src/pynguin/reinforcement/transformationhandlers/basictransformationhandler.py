from pynguin.reinforcement.transformationhandlers.abstracttransformationhandler import AbstractTransformationHandler


class BasicTransformationHandler(AbstractTransformationHandler):
    """Provides basic functionality for most transformations"""
    def __init__(self, lower_bound: float, upper_bound: float, min_value: float, max_value: float, name="UNNAMED"):
        self.min_value = min_value
        self.max_value = max_value

        self.config_lower_bound = lower_bound
        self.config_upper_bound = upper_bound

        self.name = name

    @staticmethod
    def convert_from_normalized(normalized_value, min_value, max_value):
        """Converts a normalized value [-1,1] into the range of [min_value, max_value]"""
        return (normalized_value + 1) * ((max_value - min_value) / 2) + min_value

    @staticmethod
    def convert_to_normalized(denormalized_value, lower_bound, upper_bound):
        """Converts a bounded value between [lower_bound, upper_bound] to a normalized value [-1,1]"""
        return ((denormalized_value - lower_bound) / (upper_bound - lower_bound)) * 2 - 1

    def clamp(self, current_value: float):
        """Make sure a float-value stays within defined bounds"""
        return max(self.config_lower_bound, min(self.config_upper_bound, current_value))

    def normalize_observation(self, denormalized_observation: float) -> float:
        return self.convert_to_normalized(denormalized_observation, self.config_lower_bound, self.config_upper_bound)

    def denormalize_action(self, normalized_action: float) -> float:
        return self.convert_from_normalized(normalized_action, self.min_value, self.max_value)

    def get_value(self):
        pass

    def apply_action(self, normalized_action):
        pass

    def get_name(self):
        return self.name
