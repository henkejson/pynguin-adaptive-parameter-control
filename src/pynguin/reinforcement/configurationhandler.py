import numpy as np

from pynguin.reinforcement.transformationhandlers.abstracttransformationhandler import AbstractTransformationHandler
import pynguin.configuration as config
from pynguin.reinforcement.transformationhandlers.crossovertransformationhandler import CrossoverTransformationHandler


class ConfigurationHandler:

    def __init__(self, transformation_handlers: list[AbstractTransformationHandler]):
        self.transformation_handlers = transformation_handlers

    def apply_actions(self, actions):
        """Apply all actions retrieved to their respective configuration variable, after denormalizing them"""
        print(" ACTIONS ".center(35, "-"))
        for i, action in enumerate(actions):
            normalizer = self.transformation_handlers[i]

            normalizer.apply_action(action)

            print(f"| {normalizer.get_name()}: (DN) {round(normalizer.denormalize_action(action), 4)} "
                  f"(N) {round(float(action), 4)}, ", )
        # print("")
        print("-"*35)
    def get_normalized_observations(self, handlers: list[AbstractTransformationHandler] = None):
        """Return a numpy array of all normalized observations"""
        observations = []

        if handlers is None:
            handlers = []

        print(" OBSERVATIONS ".center(35, "-") )
        for normalizer in handlers + self.transformation_handlers:
            observations.append(normalizer.normalize_observation(normalizer.get_value()))

            print(f"| {normalizer.get_name()}: (DN) {round(normalizer.get_value(), 4)}, "
                  f"(N) {round(normalizer.normalize_observation(normalizer.get_value()), 4)}", )
        # print("")

        return np.array(observations, dtype=np.float32)

    def iterate_transformation_handlers(self):
        for n in self.transformation_handlers:
            yield n
