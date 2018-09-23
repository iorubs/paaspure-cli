# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod


class AbstractParser(ABC):
    def __init__(self, filename=__file__):
        self.name = os.path.basename(os.path.dirname(filename)),
        self.name = ''.join(self.name)
        super(AbstractParser, self).__init__()

    @abstractmethod
    def initialize(self):
        """
            This method should implement the module parser.
        """
