# -*- coding: utf-8 -*-

import re
import sys
from paaspure.__init__ import __version__


def get_version():
    return __version__


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def validate_name(type, name):
    if re.match('^[a-z]+(_[a-z]+)*$', name) is None:
        print(f'Invalid {type} name: {name}')
        print('Valid names must:')
        print('\tConsist of only letters and underscores.')
        print('\tStart and finish with a letter.')

        print(f'E.g: {type}_name')

        sys.exit(1)
