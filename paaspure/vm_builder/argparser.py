# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractParser
from paaspure.argparser import paaSPureParser


class VmBuilderParser(AbstractParser):
    """New auto-generated modulo argparse template."""
    def __init__(self, module):
        super(VmBuilderParser, self).__init__(__file__)
        self.initialize(module)

    def initialize(self, module):
        module.parser = paaSPureParser.extend_parser(
            f'paaspure {self.name} COMMAND',
            f'{self.name}',
            'Build cloud images.'
        )

        sub_parsers = module.parser.add_subparsers(
            title='Commands',
            dest='subcommand'
        )

        module.run_parser = sub_parsers.add_parser(
            'build',
            help='Run the VmBuilder module.',
            usage=f'paaspure {self.name} run'
        )

        module.run_parser = sub_parsers.add_parser(
            'destroy',
            help='Destroy VmBuilder resources.',
            usage=f'paaspure {self.name} destroy'
        )

        module.run_parser._optionals.title = 'Options'
        module.run_parser._positionals.title = 'Commands'
        module.run_parser.set_defaults(parser=True)
