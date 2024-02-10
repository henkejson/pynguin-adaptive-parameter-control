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
        test_image = client.images.build(path=".", dockerfile="docker/Dockerfile", tag=image_tag)
    else:
        print(f"Image {image_tag} already exist. Skip build.")


def run_container():
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
        "--report_dir", "/results",
        "-v"
    ]
    return client.containers.run(
        "pynguin_image:latest",
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
    container = run_container()
    # print(container.logs())

    # Stream the logs
    # Wait for the container to finish
    container.wait()

    # Fetch logs after completion
    logs = container.logs()
    print(logs.decode("utf-8"))

    # Optionally, remove the container manually if needed
    container.remove()

    # Optionally, remove the container after execution
    #container.remove()



