#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='ccapi',
    version='0.0.1',
    description='Wrapper for Cloud Commerce Pro API',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    install_requires=['requests', 'beautifulsoup4'],
    packages=find_packages(),
    )
