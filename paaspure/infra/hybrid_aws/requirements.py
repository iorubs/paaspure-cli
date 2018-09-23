# -*- coding: utf-8 -*-

from paaspure.utils import pip_install

pip_packages = [
    'docker'
]


def install():
    pip_install(packages=pip_packages, component='TerraformAWS')


install()
