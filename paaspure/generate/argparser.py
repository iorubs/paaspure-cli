# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractParser
from paaspure.argparser import paaSPureParser


class GeneratorParser(AbstractParser):
    """Template generator, for adding code scaffolding."""
    def __init__(self, generator):
        super(GeneratorParser, self).__init__(__file__)
        self.initialize(generator)

    def initialize(self, generator):
        generator.parser = paaSPureParser.extend_parser(
            f'paaspure {self.name} TEMPLATE',
            f'{self.name}',
            'Generate templates.'
        )

        sub_parsers = generator.parser.add_subparsers(
            title='Templates',
            dest='template'
        )

        generator.module_parser = sub_parsers.add_parser(
            'module',
            help='Generate template for a new module.',
            usage=f'paaspure {self.name} module NAME'
        )

        generator.module_parser.add_argument(
            'NAME',
            nargs='?',
            type=str,
            help='The name of the new module.'
        )

        generator.module_parser._optionals.title = 'Options'
        generator.module_parser._positionals.title = 'Arguments'
        generator.module_parser.set_defaults(module_parser=True)

        generator.component_parser = sub_parsers.add_parser(
            'component',
            help='Generate template for a new component.',
            usage=f'paaspure {self.name} component PARENT_MODULE NAME'
        )

        generator.component_parser.add_argument(
            'PARENT_MODULE',
            nargs='?',
            type=str,
            help='The name of the parent module.'
        )

        generator.component_parser.add_argument(
            'NAME',
            nargs='?',
            type=str,
            help='The name of the new component.'
        )

        generator.component_parser._optionals.title = 'Options'
        generator.component_parser._positionals.title = 'Arguments'
        generator.component_parser.set_defaults(new_parser=True)
