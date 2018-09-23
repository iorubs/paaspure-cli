# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractModule
from .argparser import ServiceDeployerParser


class ServiceDeployer(AbstractModule):
    """
        Abstraction module for deploying general components.
    """
    def __init__(self):
        ServiceDeployerParser(self)
        super(ServiceDeployer, self).__init__(__file__)

    def execute(self, config, args):
        super(ServiceDeployer, self).general_deploy(config, args)


instance = ServiceDeployer()
