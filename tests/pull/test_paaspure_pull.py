# -*- coding: utf-8 -*-

import os
import shutil
import pytest

from paaspure.argparser import paaSPureParser
from paaspure.pull import PaaSPurePuller


@pytest.fixture(scope="module")
def pull_setup():
    """ Setup state specific to the execution of the module."""
    PaaSPurePuller()


@pytest.fixture(scope="function")
def pulled_module():
    """ New module name and cleanup work."""
    module_url = 'git@github.com:iorubs/paaspure_vm_builder.git'
    module_name = 'test_module'
    yield [module_url, module_name]
    shutil.rmtree(module_name, ignore_errors=True)
    shutil.rmtree('tests/' + module_name + '_tests', ignore_errors=True)


# TODO: Update tests after the central hub is implemented.
@pytest.mark.usefixtures("pull_setup")
class TestPaaSPurePuller:
    def test_extended_generic_parser(self, capsys):
        with pytest.raises(SystemExit):
            PaaSPurePuller().run(
                args=paaSPureParser.parser.parse_args(['pull']),
                config={}
            )

        with pytest.raises(SystemExit):
            PaaSPurePuller().run(
                args=paaSPureParser.parser.parse_args(
                    ['pull', '--git-url', 'some_url', 'module']
                ),
                config={}
            )

        with pytest.raises(SystemExit):
            PaaSPurePuller().run(
                args=paaSPureParser.parser.parse_args(
                    ['pull', '--git-url', 'some_url', 'component']
                ),
                config={}
            )

        out, _ = capsys.readouterr()
        assert 'usage: paaspure pull [OPTIONS] TYPE' in out
        assert 'paaspure pull module NAME' in out
        assert 'paaspure pull component PARENT_MODULE NAME' in out

    @pytest.mark.skip(reason="Repos are currently private.")
    def test_pull_module(self, capsys, pulled_module):
        args = paaSPureParser.parser.parse_args([
            'pull', '--git-url', pulled_module[0], 'module', pulled_module[1]
        ])

        assert args.command == 'pull'
        assert args.type == 'module'
        assert args.NAME == pulled_module[1]

        PaaSPurePuller().run(args)

        assert os.path.exists(pulled_module[1])
        assert os.path.exists('tests/' + pulled_module[1] + '_tests')

        # Test: Trying to create module with existing name raises exeception.
        PaaSPurePuller().run(args)

        out, _ = capsys.readouterr()
        assert f'Found existing module {pulled_module[1]}:' in out

    @pytest.mark.skip(reason="Repos are currently private.")
    def test_pull_component(self, capsys, pulled_module):
        component_args = paaSPureParser.parser.parse_args([
            'pull',
            '--git-url',
            'git@github.com:iorubs/paaspure_packer_aws.git',
            'component',
            pulled_module[1],
            pulled_module[1],
        ])

        assert component_args.command == 'pull'
        assert component_args.type == 'component'
        assert component_args.PARENT_MODULE == pulled_module[1]
        assert component_args.NAME == pulled_module[1]

        with pytest.raises(SystemExit):
            PaaSPurePuller().run(component_args)

        out, _ = capsys.readouterr()
        assert 'Missing module: ' in out

        module_args = paaSPureParser.parser.parse_args([
            'pull', '--git-url', pulled_module[0], 'module', pulled_module[1]
        ])

        PaaSPurePuller().run(module_args)
        PaaSPurePuller().run(component_args)
        assert os.path.exists(pulled_module[1] + '/' + pulled_module[1])
        module_test_folder = pulled_module[1] + '_tests/'
        component_test_folder = module_test_folder + module_test_folder
        assert os.path.exists('tests/' + component_test_folder)
