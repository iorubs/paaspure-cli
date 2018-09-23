# -*- coding: utf-8 -*-

import os
import docker
import json

from paaspure.abstract import AbstractComponent
from paaspure.utils import build_image, copy_from_container


class TerraformAWS(AbstractComponent):
    """Component for provisioning AWS resources."""
    def __init__(self):
        super(TerraformAWS, self).__init__()

    def build(self, config, credentials):
        var_file = os.path.dirname(__file__) + "/terraform.tfvars"
        with open(var_file, 'w+') as f:
            f.write(json.dumps(config, indent=4))

        self.__execute_command(credentials, ['apply', '-auto-approve'])

    def destroy(self, config, credentials):
        # TODO: Should destroy also remove resource files?
        self.__execute_command(credentials, ['destroy', '-force'])

    def __execute_command(self, credentials, command=['plan']):
        build_image(
            image_tag='paaspure_terraform',
            path=os.path.dirname(__file__)
        )

        client = docker.from_env()

        container = client.containers.run(
            'paaspure_terraform',
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


instance = TerraformAWS()
