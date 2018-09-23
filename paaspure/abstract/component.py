# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class AbstractComponent(ABC):
    def __init__(self):
        super(AbstractComponent, self).__init__()

    @abstractmethod
    def build(self):
        """
            This method should implement the logic for running a specific
            compoenent.
        """

    @abstractmethod
    def destroy(self):
        """
            This method should implement the logic for tearing down the
            resources created by run().
        """
