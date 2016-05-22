#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import techfugees
version = techfugees.__version__

setup(
    name='techfugees',
    version=version,
    author='',
    author_email='letoosh@gmail.com',
    packages=[
        'techfugees',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.1',
    ],
    zip_safe=False,
    scripts=['techfugees/manage.py'],
)
