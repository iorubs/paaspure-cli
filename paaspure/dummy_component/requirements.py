# -*- coding: utf-8 -*-

from paaspure.utils import pip_install


def install():
    print('Dummy install')
    pip_install(packages=[], component='DummyComponent')


install()
