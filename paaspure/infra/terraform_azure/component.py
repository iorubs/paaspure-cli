# -*- coding: utf-8 -*-

import os
import docker
import json

from paaspure.abstract import AbstractComponent
from paaspure.utils import build_image, copy_from_container


class TerraformAzure(AbstractComponent):
    """Component for provisioning Azure resources."""
    def __init__(self):
        super(TerraformAzure, self).__init__()

    def build(self, config, credentials):
        with open(config['parameters']['linuxSSHPublicKey'], 'r') as f:
            config['parameters']['linuxSSHPublicKey'] = f.read()

        config['parameters']['adServicePrincipalAppID'] = \
            credentials['azure_client_id']
        config['parameters']['adServicePrincipalAppSecret'] = \
            credentials['azure_client_secret']

        var_file = os.path.dirname(__file__) + "/terraform.tfvars"
        with open(var_file, 'w+') as f:
            f.write(json.dumps(config, indent=4))

        self.__execute_command(credentials, ['apply', '-auto-approve'])

    def destroy(self, config, credentials):
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
                'ARM_CLIENT_ID=' + credentials['azure_client_id'],
                'ARM_CLIENT_SECRET=' + credentials['azure_client_secret'],
                'ARM_TENANT_ID=' + credentials['azure_tenant_id'],
                'ARM_SUBSCRIPTION_ID=' + credentials['subscription_id']

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


instance = TerraformAzure()
