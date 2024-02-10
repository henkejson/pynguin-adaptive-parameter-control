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
        os.path.join(root_path, 'project_test_output'): {'bind': '/output', 'mode': 'rw'},
        os.path.join(root_path, 'project_requirements'): {'bind': '/package', 'mode': 'ro'}
        #os.path.join(root_path, 'run_results'): {'bind': '/results', 'mode': 'rw'}
    }

    print(root_path)
    print(volumes)

    command_input = """
            --project-path /projects \
            --output-path /project_test_output \
            --module-name bmi_calculator \
            --maximum_search_time 60 \
            --algorithm 'DYNAMOSA' \
            -v
            """
    #--report_dir "/results" \
    return client.containers.run("pynguin_image:latest", detach=True, volumes=volumes, command=command_input)


if __name__ == '__main__':
    client = docker.from_env()

    image_tag = "pynguin_image:latest"
    build_image(image_tag)
    # Run a container
    container = run_container()
    # print(container.logs())

    print(container.status)
    print(container.logs())
    time.sleep(5)
    print(container.status)
    print(container.logs())

    time.sleep(10)
    print(container.status)
    print(container.logs())
