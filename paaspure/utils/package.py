# -*- coding: utf-8 -*-

import sys
import importlib
import subprocess
from paaspure import settings


def pip_install(packages=None, component=None):
    print(f'Checking pip dependecies: {component}')

    missing = []
    for package in packages:
        try:
            importlib.__import__(package)
        except ImportError:
            missing.append(package)

    __run_install([sys.executable, '-m', 'pip', 'install'], missing)


def apk_install(packages=None, component=None):
    print(f'Checking apk dependecies: {component}')

    installed = subprocess.check_output(['apk', 'info']).decode().split()
    missing = [package for package in packages if package not in installed]
    __run_install(['apk', 'add'], missing)


def __run_install(command, missing):
    if len(missing) != 0:
        print(f'Install missing dependecies:')
        print(missing)

        request_input(
            question='Do you want to continue? [Y/n] ',
            reject='\tY U NOT let me install? (/ಠ,ಠ)/'
        )

        if not settings.DEBUG:
            command.append('-q')
        subprocess.check_call(command + missing)


def request_input(**kwargs):
    print(kwargs['question'], end='')

    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    choice = 'yes' if settings.QUIET_INSTALL else input().lower()

    if choice in yes:
        return
    elif choice in no:
        print(kwargs['reject'])
        sys.exit(1)
    else:
        print("\tPlease respond with 'yes' or 'no'")
        sys.exit(1)
