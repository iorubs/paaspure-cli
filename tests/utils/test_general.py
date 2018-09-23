# -*- coding: utf-8 -*-

from paaspure.utils import get_version, escape_ansi
from paaspure.__init__ import __version__


def test_get_version():
    assert get_version() == __version__


def test_escape_ansi():
    expected = '\tTestAnsi\n'
    ansi_encoded_line = '\t\u001b[0;35mTestAnsi\u001b[0m\n'
    actual = escape_ansi(ansi_encoded_line)

    assert expected == actual
