# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractModule
from .argparser import InfraBuilderParser


class InfraBuilder(AbstractModule):
    """
        Abstraction module for components used to run the cloud infrastructure.
    """
    def __init__(self):
        InfraBuilderParser(self)
        super(InfraBuilder, self).__init__(__file__)

    def execute(self, config, args):
        super(InfraBuilder, self).general_execute(config, args)


instance = InfraBuilder()
