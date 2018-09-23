# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractModule
from .argparser import LogManagementParser


class LogManagement(AbstractModule):
    """
        Abstraction module for deploying general components.
    """
    def __init__(self):
        LogManagementParser(self)
        super(LogManagement, self).__init__(__file__)

    def execute(self, config, args):
        super(LogManagement, self).general_deploy(config, args)


instance = LogManagement()
