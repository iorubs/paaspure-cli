# -*- coding: utf-8 -*-

import os

from paaspure.abstract import AbstractComponent
from paaspure.utils import docker_stack


class TraefikReverseProxy(AbstractComponent):
    """Deploy the areverse proxy traefik."""
    def __init__(self):
        super(TraefikReverseProxy, self).__init__()

    def build(self, config, client):
        docker_stack(
            command='deploy',
            compose_file=os.path.dirname(__file__) + '/docker-compose.yml',
            stack_name='logging'
        )

    def destroy(self, config, client):
        docker_stack(
            command='rm',
            stack_name='logging'
        )


instance = TraefikReverseProxy()
