# -*- coding: utf-8 -*-

from paaspure.utils import pip_install, apk_install

pip_packages = [
    'boto3'
]

apk_packages = [
    'openssh'
]


def install():
    pip_install(packages=pip_packages, component='SwarmAWS')
    apk_install(packages=apk_packages, component='SwarmAWS')


install()
