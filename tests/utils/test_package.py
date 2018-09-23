# -*- coding: utf-8 -*-

import pytest
import subprocess
import sys
import importlib
from paaspure.utils import pip_install
from paaspure import settings
from io import StringIO


@pytest.fixture(scope="function")
def dummy_package():
    package = 'dummy-yummy'
    yield [package, 'yummy']
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'uninstall', '-y', package]
    )


def test_pip_install_quiet(dummy_package):
    with pytest.raises(ImportError):
        importlib.__import__(dummy_package[1])

    pip_install(packages=[dummy_package[0]], component='Test')

    try:
        importlib.__import__(dummy_package[1])
    except ImportError:
        raise pytest.fail('Package not found.')


def test_pip_install(capsys, dummy_package):
    settings.QUIET_INSTALL = False

    sys.stdin = StringIO('random_gib')
    with pytest.raises(SystemExit):
        pip_install(packages=[dummy_package[0]], component='Test')

    out, _ = capsys.readouterr()
    assert 'respond with' in out

    sys.stdin = StringIO('no')
    with pytest.raises(SystemExit):
        pip_install(packages=[dummy_package[0]], component='Test')

    out, _ = capsys.readouterr()
    assert 'let me install' in out
