# -*- coding: utf-8 -*-

import sys
import importlib

from paaspure.abstract import AbstractModule
from .argparser import InfraBuilderParser


class OrchestratorConnect(AbstractModule):
    """
        Abstraction module for connection to orchestrators.
    """
    def __init__(self):
        InfraBuilderParser(self)
        super(OrchestratorConnect, self).__init__(__file__)

    def execute(self, config, args):
        if args.subcommand is None:
            self.parser.print_help()
            sys.exit(1)

        components = config['modules'][args.command]['components']
        for name, sub_config in components.items():
            component = importlib.import_module(f'{name}')
            # Use dispatch pattern to invoke method with same name
            return getattr(component.instance, args.subcommand)(
                sub_config,
                config['credentials']
            )


instance = OrchestratorConnect()
