import json
import pynguin.configuration as config
from pathlib import Path

"""Handle loading and saving JSON information"""


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


def save_parameter_data(modulename: str, run_id: str, run_data: dict):
    output_dir = Path(
        config.configuration.statistics_output.report_dir
    ).resolve()
    output_file = output_dir / f"{modulename}/{run_id}/parameters_timeline.json"

    with open(output_file, 'w') as json_file:
        json.dump(run_data, json_file, indent=4)


def save_config_data(filename: str, modulename: str, run_id: str, config_data: dict):
    output_dir = Path(
        config.configuration.statistics_output.report_dir
    ).resolve()
    output_file = output_dir / f"{filename}.json"

    # Read json file and return a dictionary
    data = read_json_file(output_file)

    if modulename not in data:
        data[modulename] = {}
    data[modulename][run_id] = config_data

    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)
