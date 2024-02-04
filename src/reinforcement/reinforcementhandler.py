from typing import Callable
import logging
import pynguin.configuration as config
import multiprocessing
from reinforcement.transformationhandlers.crossovertransformationhandler import CrossoverTransformationHandler
from reinforcement.customenv import training
from reinforcement.configurationhandler import ConfigurationHandler
from reinforcement.transformationhandlers.testchangetransformationhandler import TestChangeTransformationHandler


class ReinforcementHandler:

    def __init__(self, current_coverage: Callable[[], float], best_coverage: Callable[[], float], _logger):
        self.config_handler = self.set_up_tuning_parameters()
        self.timeout = 20
        self._logger = _logger

        self.get_current_coverage = current_coverage
        self.get_best_coverage = best_coverage

        conn_1, conn_2 = multiprocessing.Pipe()
        self.conn = conn_1
        self.set_up_process(conn_2)

        self.iteration = 0

        self.get_action()

    def set_up_process(self, conn):
        # Create a new process, passing the child connection
        p = multiprocessing.Process(target=training,
                                    args=(len(self.config_handler.normalizers),  # number of actions
                                          len(self.config_handler.normalizers),  # number of observations
                                          conn,))
        p.start()

    @staticmethod
    def set_up_tuning_parameters() -> ConfigurationHandler:
        tuning_parameters = []
        for i in config.configuration.rl.tuning_parameters:
            if i == config.TuningParameters.CrossoverRate:
                tuning_parameters.append(CrossoverTransformationHandler(-0.05, 0.05))

            elif i == config.TuningParameters.TestChangeProbability:
                tuning_parameters.append(TestChangeTransformationHandler(-0.05, 0.05))

        return ConfigurationHandler(tuning_parameters)

    def update(self):

        if self.iteration >= config.configuration.rl.update_frequency:

            # Get the best coverage so far
            current_coverage = self.get_current_coverage()
            best_coverage = self.get_best_coverage()

            # Send observations, rewards and if we are done
            self.conn.send((self.config_handler.get_normalized_observations(), current_coverage, False))
            print(f"Current Coverage: {current_coverage}")
            print(f"Best Coverage: {best_coverage}")
            # Wait for new actions and apply them
            self.get_action()

            self.iteration = 0

        self.iteration += 1

    def get_action(self):
        if self.conn.poll(timeout=self.timeout):
            actions = self.conn.recv()
            self.config_handler.apply_actions(actions)
        else:
            self._logger.info("No action received... ")
            raise ValueError("No action received from RL.")


    def stop(self):
        self.conn.send((None, None, True))
