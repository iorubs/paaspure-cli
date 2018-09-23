# -*- coding: utf-8 -*-

import pytest
import yaml
import os
from paaspure.utils import read_file, read_yaml_file, write_yaml_file
import pathlib


def test_normal_file_utils():
    with pytest.raises(FileNotFoundError):
        file_output = read_file('Missing file', 'missing')

    file_output = read_file('setup.py')
    assert "name='paaspure'," in file_output


def test_yaml_file_utils():
    with pytest.raises(yaml.scanner.ScannerError):
        yaml_file_output = read_yaml_file('setup.py', 'setup.py')

    with pytest.raises(FileNotFoundError):
        yaml_file_output = read_yaml_file('Missing file', 'missing')

    with pytest.raises(FileNotFoundError):
        write_yaml_file(['Bad path'], '/dummy loc/test.yml')

    write_yaml_file(['test'], 'test.yml')

    new_yaml_file = pathlib.Path('test.yml')
    assert new_yaml_file.exists()

    yaml_file_output = read_yaml_file('test.yml', 'test.yml')

    assert ['test'] == yaml_file_output

    os.remove('test.yml')
    assert not new_yaml_file.exists()
