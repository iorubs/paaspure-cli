# -*- coding: utf-8 -*-

import sys
import importlib

from paaspure import settings
from paaspure.argparser import paaSPureParser
from paaspure.generate import PaaSPureGenerator
from paaspure.pull import PaaSPurePuller
from paaspure.utils import read_yaml_file


def main(args=None):
    # TODO: This is a bit hacky, fix initial parser.
    config_file = 'pure.yml'
    if '-f' in sys.argv:
        config_file = sys.argv[sys.argv.index('-f') + 1]
    elif '--file' in sys.argv:
        config_file = sys.argv[sys.argv.index('--file') + 1]

    if '-v' in sys.argv or '--verbose' in sys.argv:
        settings.DEBUG = '-v' in sys.argv

    config = read_yaml_file(
        'config',
        config_file
    )

    if 'hub' in config:
        settings.HUB = config['hub']

    args = __extend_paaspure_parser(config)
    __run_command(config, args)


def __extend_paaspure_parser(config):
    PaaSPurePuller()
    PaaSPureGenerator()

    if 'modules' in config and config['modules'] is not None:
        for module in config['modules']:
            try:
                importlib.import_module(module)
            except ModuleNotFoundError as err:
                args = paaSPureParser.parser.parse_args(sys.argv[1:])

                if args.command != 'generate' and args.command != 'pull':
                    print(err)
                    print('To import an existing module run:')
                    print(f'\tpaaspure pull module {module}')
                    print(f'\tpaaspure pull all')
                    print('To create a new module run:')
                    print(f'\tpaaspure generate module {module}')
                    sys.exit(1)

    return paaSPureParser.parser.parse_args(sys.argv[1:])


def __run_command(config, args):
    if args.command == 'generate':
        PaaSPureGenerator().run(args)
    elif args.command == 'pull':
        PaaSPurePuller().run(args, config)
    elif args.command == 'build' or args.command == 'destroy':
        # NOTE: use temp command in case modules modify args. Fine for now but
        # there must be a cleaner version (maybe suply modules with deep copy)
        command = args.command

        if args.command == 'build':
            modules = list(config['modules'].keys())
        else:
            modules = reversed(list(config['modules'].keys()))

        for module in modules:
            args.command = module
            args.subcommand = command
            module = importlib.import_module(args.command)
            module.instance.execute(config, args)
    elif args.command is not None:
        module = importlib.import_module(args.command)
        module.instance.execute(config, args)
    else:
        paaSPureParser.parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
