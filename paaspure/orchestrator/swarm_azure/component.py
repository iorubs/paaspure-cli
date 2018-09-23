# -*- coding: utf-8 -*-

import os
import sys

from paaspure.abstract import AbstractComponent
from paaspure.utils import DockerClientSSHTunnel
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient


class SwarmAzure(AbstractComponent):
    """Find swarm manager and create client connection."""
    def __init__(self):
        super(SwarmAzure, self).__init__()

    def build(self, config, credentials):
        sp_creds = ServicePrincipalCredentials(
            client_id=credentials['azure_client_id'],
            secret=credentials['azure_client_secret'],
            tenant=credentials['azure_tenant_id']
        )

        network_client = NetworkManagementClient(
            sp_creds,
            credentials['subscription_id']
        )

        puplic_ip = network_client.public_ip_addresses.get(
            config['resource_group_name'],
            config['swarmName'] + '-externalSSHLoadBalancer-public-ip'
        )

        nat_rule = network_client.inbound_nat_rules.get(
            config['resource_group_name'],
            'externalSSHLoadBalancer',
            'default.0'
        )

        return puplic_ip.ip_address, nat_rule.frontend_port

    def destroy(self, config, credentials):
        pass

    def client_connection(self, config, credentials):
        manager_ip, manager_port = self.build(config, credentials)

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
            manager_address=manager_ip,
            manager_port=manager_port,
            bind_port=config['bind_port'],
            user=config['user']
        )


instance = SwarmAzure()
