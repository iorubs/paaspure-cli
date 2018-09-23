# -*- coding: utf-8 -*-

import os
import docker
import boto3

from paaspure.abstract import AbstractComponent
from botocore.exceptions import ClientError
from paaspure.utils import read_yaml_file, write_yaml_file, escape_ansi, \
    build_image


class PackerAWS(AbstractComponent):
    """Create AWS AMIs using Packer."""
    def __init__(self):
        self.resource_file = os.path.join(
            os.path.dirname(__file__),
            'resources.yml'
        )

        super(PackerAWS, self).__init__()

    def parse_id(self, line):
        no_color = escape_ansi(line)
        split_output = no_color.replace('\n', ' ').split()
        return split_output if len(split_output) == 0 else split_output[-1]

    def build(self, config, credentials):
        client = docker.from_env()
        build_image(
            image_tag='paaspure_packer',
            path=os.path.dirname(__file__)
        )

        resources = {'images': [], 'snapshots': []}

        command = ['build']

        for var_file in config['var-files']:
            command.append(f'-var-file={var_file}')

        command.append(config['template'])

        container = client.containers.run(
            'paaspure_packer',
            environment=[
                'AWS_ACCESS_KEY=' + credentials['aws_access_key'],
                'AWS_SECRET_KEY=' + credentials['aws_secret_key']
            ],
            command=command,
            detach=True
        )

        for log in container.logs(stream=True):
            print(log.decode(), end='')

            if 'AMI: ami' in log.decode() and 'Error' not in log.decode():
                resources['images'].append(self.parse_id(log.decode()))
            elif 'shot: snap' in log.decode() and 'Error' not in log.decode():
                resources['snapshots'].append(self.parse_id(log.decode()))

        if container.wait()['StatusCode'] == 1:
            print(container.wait()['StatusCode'])
            raise Exception('Could not build image.')
        else:
            write_yaml_file(resources, self.resource_file)

    def destroy(self, config, credentials):
        self.boto3_client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['aws_access_key'],
            aws_secret_access_key=credentials['aws_secret_key'],
            region_name=config['region']
        )

        resources = {}

        try:
            resources = read_yaml_file(
                'packer resource',
                self.resource_file
            )
        except Exception as err:
            print('No packer resources were removed!')
            return

        self.__destroy_resources(
            resource_list=resources['images'],
            resource_type='image'
        )

        self.__destroy_resources(
            resource_list=resources['snapshots'],
            resource_type='snapshot'
        )

        if len(resources['snapshots']) == 0 and len(resources['images']) == 0:
            os.remove(self.resource_file)
            print('All packer resources removed succefully!')
        else:
            print('Could not remove some resources!')
            write_yaml_file(resources, self.resource_file)

    def __destroy_resources(self, resource_list=[], resource_type=None):
        already_removed_codes = [
            'InvalidAMIID.Unavailable',
            'InvalidSnapshot.NotFound'
        ]

        for resource_id in resource_list:
            try:
                if resource_type == 'image':
                    self.boto3_client.deregister_image(ImageId=resource_id)
                if resource_type == 'snapshot':
                    self.boto3_client.delete_snapshot(SnapshotId=resource_id)

                resource_list.remove(resource_id)

                print(f'Removed {resource_type}: {resource_id}')
            except ClientError as e:
                if e.response['Error']['Code'] in already_removed_codes:
                    resource_list.remove(resource_id)
                else:
                    print(f'Could not remove resource: {resource_id}')


instance = PackerAWS()
