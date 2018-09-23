# -*- coding: utf-8 -*-

import os

from paaspure.abstract import AbstractComponent
from paaspure.utils import docker_stack


class SwarmVisualizer(AbstractComponent):
    """Deploy the Swarm service visualizer."""
    def __init__(self):
        super(SwarmVisualizer, self).__init__()

    def build(self, config, client):
        docker_stack(
            command='deploy',
            compose_file=os.path.dirname(__file__) + '/docker-compose.yml',
            stack_name='visualizer'
        )

    def destroy(self, config, client):
        docker_stack(command='rm', stack_name='visualizer')


instance = SwarmVisualizer()
