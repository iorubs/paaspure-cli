# -*- coding: utf-8 -*-

import pytest
from paaspure.argparser import paaSPureParser
from .module import instance


class TestVmBuilder:
    def test_vm_builder_execution(self, capsys):
        # NOTE: Need a better way to do this.
        module_name = __name__.split('.')[-2]

        config = {
            'version': 1,
            'credentials': {},
            'modules': {
                module_name: {
                    'components': {
                        'paaspure.dummy_component': {}
                    }
                }
            }
        }

        args = paaSPureParser.parser.parse_args([
            module_name
        ])
        with pytest.raises(SystemExit):
            instance.execute(config, args)

        out, _ = capsys.readouterr()
        assert f'paaspure {module_name} COMMAND' in out

        args.subcommand = 'build'
        instance.execute(config, args)
        out, _ = capsys.readouterr()
        assert 'Dummy run.' in out

        args.subcommand = 'destroy'
        instance.execute(config, args)
        out, _ = capsys.readouterr()
        assert 'Dummy destroy.' in out
