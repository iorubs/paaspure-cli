# -*- coding: utf-8 -*-

import os
import sys

from paaspure.utils import validate_name
from paaspure.generate.argparser import GeneratorParser
from jinja2 import Environment, FileSystemLoader


class PaaSPureGenerator:
    """Template generator, for adding code scaffolding."""
    def __init__(self):
        GeneratorParser(self)
        super(PaaSPureGenerator, self).__init__()

    def run(self, args):
        if args.template is None or not hasattr(self, args.template):
            self.parser.print_help()
            sys.exit(1)

        # Use dispatch pattern to invoke method with same name
        getattr(self, args.template)(args)

    def module(self, args):
        if args.NAME is None:
            self.module_parser.print_help()
            sys.exit(1)

        name = args.NAME.lower()
        validate_name(args.template, name)
        capitalized_name = self.__capitalize_name(name)

        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'module'
        )

        target_path = os.path.join(os.getcwd(), name)

        self.__generate_target_files(
            template_path,
            target_path,
            name,
            capitalized_name
        )

    def component(self, args):
        if args.PARENT_MODULE is None or args.NAME is None:
            self.component_parser.print_help()
            sys.exit(1)

        # generate new compoenent source files

    def __capitalize_name(self, name):
        split_name = name.split('_')

        capitalized_name = ''

        for token in split_name:
            capitalized_name += token.capitalize()

        return capitalized_name

    def __generate_target_files(self, template_path, target_path, name,
                                capitalized_name):
        try:
            os.mkdir(target_path)
        except FileExistsError:
            print(f'Module {name}, already exists.')
            sys.exit(1)

        # Create the jinja2 environment.
        j2_env = Environment(
            loader=FileSystemLoader(template_path),
            trim_blocks=True
        )

        for template in j2_env.list_templates():
            j2_env.get_template(template).stream(
                module=name,
                module_capitalized=capitalized_name,
                new_line=''
            ).dump(
                os.path.join(target_path, '.'.join(template.split('-')))
            )
