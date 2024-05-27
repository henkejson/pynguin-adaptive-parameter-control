from pynguin.reinforcement.transformationhandlers.abstracttransformationhandler import AbstractTransformationHandler
import pynguin.configuration as config
from pynguin.reinforcement.transformationhandlers.basictransformationhandler import BasicTransformationHandler
from typing import Callable


class CoverageTransformationHandler(AbstractTransformationHandler):
    """Transformation handler for coverage"""
    def __init__(self, get_coverage_function: Callable[[], float]):
        self.get_coverage = get_coverage_function

        self.transformation_handler = BasicTransformationHandler(lower_bound=0, upper_bound=1,
                                                                 min_value=0, max_value=0)

    def normalize_observation(self, denormalized_observation: float) -> float:
        return self.transformation_handler.normalize_observation(denormalized_observation)

    def denormalize_action(self, normalized_action: float) -> float:
        raise NotImplementedError

    def get_value(self):
        return self.get_coverage()

    def apply_action(self, normalized_action):
        raise NotImplementedError

    def get_name(self):
        return "Best Coverage"
