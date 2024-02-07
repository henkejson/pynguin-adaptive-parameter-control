from typing import Callable
import logging
import pynguin.configuration as config
import multiprocessing
from reinforcement.transformationhandlers.crossovertransformationhandler import CrossoverTransformationHandler
from reinforcement.transformationhandlers.testchangetransformationhandler import TestChangeTransformationHandler
from reinforcement.transformationhandlers.changeparametertransformationhandler import \
    ChangeParameterTransformationHandler
from reinforcement.customenv import training
from reinforcement.configurationhandler import ConfigurationHandler


class ReinforcementHandler:

    def __init__(self, best_coverage: Callable[[], float], _logger):
        # current_coverage: Callable[[], float],
        self.config_handler = self.set_up_tuning_parameters()
        self.timeout = 20
        self._logger = _logger

        # self.current_coverage_history = [0.0]
        # self.get_current_coverage = current_coverage

        self.best_coverage_history = [0.0]
        self.get_best_coverage = best_coverage
        self.previous_coverage = 0.0

        self.is_rl_activated = False
        self.first_activation = True
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
        for parameter in config.configuration.rl.tuning_parameters:

            match parameter:
                case config.TuningParameters.CrossoverRate:
                    tuning_parameters.append(CrossoverTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.TestChangeProbability:
                    tuning_parameters.append(TestChangeTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.ChangeParameterProbability:
                    tuning_parameters.append(ChangeParameterTransformationHandler(-0.05, 0.05))
                case _:
                    raise Exception()

        return ConfigurationHandler(tuning_parameters)

    def activate_reinforcement(self):
        threshold = 0.6
        best_coverage = self.get_best_coverage()

        if best_coverage < threshold:
            print("Under Threshold")
            return False

        coverage_diff = best_coverage - self.best_coverage_history[-1]
        if coverage_diff > 0:
            if self.is_rl_activated:
                self.previous_coverage = self.best_coverage_history[0]
                self.is_rl_activated = False
            self.best_coverage_history.clear()
            self.best_coverage_history.append(best_coverage)
            print("Improvement!")
            return False
        elif len(self.best_coverage_history) > 4:
            self.best_coverage_history.append(best_coverage)
            self.is_rl_activated = True
            print("Over three in a row!")
            return True
        else:
            self.best_coverage_history.append(best_coverage)
            print("Add one more to the stack")
            return False

    def update(self):

        if self.iteration >= config.configuration.rl.update_frequency:

            if self.activate_reinforcement():

                # Get the best coverage so far
                reward = self.calc_reward()

                # Send observations, rewards and if we are done
                self.conn.send((self.config_handler.get_normalized_observations(), reward, True, False))
                print(f"Best Coverage: {self.get_best_coverage()}")
                # Wait for new actions and apply them
                self.get_action()

            else:
                self.conn.send((None, 0, False, False))
            self.iteration = 0
        self.iteration += 1

    def get_action(self):
        if self.conn.poll(timeout=self.timeout):
            actions = self.conn.recv()
            self.config_handler.apply_actions(actions)
        else:
            self._logger.info("No action received... ")
            raise ValueError("No action received from RL.")

    def calc_reward(self):
        # Add the latest coverage value to the history
        # self.current_coverage_history.append(self.get_current_coverage())
        # self.best_coverage_history.append(self.get_best_coverage())

        best_coverage = self.get_best_coverage()

        if self.first_activation:
            self.first_activation = False
            self.previous_coverage = best_coverage
            return 0.0

        # Calculate reward from the coverage
        # Scale reward to give more as it approaches 1?

        reward = best_coverage - self.previous_coverage
        self.previous_coverage = best_coverage
        print(f"REWARD | (Best): {reward}")
        return reward

    def stop(self):
        self.conn.send((None, None, True, True))
