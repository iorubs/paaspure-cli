# -*- coding: utf-8 -*-

import argparse

from paaspure.utils import get_version


class PaaSPureParser:
    """Genereic parser to be extended by sub-modules."""
    def __init__(self):
        self.create_parser()
        super(PaaSPureParser, self).__init__()

    def create_parser(self):
        self.parser = argparse.ArgumentParser(
            description='PaaSPure build the Paas of the future.',
            usage='paaspure command',
            add_help=False
        )

        self.parser._optionals.title = 'Options'

        self.parser.add_argument('-f', '--file', default='pure.yml', type=str,
                                 help="Name of the cofig file \
                                 (Default is 'PATH/pure.yml').")

        self.parser.add_argument('-h', '--help', action='help',
                                 default=argparse.SUPPRESS,
                                 help='Show this help message and exit.')

        self.parser.add_argument('-v', '--verbose', action='store_true',
                                 help='Debug mode.')

        self.parser.add_argument('--version', action='version',
                                 version=f'%(prog)s {get_version()}',
                                 help='Show version number and exit.')

        self.parser._positionals.title = 'Management Commands'

        self.subparsers = self.parser.add_subparsers(
            title='commands',
            dest='command'
        )

        self.extend_parser(
            f'paaspure build',
            f'build',
            'Build all PureObjects.'
        )

        self.extend_parser(
            f'paaspure destroy',
            f'destroy',
            'Destroy all PureObjects.'
        )

    def extend_parser(self, usage, command, help_msg):
        new_parser = self.subparsers.add_parser(
            command,
            help=help_msg,
            usage=usage
        )

        new_parser._optionals.title = 'Options'
        new_parser._positionals.title = 'Commands'
        new_parser.set_defaults(new_parser=True)

        return new_parser


paaSPureParser = PaaSPureParser()
