# -*- coding: utf-8 -*-

from paaspure.abstract import AbstractComponent


class DummyComponent(AbstractComponent):
    """Dummy Component"""
    def __init__(self):
        super(DummyComponent, self).__init__()

    def build(self, config, credentials):
        print('Dummy run.')
        return True

    def destroy(self, config, credentials):
        print('Dummy destroy.')
        return True


instance = DummyComponent()
