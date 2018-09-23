# -*- coding: utf-8 -*-

import os
import boto3
import sys

from paaspure.abstract import AbstractComponent
from paaspure.utils import DockerClientSSHTunnel


class SwarmAWS(AbstractComponent):
    """Find swarm manager and create client connection."""
    def __init__(self):
        super(SwarmAWS, self).__init__()

    def build(self, config, credentials):
        os.environ['AWS_ACCESS_KEY_ID'] = credentials['aws_access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['aws_secret_key']
        os.environ['AWS_DEFAULT_REGION'] = config['region']

        ec2 = boto3.resource('ec2')

        filter_managers = [{
             'Name': f'tag:{config["tags"]["key"]}',
             'Values': [config['tags']['manager_value']]
        }, {
             'Name': 'instance-state-name',
             'Values': ['running']
        }]

        filter_workers = [{
             'Name': f'tag:config["tags"]["key"]',
             'Values': [config['tags']['worker_value']]
        }, {
             'Name': 'instance-state-name',
             'Values': ['running']
        }]

        return {
            'managers': ec2.instances.filter(Filters=filter_managers),
            'workers': ec2.instances.filter(Filters=filter_workers),
        }

    def destroy(self, config, credentials):
        pass

    def client_connection(self, config, credentials):
        cluster_instances = self.build(config, credentials)
        first_manager = list(cluster_instances['managers'])[0]

        try:
            permission = oct(
                os.stat(credentials['private_key']).st_mode & 0o777
            )
            if int(permission[2:]) > 600:
                raise Exception(f'Permissions {permission} for \
                                {credentials["private_key"]} are too open.')
        except KeyError:
            print(f'No private_key credential in Purefile')
            sys.exit(1)

        return DockerClientSSHTunnel(
            key_path=credentials["private_key"],
            manager_address=first_manager.public_ip_address,
            bind_port=config['bind_port'],
            user=config['user']
        )


instance = SwarmAWS()


# docker -H localhost:2374 service create \
#   --name=viz \
#   --publish=8080:8080/tcp \
#   --constraint=node.role==manager \
#   --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
#   dockersamples/visualizer
