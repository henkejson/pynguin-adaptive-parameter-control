from abc import ABC, abstractmethod


class AbstractTransformationHandler(ABC):
    """Handles transformation in between environment-space and normalized-space (used in the RL)"""

    @staticmethod
    def convert_from_normalized(normalized_value, min_value, max_value):
        return (normalized_value + 1) * ((max_value - min_value) / 2) + min_value

    @staticmethod
    def convert_to_normalized(denormalized_value, lower_bound, upper_bound):
        return ((denormalized_value - lower_bound) / (upper_bound - lower_bound)) * 2 - 1

    def get_name(self):
        return ""

    @abstractmethod
    def normalize_observation(self, denormalized_observation: float) -> float:
        """Scales observation from environment-space to normalized-space ([-1,1])"""
        pass

    @abstractmethod
    def denormalize_action(self, normalized_action: float) -> float:
        """Scales action from normalized-space ([-1,1]) to environment-space"""
        pass

    # TODO Remove maybe????
    @abstractmethod
    def calc_new_config_value(self, current_value: float, action: float) -> float:
        """Calculates new valid configuration value"""
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def set_value(self, normalized_action):
        pass



