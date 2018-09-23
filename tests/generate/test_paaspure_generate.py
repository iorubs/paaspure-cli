# -*- coding: utf-8 -*-

import os
import shutil
import pytest

from paaspure import settings
from paaspure.argparser import paaSPureParser
from paaspure.generate import PaaSPureGenerator


invalid_names = [
    '1',
    '_test',
    'test_',
    'test_1',
    'as@#asd',
    'test1test'
]


@pytest.fixture(scope="module")
def generator_setup():
    """ Setup state specific to the execution of the module."""
    PaaSPureGenerator()


@pytest.fixture(scope="function")
def module_name():
    """ New module name and cleanup work."""
    new_module = 'test_module'
    yield new_module
    shutil.rmtree(new_module, ignore_errors=True)


@pytest.mark.usefixtures("generator_setup")
class TestPaaSPureGenerator:
    def test_extended_generic_parser(self, capsys):
        with pytest.raises(SystemExit):
            PaaSPureGenerator().run(
                paaSPureParser.parser.parse_args(['generate'])
            )

        with pytest.raises(SystemExit):
            PaaSPureGenerator().run(
                paaSPureParser.parser.parse_args(['generate', 'module'])
            )

        with pytest.raises(SystemExit):
            PaaSPureGenerator().run(
                paaSPureParser.parser.parse_args(['generate', 'component'])
            )

        out, _ = capsys.readouterr()
        assert 'usage: paaspure generate TEMPLATE' in out
        assert 'paaspure generate module NAME' in out
        assert 'paaspure generate component PARENT_MODULE NAME' in out

    def test_generate_module(self, capsys, module_name):
        args = paaSPureParser.parser.parse_args([
            'generate', 'module', module_name
        ])

        assert args.command == 'generate'
        assert args.template == 'module'
        assert args.NAME == module_name

        PaaSPureGenerator().run(args)

        assert os.path.exists(module_name)

        # Check that all files were generated.
        component_templates = os.listdir(os.path.join(
            settings.PROJECT_ROOT,
            'generate',
            'templates',
            'module'
        ))

        for template in component_templates:
            assert os.path.exists(os.path.join(
                module_name,
                '.'.join(template.split('-'))
            ))

        # Test: Trying to create module with existing name raises exeception.
        with pytest.raises(SystemExit):
            PaaSPureGenerator().run(args)

        out, _ = capsys.readouterr()
        assert f'Module {module_name}, already exists.' in out

    def test_generate_component(self, module_name):
        args = paaSPureParser.parser.parse_args([
            'generate', 'component', module_name, module_name
        ])

        assert args.command == 'generate'
        assert args.template == 'component'
        assert args.PARENT_MODULE == module_name
        assert args.NAME == module_name

        PaaSPureGenerator().run(args)
        # TODO: Finish component implementation and asserts

    @pytest.mark.parametrize("name", invalid_names)
    def test_invalid_names(self, capsys, name):
        args = paaSPureParser.parser.parse_args([
            'generate', 'module', name
        ])

        assert args.command == 'generate'
        assert args.template == 'module'
        assert args.NAME == name

        with pytest.raises(SystemExit):
            PaaSPureGenerator().run(args)

        out, _ = capsys.readouterr()
        assert 'Valid names must:' in out
        assert not os.path.exists(name)
