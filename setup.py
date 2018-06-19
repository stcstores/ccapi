#!/usr/bin/env python
"""Setup for the ccapi package."""

from setuptools import find_packages, setup

setup(
    name='ccapi',
    version='0.0.1',
    description='Cloud Commerce Pro API integration.',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    install_requires=['requests', 'beautifulsoup4'],
    packages=find_packages(),
)
