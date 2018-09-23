# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractModule
from .argparser import NetworkParser


class Network(AbstractModule):
    """
        Abstraction module for setting up network resources.
            E.g reverge proxy, ssl certs, etc.
    """
    def __init__(self):
        NetworkParser(self)
        super(Network, self).__init__(__file__)

    def execute(self, config, args):
        # TODO: Add ssl certs as secret. Use a component
        super(Network, self).general_deploy(config, args)


instance = Network()
