# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractModule
from .argparser import VmBuilderParser


class VmBuilder(AbstractModule):
    """Abstraction module for components used to build cloud images."""
    def __init__(self):
        VmBuilderParser(self)
        super(VmBuilder, self).__init__(__file__)

    def execute(self, config, args):
        super(VmBuilder, self).general_execute(config, args)


instance = VmBuilder()
