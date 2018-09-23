# -*- coding: utf-8 -*-

import os
import sys


DEBUG = False
PROJECT_ROOT = os.path.dirname(__file__)

if 'pytest' in sys.modules:
    QUIET_INSTALL = True
else:
    QUIET_INSTALL = False

HUB = 'https://paaspure.com'
