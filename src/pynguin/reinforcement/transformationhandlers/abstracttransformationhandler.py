from abc import ABC, abstractmethod


class AbstractTransformationHandler(ABC):
    """Handles transformation in between environment-space and normalized-space (used in the RL) of a single variable"""

    @abstractmethod
    def normalize_observation(self, denormalized_observation: float) -> float:
        """Scales observation from environment-space to normalized-space ([-1,1])"""
        pass

    @abstractmethod
    def denormalize_action(self, normalized_action: float) -> float:
        """Scales action from normalized-space ([-1,1]) to environment-space"""
        pass

    @abstractmethod
    def get_value(self):
        """Get the current environment-space variable value"""
        pass

    @abstractmethod
    def apply_action(self, normalized_action):
        """Apply a normalized-action to the environment"""
        pass

    @abstractmethod
    def get_name(self):
        """Get the reader friendly name of the transformation handler"""
        pass
