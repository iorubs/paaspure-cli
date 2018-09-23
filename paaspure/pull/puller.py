# -*- coding: utf-8 -*-

import os
import sys

from paaspure.utils import validate_name, hub
from paaspure.pull.argparser import PullerParser
from paaspure.pull.utils import clone


class PaaSPurePuller:
    """Module for pulling other modules and components."""
    def __init__(self):
        PullerParser(self)
        super(PaaSPurePuller, self).__init__()

    def run(self, args={}, config={}):
        if args.type == 'all':
            self.__all(config['modules'])
        else:
            if args.type is None:
                self.parser.print_help()
                sys.exit(1)

            if args.NAME is None:
                self.parsers[args.type].print_help()
                sys.exit(1)

            self.__pull_type(args)

    def __all(self, pure_obects):
        for module, module_args in pure_obects.items():
            print('Pulling module', module)
            repo, commit = self.__search_hub(
                name=module,
                type='module',
                args=module_args
            )

            self.__module(
                name=module,
                type='module',
                commit=commit,
                repo_url=repo
            )

            for component, component_args in module_args['components'].items():
                print('Pulling component', component)

                repo, commit = self.__search_hub(
                    name=component,
                    type='component',
                    args=component_args
                )

                self.__component(
                    name=component,
                    parent_module=module,
                    type='component',
                    commit=commit,
                    repo_url=repo
                )

    def __search_hub(self, name=None, type=None, args=None):
        if args is None:
            args = {}

        if 'repo' in args:
            repo = args['repo']
            if 'commit' not in args:
                commit = 'master'
            else:
                commit = args['commit']
        else:
            hub_object = hub.get_object(name, type)
            repo = hub_object['gitUrl']
            if 'tag' not in args:
                args['tag'] = 'latest'

            commit = hub.get_version(hub_object, str(args['tag']))['commit']

        return repo, commit

    def __pull_type(self, args):
        if args.git_url is None:
            hub_object = hub.get_object(args.NAME, args.type)
            args.git_url = hub_object['gitUrl']

            # NOTE: Only get versions for hub objects
            if args.version is not None:
                version = hub.get_version(hub_object, args.version)
                args.version = version['commit']

        if args.type == 'module':
            self.__module(
                name=args.NAME,
                type=args.type,
                commit=args.version,
                repo_url=args.git_url
            )
        else:
            self.__component(
                name=args.NAME,
                parent_module=args.PARENT_MODULE,
                type=args.type,
                commit=args.version,
                repo_url=args.git_url
            )

    def __module(self, name=None, type=None, commit='Master', repo_url=None):
        name = name.lower()
        validate_name(type, name)

        clone(
            repo_url=repo_url,
            type=type,
            commit=commit,
            target_path=[name]
        )

    def __component(self, name=None, parent_module=None, type=None,
                    commit='Master', repo_url=None):
        if parent_module is None:
            self.parsers[type].print_help()
            sys.exit(1)

        name = name.lower()
        validate_name(type, name)
        parent_module = parent_module.lower()
        validate_name('module', parent_module)

        if not os.path.exists(parent_module):
            print(f'Missing module: {parent_module}')
            sys.exit(1)

        clone(
            repo_url=repo_url,
            type=type,
            commit=commit,
            target_path=[parent_module, name]
        )
