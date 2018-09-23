# -*- coding: utf-8 -*-

import os
import docker
import collections
import tarfile
import subprocess
import time


from paaspure import settings


def build_image(image_tag=None, path=None, dockerfile='Dockerfile'):
    print(f'Building docker image: {image_tag}')

    logs = docker.APIClient().build(
        path=path,
        tag=image_tag,
        decode=True,
        dockerfile=dockerfile
    )

    for log in logs:
        if settings.DEBUG:
            for key, value in log.items():
                print(value, end='')


def copy_from_container(container=None, src_path=None, dest_path=None,
                        force=False):

    if container.wait()['StatusCode'] != 0 and not force:
        print('Container execution failed, skipping copy_from_container()')
        print('\tYou can force it with force=True')
    else:
        stream, stat = container.get_archive(src_path)
        with open('extracted_resources.tar', 'wb') as outfile:
            for data in stream:
                outfile.write(data)

        tar = tarfile.open('extracted_resources.tar')
        tar.extractall(path=dest_path)
        tar.close()

        os.remove('extracted_resources.tar')


class MockContainerRun:
    def __init__(self, log_output=[], status_code=None):
        self.log_output = [log.encode() for log in log_output]
        self.status_code = status_code
        self.containers = self

    def __call__(self):
        return self

    def run(self, image_tag, **kwargs):
        MockContainerRun = collections.namedtuple(
            'MockContainerRun',
            'logs wait'
        )
        return MockContainerRun(logs=self.logs, wait=self.wait)

    def logs(self, stream=None):
        return self.log_output

    def wait(self):
        return {'StatusCode': self.status_code}


class DockerClientSSHTunnel:
    def __init__(self, key_path=None, manager_address=None, manager_port=22,
                 bind_port='2374', user=None):
        self.key_path = key_path
        self.manager_address = manager_address
        self.manager_port = str(manager_port)
        self.bind_port = str(bind_port)
        self.user = user

    def __enter__(self):
        self.p = subprocess.Popen(
            [
                'ssh', '-i', self.key_path, '-oStrictHostKeyChecking=no', '-p',
                self.manager_port, '-NL',
                f'localhost:{self.bind_port}:/var/run/docker.sock',
                f'{self.user}@{self.manager_address}'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # NOTE: wait for tunnel to be ready.
        time.sleep(1)

        return docker.DockerClient(base_url=f'localhost:{self.bind_port}')

    def __exit__(self, type, value, traceback):
        self.p.terminate()


def docker_stack(command=None, compose_file=None, stack_name=None):
    docker_command = f'docker -H localhost:2374 stack {command} '
    if command == 'deploy':
        docker_command += f'-c {compose_file} '
    docker_command += stack_name

    if subprocess.check_call(docker_command, shell=True) != 0:
        print('Error')
