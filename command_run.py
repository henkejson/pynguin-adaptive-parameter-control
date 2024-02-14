import os

from src.pynguin.configuration import configuration
from src.pynguin.configuration import TuningParameters, Algorithm


class RunCommand:

    def __init__(self):
        self.argument_dict = {}
        self.volumes = {}

    def add_argument(self, argument: str, value: str):
        self.argument_dict[argument] = value

    def get_argument(self, argument: str):
        return self.argument_dict.get(argument, None)

    def add_volume(self, base_directory: str, host_folder: str, container_folder: str, mode: str):
        self.volumes[os.path.join(base_directory, host_folder)] = {'bind': container_folder, 'mode': mode}

    def build_command(self, start_command: str = "") -> list[str]:
        command_list = []
        if start_command != "":
            command_list.append(start_command)

        for argument, value in self.argument_dict.items():
            if len(argument) > 1:
                command_list.append("--" + argument)
                command_list.append(value)
            else:
                command_list.append("-" + argument)

        return command_list

    def add_algorithm(self, algorithm: Algorithm):
        self.add_argument("algorithm", algorithm.value)

    def add_tuning_parameters(self, tuning_parameters: list[TuningParameters]):
        tmp = []
        for parm in tuning_parameters:
            tmp.append(parm.value)

        param_string = ",".join(tmp)
        self.add_argument("tuning_parameters", param_string)


if __name__ == '__main__':
    command = RunCommand()
    command.add_argument("project_path", "projects/")
    command.add_argument("v", "")
    command.add_algorithm(configuration.algorithm.DYNAMOSA_RL)
    command.add_tuning_parameters([TuningParameters.CrossoverRate,
                                   TuningParameters.TestInsertionProbability])
    command.add_volume(os.getcwd(), "projects", '/input', "ro")
    print(command.volumes)
    # print(type(configuration.TuningParameters.CrossoverRate))
    print(command.get_argument("project_path"))
    print(command.get_argument("prhre_tth"))
    print(command.build_command("pynguin"))
