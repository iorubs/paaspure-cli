# -*- coding: utf-8 -*-

import sys
import os
import importlib
from abc import ABC, abstractmethod


class AbstractModule(ABC):
    def __init__(self, filename=__file__):
        sys.path.append(os.path.dirname(filename))
        super(AbstractModule, self).__init__()

    @abstractmethod
    def execute(self):
        """
            This method should implement how to run the module. Think of it
            as a layer of abstraction that implements the logic needed to
            setup, run and clean up after components.
        """

    def general_execute(self, config, args):
        if args.subcommand is None:
            self.parser.print_help()
            sys.exit(1)

        components = config['modules'][args.command]['components']
        for name, sub_config in components.items():
            try:
                component = importlib.import_module(f'{name}')
                # Use dispatch pattern to invoke method with same name
                getattr(component.instance, args.subcommand)(
                    sub_config,
                    config['credentials']
                )
            except ModuleNotFoundError:
                self._general_err(args, name)

    def general_deploy(self, config, args):
        if args.subcommand is None:
            self.parser.print_help()
            sys.exit(1)

        orchestrator = importlib.import_module(
            config['modules'][args.command]['orchestrator']
        ).instance

        components = config['modules'][args.command]['components']
        component_command = args.subcommand
        for name, sub_config in components.items():
            try:
                component = importlib.import_module(f'{name}').instance

                args.subcommand = 'client_connection'
                args.command = 'orchestrator'

                with orchestrator.execute(config, args) as client:
                    # Use dispatch pattern to invoke method with same name
                    getattr(component, component_command)(
                        sub_config,
                        client
                    )
            except ModuleNotFoundError:
                self._general_err(args, name)

    def _general_err(self, args, name):
        print(
            f"No component named '{name}' in module '{args.command}'"
        )
        print('To import an existing component run:')
        print(f'\tpaaspure pull component {args.command} {name}')
        print(f'\tpaaspure pull all')
        print('To create a new component run:')
        print(f'\tpaaspure generate component {args.command} {name}')
        sys.exit(1)
