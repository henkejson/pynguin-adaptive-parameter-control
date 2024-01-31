from abc import ABC, abstractmethod


class NormalizationFunction(ABC):
    @staticmethod
    @abstractmethod
    def normalize(observation: float) -> float:
        """Go from desired scale to [-1,1]"""
        pass

    @staticmethod
    @abstractmethod
    def denormalize(current_value: float, normalized_action: float) -> float:
        """Go from scale [-1, 1] to desired scale"""
        pass


