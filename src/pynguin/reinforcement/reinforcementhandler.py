from typing import Callable
import pynguin.configuration as config
import multiprocessing

from pynguin.reinforcement.apoenvironment import training
from pynguin.reinforcement.configurationhandler import ConfigurationHandler

from pynguin.reinforcement.transformationhandlers.changeparametertransformationhandler import \
    ChangeParameterTransformationHandler
from pynguin.reinforcement.transformationhandlers.chromosomelengthtransformationhandler import \
    ChromosomeLengthTransformationHandler
from pynguin.reinforcement.transformationhandlers.crossovertransformationhandler import CrossoverTransformationHandler
from pynguin.reinforcement.transformationhandlers.elitetransformationhandler import EliteTransformationHandler
from pynguin.reinforcement.transformationhandlers.perturbationtransformationhandler import \
    PerturbationTransformationHandler
from pynguin.reinforcement.transformationhandlers.populationtransformationhandler import PopulationTransformationHandler
from pynguin.reinforcement.transformationhandlers.statementinsertiontransformationhandler import \
    StatementInsertionTransformationHandler
from pynguin.reinforcement.transformationhandlers.testchangetransformationhandler import TestChangeTransformationHandler
from pynguin.reinforcement.transformationhandlers.testdeletetransformationhandler import TestDeleteTransformationHandler
from pynguin.reinforcement.transformationhandlers.testinsertiontransformationhandler import TestInsertionTransformationHandler
from pynguin.reinforcement.transformationhandlers.testinserttransformationhandler import TestInsertTransformationHandler
from pynguin.reinforcement.transformationhandlers.tournamentsizetransformationhandler import TournamentSizeTransformationHandler


class ReinforcementHandler:

    def __init__(self, best_coverage: Callable[[], float], _logger):
        # current_coverage: Callable[[], float],
        self.config_handler = self.set_up_tuning_parameters()
        self.timeout = 20
        self._logger = _logger

        # Variables associated with coverage
        self.get_best_coverage = best_coverage
        self.previous_coverage = 0.0
        self.rl_activated = False
        self.plateau = [0.0, 0.0]


        conn_1, conn_2 = multiprocessing.Pipe()
        self.conn = conn_1
        self.conn_2 = conn_2

        self.iteration = 0


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
                case config.TuningParameters.ChangeParameterProbability:
                    tuning_parameters.append(ChangeParameterTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.ChromosomeLength:
                    tuning_parameters.append(ChromosomeLengthTransformationHandler(-5, 5))
                case config.TuningParameters.CrossoverRate:
                    tuning_parameters.append(CrossoverTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.Elite:
                    tuning_parameters.append(EliteTransformationHandler(-1, 1))
                case config.TuningParameters.Population:
                    tuning_parameters.append(PopulationTransformationHandler(-15, 15))
                case config.TuningParameters.RandomPerturbation:
                    tuning_parameters.append(PerturbationTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.StatementInsertionProbability:
                    tuning_parameters.append(StatementInsertionTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.TestChangeProbability:
                    tuning_parameters.append(TestChangeTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.TestDeleteProbability:
                    tuning_parameters.append(TestDeleteTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.TestInsertProbability:
                    tuning_parameters.append(TestInsertTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.TestInsertionProbability:
                    tuning_parameters.append(TestInsertionTransformationHandler(-0.05, 0.05))
                case config.TuningParameters.TournamentSize:
                    tuning_parameters.append(TournamentSizeTransformationHandler(-1, 1))

                case config.TuningParameters.NONE:
                    raise ValueError("Cannot tune no parameters when using an RL-enabled algorithm")
                case _:
                    raise Exception()

        return ConfigurationHandler(tuning_parameters)

    def activate_reinforcement(self):

        best_coverage = self.get_best_coverage()
        if best_coverage > self.plateau[1]:
            self.plateau[0] = 0
            self.plateau[1] = best_coverage
            print("NEW COVERAGE ACHIEVED")
            return False
        elif self.plateau[0] >= config.configuration.rl.plateau_length:
            self.rl_activated = True
            self.set_up_process(self.conn_2)
            self.previous_coverage = best_coverage
            self.get_action()  # Get the initial action from the RL
            print("😨😨😨 RL ACTIVATED 😨😨😨")
            return False
        else:
            print("Plateau not ACHIEVED... waiting 😴 ")
            return False

    def update(self):
        self.plateau[0] += 1
        if self.iteration >= config.configuration.rl.update_frequency:

            if self.rl_activated or self.activate_reinforcement():

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

        # Calculate reward from the coverage
        # Scale reward to give more as it approaches 1?

        reward = best_coverage - self.previous_coverage
        self.previous_coverage = best_coverage
        print(f"REWARD | (Best): {reward}")
        return reward

    def stop(self):
        self.conn.send((None, None, True, True))
