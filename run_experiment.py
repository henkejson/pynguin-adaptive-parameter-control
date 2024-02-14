import json
import os
import random
import time

import requests

import docker
from pynguin.utils.statistics.runtimevariable import RuntimeVariable
from pynguin.utils.statistics.runtimevariable import RuntimeVariable as RVar

from src.pynguin.configuration import TuningParameters, Algorithm


class RunCommand:

    def __init__(self):
        self.argument_dict = {}
        self.volumes = []

    def add_argument(self, argument: str, value: str):
        self.argument_dict[argument] = value

    def get_argument(self, argument: str):
        return self.argument_dict.get(argument, None)

    def add_volume(self, base_directory: str, host_folder: str, container_folder: str, mode: str):
        self.volumes.append(f"{os.path.join(base_directory,host_folder)}:{container_folder}:{mode}")

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

    def add_output_variables(self, output_variables: list[RuntimeVariable]):
        tmp = []
        for parm in output_variables:
            tmp.append(parm.value)

        variables_string = ",".join(tmp)
        self.add_argument("output_variables", variables_string)


def build_image(image_tag: str):
    image_exists = False
    for image in client.images.list():
        for tag in image.tags:
            if tag == image_tag:
                image_exists = True
                break

    if not image_exists:
        print("Building Docker image locally... This will take a couple of minutes")
        image, build_output = client.images.build(path=".", dockerfile="docker/Dockerfile", tag=image_tag)
    else:
        print(f"Image {image_tag} already exist. Skip build.")


def run_container(command: RunCommand):
    print(command.build_command())
    print(command.volumes)

    print("Starting Container...")
    return client.containers.run(
        image_tag,
        command=command.build_command(),
        volumes=command.volumes,
        detach=True,
        auto_remove=False,
        stdout=True,
        stderr=True
    )


def get_path_modules() -> (str, str):
    """Paths and modules for all python files used for experimentation"""
    # Relative address (from input/) and module names for all files
    path_modules = [
        # ("projects/httpie", "httpie.output.writer"),
        # ("projects/httpie", "httpie.output.formatters.colors"),
        # ("projects/httpie", "httpie.sessions"),
        # ("projects/toy_example", "bmi_calculator")
        # ("numpy/", "vector")
    ]
    return path_modules


def get_run_config_algorithms() -> list[Algorithm]:
    """Algorithms used for experimentation"""
    algorithms = [
        Algorithm.DYNAMOSA
        # configuration.algorithm.MIO.value,
        # configuration.algorithm.MOSA.value,
        # configuration.algorithm.WHOLE_SUITE.value
    ]
    return algorithms


def get_run_config_tuning_params() -> list[TuningParameters]:
    """Parameters to tune for experimentation (only used with RL-enabled algorithms)"""
    # parameters = [param.value for param in configuration.TuningParameters]
    parameters = [TuningParameters.CrossoverRate]
    return parameters


def construct_run_configurations(max_search_time: int = 60, times_per_config: int = 1) -> list[RunCommand]:
    """Construct a list of all run configuration commands"""

    # get the ...
    path_modules = get_path_modules()
    algorithms = get_run_config_algorithms()
    parameters = get_run_config_tuning_params()

    run_id = 0
    commands = []

    for path, module, in path_modules:
        for algorithm in algorithms:
            for parameter in parameters:
                for _ in range(times_per_config):
                    command = RunCommand()
                    command.add_volume(os.getcwd(), path, "/input", "ro")
                    command.add_volume(os.getcwd(), "projects_test_output", "/output", "rw")
                    command.add_volume(os.getcwd(), path, "/package", "ro")
                    command.add_volume(os.getcwd(), "run_results", "/results", "rw")

                    command.add_argument("project_path", "/input")
                    command.add_argument("output_path", "/output")
                    command.add_argument("module_name", module)
                    command.add_algorithm(algorithm)
                    command.add_tuning_parameters([parameter])
                    command.add_argument("run_id", f"{run_id}")
                    command.add_argument("maximum_search_time", f"{max_search_time}")
                    command.add_argument("report_dir", "/results")
                    command.add_output_variables([RVar.RunId,
                                                  RVar.TargetModule,
                                                  RVar.Algorithm,
                                                  RVar.TuningParameters,
                                                  RVar.Coverage,
                                                  RVar.CoverageTimeline
                                                  ])
                    command.add_argument("v", "")
                    run_id += 1
                    commands.append(command)

    print(commands)
    return commands


if __name__ == '__main__':
    run_configs = construct_run_configurations(10, 1)
    random.seed(41753)
    random.shuffle(run_configs)
    print(run_configs)

    client = docker.from_env()

    image_tag = "pynguin_image:latest"
    build_image(image_tag)

    encountered_error = False

    i = 1

    # Run a container
    for run_config in run_configs:
        print(f"Running config {i}/{len(run_configs)} (run id: {run_config.get_argument('run_id')})")
        i += 1

        container = run_container(run_config)
        # print(container.logs())

        # Stream the logs
        # Wait for the container to finish
        print("Waiting for Pynguin to finish...")
        try:
            result = container.wait(timeout=1200)

            # Check for internal errors
            exit_code = result['StatusCode']
            if exit_code != 0:
                print(f"Container exited with error code {exit_code}")
                encountered_error = True

        except requests.exceptions.ConnectionError:
            print("Timed out waiting for container, stopping...")
            container.stop()
            encountered_error = True

        # Prepare for logging
        log_directory = "logs"
        log_filename = f"{run_config.get_argument('run_id')}.txt"
        log_path = os.path.join(log_directory, log_filename)

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Fetch logs after completion
        logs = container.logs()

        with open(log_path, 'w', encoding="utf-8") as file:
            file.write(logs.decode("utf-8"))

        # Optionally, remove the container manually if needed
        print("Removing container...")
        container.remove()

        # If we encountered an error, stop the loop
        if encountered_error:
            break
