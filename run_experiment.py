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
    """Build Pynguin docker image"""
    print("Building Docker image locally... This can take a couple of minutes")

    # Attempt to build Pynguin image
    try:
        image, build_output = client.images.build(
            path=".",
            dockerfile="docker/Dockerfile",
            tag=image_tag,
            rm=True)

        for line in build_output:
            if 'stream' in line:
                print(line['stream'].strip())

    except docker.errors.BuildError as e:
        # Handle build errors (e.g., error in Dockerfile)
        print(f"Build failed: {e.msg}")
        # Print build logs that might contain clues to what went wrong
        for line in e.build_log:
            if 'stream' in line:
                print(line['stream'].strip())


def run_container(command: RunCommand, image_tag: str):
    """Run container with specified command"""
    print(command.build_command())

    print("Starting Container...")
    return client.containers.run(
        image_tag,
        command=command.build_command(),
        volumes=command.volumes,
        detach=True,
        auto_remove=False
    )


def get_path_modules() -> (str, str):
    """Paths and modules for all python files used for experimentation"""
    # Relative address (from input/) and module names for all files
    path_modules = [

        ("projects/codetiming", "codetiming._timer"),

        # X ("projects/dataclasses-json", "dataclasses_json.api"),
        # X ("projects/dataclasses-json", "dataclasses_json.mm"),
        # ("projects/dataclasses-json", "dataclasses_json.undefined")


        # ("projects/flake8/src", "flake8.exceptions"),
        # ("projects/flake8/src", "flake8.formatting.base"),
        # ("projects/flake8/src", "flake8.formatting.default"),
        # ("projects/flake8/src", "flake8.main.debug")

        # ("projects/flutils", "flutils.decorators"),
        # ("projects/flutils", "flutils.namedtupleutils"),
        ("projects/flutils", "flutils.packages"),
        # ("projects/flutils", "flutils.pathutils"),
        # ("projects/flutils", "flutils.setuputils.cmd"),
        # ("projects/flutils", "flutils.strutils"),


        # ("projects/docstring_parser", "docstring_parser.parser"),
        # ("projects/docstring_parser", "docstring_parser.google"),
        # ("projects/pyMonet", "pymonet.box"),
        # ("projects/pyMonet", "pymonet.immutable_list"),
        # ("projects/pyMonet", "pymonet.lazy"),
        # ("projects/pyMonet", "pymonet.maybe"),
        # ("projects/pyMonet", "pymonet.monad_try"),
        # ("projects/pyMonet", "pymonet.semigroups"),
        # ("projects/pyMonet", "pymonet.task"),
        # ("projects/pyMonet", "pymonet.validation"),

        # ("projects/httpie", "httpie.cli.dicts"),
        # ("projects/httpie", "httpie.config"),
        # ("projects/httpie", "httpie.models"),
        # ("projects/httpie", "httpie.output.formatters.colors"),
        # ("projects/httpie", "httpie.output.formatters.headers"),
        # ("projects/httpie", "httpie.output.formatters.json"),
        # ("projects/httpie", "httpie.output.processing"),
        # ("projects/httpie", "httpie.output.streams"),
        # ("projects/httpie", "httpie.plugins.base"),
        # ("projects/httpie", "httpie.plugins.manager"),

        # ("projects/httpie", "httpie.output.writer"),
        # ("projects/httpie", "httpie.sessions"),

        # ("projects/toy_example", "bmi_calculator")
    ]
    return path_modules


def get_run_config_algorithms() -> list[Algorithm]:
    """Algorithms used for experimentation"""
    algorithms = [
        Algorithm.DYNAMOSA,
        #Algorithm.DYNAMOSA_RL
    ]
    return algorithms


def get_run_config_tuning_params() -> list[list[TuningParameters]]:
    """Parameters to tune for experimentation (only used with RL-enabled algorithms)"""
    # parameters = [[param.value] for param in configuration.TuningParameters]

    # Tuned for now:
    # - statement insertion probability
    # - crossover rate
    # - elite

    #parameters = [[TuningParameters.StatementInsertionProbability], [TuningParameters.CrossoverRate], [TuningParameters.Elite]]
    parameters = [[TuningParameters.NONE]]
    return parameters


def construct_run_configurations(max_search_time: int, repetitions: int, update_freq: int, plateau_length: int) -> list[RunCommand]:
    """Construct a list of all run configuration commands"""

    # Get the components for the run-configurations
    path_modules = get_path_modules()
    algorithms = get_run_config_algorithms()
    parameters_list = get_run_config_tuning_params()

    commands = []

    for path, module, in path_modules:
        module_rep = 1
        for algorithm in algorithms:
            for parameters in parameters_list:
                for rep in range(1, repetitions + 1):
                    module_rep_id = f"{module}#{'{:02d}'.format(module_rep)}"
                    module_rep += 1

                    # Setup directories
                    module_rep_path = f"data/{module}/{module_rep_id}"
                    os.makedirs(os.path.join(os.getcwd(), module_rep_path), exist_ok=True)

                    # Construct run command
                    command = RunCommand()
                    command.add_volume(os.getcwd(), path, "/input", "ro")
                    command.add_volume(os.getcwd(), path, "/package", "ro")
                    command.add_volume(os.getcwd(), module_rep_path, "/output", "rw")
                    command.add_volume(os.getcwd(), "data", "/results", "rw")

                    command.add_argument("project_path", "/input")
                    command.add_argument("output_path", "/output")
                    command.add_argument("report_dir", "/results")
                    command.add_argument("module_name", module)
                    command.add_algorithm(algorithm)
                    command.add_tuning_parameters(parameters)
                    command.add_argument("run_id", f"{module_rep_id}")
                    command.add_argument("maximum_search_time", f"{max_search_time}")
                    command.add_argument("update_frequency", f"{update_freq}")
                    command.add_argument("plateau_length", f"{plateau_length}")
                    command.add_output_variables([RVar.RunId,
                                                  RVar.TargetModule,
                                                  RVar.Algorithm,
                                                  RVar.AlgorithmIterations,
                                                  RVar.SearchTime,
                                                  RVar.TuningParameters,
                                                  RVar.Coverage,
                                                  RVar.CoverageTimeline
                                                  ])
                    command.add_argument("assertion_generation", "NONE")
                    command.add_argument("create-coverage-report", "True")
                    #command.add_argument("coverage_metrics", "LINE")
                    command.add_argument("v", "")
                    commands.append(command)

    return commands


if __name__ == '__main__':
    run_configs = construct_run_configurations(300, 30, 10, 20)
    random.seed(41753)
    random.shuffle(run_configs)

    # Establish communication with the docker daemon
    client = docker.from_env()

    # Build Pynguin image
    img_tag = "pynguin_image:latest"
    build_image(image_tag=img_tag)

    # (Prep for run_config loop)
    encountered_error = False
    i = 1

    # Run a container per run configuration
    for run_config in run_configs:
        print(f"Running config {i}/{len(run_configs)} (run id: {run_config.get_argument('run_id')})")
        i += 1

        container = run_container(run_config, img_tag)

        print("Waiting for Pynguin to finish...")
        try:
            timeout_time = int(run_config.get_argument("maximum_search_time")) + 180
            result = container.wait(timeout=timeout_time)

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
        log_directory = f"data/{run_config.get_argument('module_name')}/{run_config.get_argument('run_id')}"
        log_filename = f"logs.txt"
        log_path = os.path.join(log_directory, log_filename)

        # Should already exist, only for some extra peace of mind
        os.makedirs(log_directory, exist_ok=True)

        # Fetch and save logs
        logs = container.logs()
        with open(log_path, 'w', encoding="utf-8") as file:
            file.write(logs.decode("utf-8"))

        #Move penguin-config.txt to the current run config data directory
        os.replace("data/pynguin-config.txt", os.path.join(log_directory, "pynguin-config.txt"))
        os.replace("data/cov_report.xml", os.path.join(log_directory, "cov_report.xml"))
        os.replace("data/cov_report.html", os.path.join(log_directory, "cov_report.html"))
        print("Removing container...")
        container.remove()

        # If we encountered an error, stop the loop
        if encountered_error:
            break
