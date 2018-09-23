# -*- coding: utf-8 -*-

import os
import yaml


def read_yaml_file(description='yaml', *path):
    try:
        with open(os.path.join(*path), 'r') as f:
            return yaml.load(f)
    except FileNotFoundError as err:
        print(f'Missing {description} file: {os.path.join(*path)}')
        raise
    except yaml.scanner.ScannerError as yaml_err:
        print('Invalid YAML file:')
        print(yaml_err)
        raise


def write_yaml_file(output, *path):
    try:
        with open(os.path.join(*path), 'w') as outfile:
            yaml.dump(output, outfile, default_flow_style=False)
    except Exception as err:
        print(f'Could not create new YAML file: {os.path.join(*path)}')
        print(err)
        raise


def read_file(*path):
    try:
        with open(os.path.join(*path), 'r') as fp:
            return fp.read()
    except FileNotFoundError as err:
        print(f'Missing file: {os.path.join(*path)}')
        raise
