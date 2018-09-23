# -*- coding: utf-8 -*-

from paaspure.utils import pip_install

pip_packages = [
    'docker',
    'boto3'
]


def install():
    pip_install(packages=pip_packages, component='PackerAWS')


install()
