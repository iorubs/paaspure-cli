# -*- coding: utf-8 -*-

from paaspure.utils import pip_install, apk_install

pip_packages = [
    'azure',
    'keyrings.alt'
]

apk_packages = [
    'openssh',
    'build-base',
    'libffi-dev',
    'openssl-dev'
]


def install():
    apk_install(packages=apk_packages, component='SwarmAzure')
    pip_install(packages=pip_packages, component='SwarmAzure')


install()
