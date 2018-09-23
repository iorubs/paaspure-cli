# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractModule
from .argparser import MonitoringParser


class Monitoring(AbstractModule):
    """
        Abstraction module for Monitoring service and infrastructure.
    """
    def __init__(self):
        MonitoringParser(self)
        super(Monitoring, self).__init__(__file__)

    def execute(self, config, args):
        super(Monitoring, self).general_deploy(config, args)


instance = Monitoring()
