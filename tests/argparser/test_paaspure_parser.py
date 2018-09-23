# -*- coding: utf-8 -*-

import argparse
import pytest
from paaspure.argparser import paaSPureParser


def test_generic_parser(capsys):
    assert isinstance(paaSPureParser.parser, argparse.ArgumentParser)

    args = paaSPureParser.parser.parse_args([])
    assert args.file == 'pure.yml'

    args = paaSPureParser.parser.parse_args(['--file', 'test'])
    assert args.file == 'test'

    with pytest.raises(SystemExit):
        paaSPureParser.parser.parse_args(['-h'])

    out, _ = capsys.readouterr()
    assert 'PaaSPure build the Paas of the future.' in out


def test_can_extend_parser():
    paaSPureParser.parser.add_argument('--unit_test', type=str)

    args = paaSPureParser.parser.parse_args([
        '--unit_test', 'test'
    ])

    assert args.unit_test == 'test'
