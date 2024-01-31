from abc import ABC, abstractmethod


class AbstractTransformationHandler(ABC):
    """Handles transformation in between environment-space and normalized-space (used in the RL)"""
    @staticmethod
    @abstractmethod
    def normalize_observation(observation: float) -> float:
        """Scales observation from environment-space to normalized-space ([-1,1])"""
        pass

    @staticmethod
    @abstractmethod
    def denormalize_action(normalized_action: float) -> float:
        """Scales action from normalized-space ([-1,1]) to environment-space"""
        pass

    @staticmethod
    @abstractmethod
    def calc_new_config_value(current_value: float, action: float) -> float:
        """Calculates new valid configuration value"""
        pass

