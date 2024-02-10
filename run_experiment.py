import json
import os
import time

import docker


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


def run_container(image_tag: str):
    root_path = os.getcwd()
    volumes = {
        os.path.join(root_path, 'projects'): {'bind': '/input', 'mode': 'ro'},
        os.path.join(root_path, 'projects_test_output'): {'bind': '/output', 'mode': 'rw'},
        os.path.join(root_path, 'project_packages'): {'bind': '/package', 'mode': 'ro'},
        os.path.join(root_path, 'run_results'): {'bind': '/results', 'mode': 'rw'}
    }

    print(root_path)
    print(volumes)

    command = [
        "--project-path", "/input",
        "--module-name", "bmi_calculator",
        "--output-path", "/output",
        "--maximum_search_time", "10",
        "--report_dir", "/results/experiment1/dyna",
        "-v"
    ]

    print("Starting Container...")
    return client.containers.run(
        image_tag,
        command=command,
        volumes=volumes,
        detach=True,
        auto_remove=False,
        stdout=True,
        stderr=True
    )


if __name__ == '__main__':
    client = docker.from_env()

    image_tag = "pynguin_image:latest"
    build_image(image_tag)
    # Run a container
    container = run_container(image_tag)
    # print(container.logs())

    # Stream the logs
    # Wait for the container to finish
    print("Waiting for Pynguin to finish...")
    container.wait()

    # Fetch logs after completion
    logs = container.logs()
    print(logs.decode("utf-8"))

    # Optionally, remove the container manually if needed
    print("Removing container...")
    container.remove()




