# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractParser
from paaspure.argparser import paaSPureParser


class PullerParser(AbstractParser):
    """PaaSPurePuller argparser"""
    def __init__(self, puller):
        super(PullerParser, self).__init__(__file__)
        self.initialize(puller)

    def initialize(self, puller):
        puller.parser = paaSPureParser.extend_parser(
            f'paaspure {self.name} [OPTIONS] TYPE',
            f'{self.name}',
            'Pull a module or component'
        )

        puller.parser.add_argument(
            '--git-url',
            type=str,
            help='Repo url to pull from.'
        )

        sub_parsers = puller.parser.add_subparsers(
            title='Type',
            dest='type'
        )

        puller.parsers = {}

        puller.parsers['all'] = sub_parsers.add_parser(
            'all',
            help=f'Pull all objects definied in the config file.',
            usage=f'paaspure {self.name} all'
        )

        puller.parsers['module'] = sub_parsers.add_parser(
            'module',
            help=f'Pull module',
            usage=f'paaspure {self.name} module NAME'
        )

        puller.parsers['module'].add_argument(
            'NAME',
            nargs='?',
            type=str,
            help='The module name'
        )

        puller.parsers['module'].add_argument(
            '--version',
            type=str,
            help='Module version'
        )

        puller.parsers['module']._optionals.title = 'Options'
        puller.parsers['module']._positionals.title = 'Arguments'
        puller.parsers['module'].set_defaults(module_parser=True)

        puller.parsers['component'] = sub_parsers.add_parser(
            'component',
            help='Pull component',
            usage=f'paaspure {self.name} component PARENT_MODULE NAME'
        )

        puller.parsers['component'].add_argument(
            'PARENT_MODULE',
            nargs='?',
            type=str,
            help='The parent module name'
        )

        puller.parsers['component'].add_argument(
            'NAME',
            nargs='?',
            type=str,
            help='The component name'
        )

        puller.parsers['component'].add_argument(
            '--version',
            type=str,
            help='Module version'
        )

        puller.parsers['component']._optionals.title = 'Options'
        puller.parsers['component']._positionals.title = 'Arguments'
        puller.parsers['component'].set_defaults(new_parser=True)
