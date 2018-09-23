# -*- coding: utf-8 -*-

import os
import docker
import json
import shutil
import importlib

from paaspure.abstract import AbstractComponent
from paaspure.utils import build_image, copy_from_container


class HybridAWS(AbstractComponent):
    """Component for extending existing swarm. Using AWS resources."""
    def __init__(self):
        super(HybridAWS, self).__init__()

    def build(self, config, credentials):
        var_file = os.path.dirname(__file__) + "/terraform.tfvars"
        with open(var_file, 'w+') as f:
            f.write(json.dumps(config, indent=4))

        # inventory_file = os.path.dirname(__file__) + "/swarm-inventory"
        # ssh_key = f'ansible_ssh_private_key_file={config["aws_key_name"]}.pem'
        # ssh_user = f'ansible_user={config["ssh_user"]}'
        #
        # orchestrator = self.__get_orchestrator_instance(
        #     config['orchestrator_params']['name'],
        #     config['orchestrator_params']['component']
        # )
        #
        # host, ssh_port = orchestrator.build(
        #     config['orchestrator_params'],
        #     credentials
        # )
        #
        # with open(inventory_file, 'w+') as f:
        #     f.write('[swarm-master]\n')
        #     f.write(f'{host} ansible_port={ssh_port} {ssh_user} {ssh_key}\n')
        #
        # shutil.copy2(credentials['private_key'], os.path.dirname(__file__))
        #
        self.__terraform_execute(credentials, ['apply', '-auto-approve'])
        self.__ansible_execute(
            credentials,
            ['-i', 'swarm-inventory', 'swarm-join.yml']
        )

    def destroy(self, config, credentials):
        # TODO: Should destroy also remove resource files?
        self.__ansible_execute(
            credentials,
            ['-i', 'swarm-inventory', 'swarm-leave.yml']
        )
        self.__terraform_execute(credentials, ['destroy', '-force'])

    def __get_orchestrator_instance(self, name, component):
        return importlib.import_module(
            name + '.' + component
        ).instance

    def __terraform_execute(self, credentials, command=['plan']):
        build_image(
            image_tag='paaspure_hybrid_terraform',
            path=os.path.dirname(__file__),
            dockerfile='Dockerfile.terraform'
        )

        client = docker.from_env()

        container = client.containers.run(
            'paaspure_hybrid_terraform',
            environment=[
                'AWS_ACCESS_KEY_ID=' + credentials['aws_access_key'],
                'AWS_SECRET_ACCESS_KEY=' + credentials['aws_secret_key']
            ],
            command=command,
            detach=True
        )

        for log in container.logs(stream=True):
            print(log.decode(), end='')

        copy_from_container(
            container=container,
            src_path='/data/.',
            dest_path=os.path.dirname(__file__)
        )

    def __ansible_execute(self, credentials, command=['--version']):
        build_image(
            image_tag='paaspure_hybrid_ansible',
            path=os.path.dirname(__file__),
            dockerfile='Dockerfile.ansible'
        )

        client = docker.from_env()

        container = client.containers.run(
            'paaspure_hybrid_ansible',
            command=command,
            detach=True
        )

        for log in container.logs(stream=True):
            print(log.decode(), end='')

        copy_from_container(
            container=container,
            src_path='/ansible/playbooks/.',
            dest_path=os.path.dirname(__file__)
        )


instance = HybridAWS()
