# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from paaspure.utils import get_version, read_file

setup(
    name='paaspure',
    version=get_version(),
    description='A tool for building the PaaS of the future.',
    long_description=read_file(
        os.path.abspath(os.path.dirname(__file__)),
        'README.md'
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: DevOps & Platform',
        'License :: Unkown for now',
        'Topic :: System :: Installation/Setup',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='paas caas',
    author='Ruben Vasconcelos',
    author_email='ruben.vasconcelos3@mail.dcu.ie',
    url='None yet',
    license='MIT hopefully',
    packages=find_packages(
        exclude=['docs', 'tests*']
    ),
    entry_points={
        'console_scripts': [
            'paaspure = paaspure.__main__:main'
        ],
    },
    zip_safe=False,
    python_requires='>=3.0',
    extras_require={
        'testing': ['pytest'],
    },
)
