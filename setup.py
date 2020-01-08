#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from pytest_echo import __version__

setup(
    name='pytest-echo',
    description='pytest plugin with mechanisms for echoing environment '
                'variables, package version and generic attributes',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    version=__version__,
    author='Stefano Apostolico',
    author_email='s.apostolico@gmail.com',
    url='https://github.com/pytest-dev/pytest-echo',
    py_modules=['pytest_echo'],
    entry_points={'pytest11': ['echo = pytest_echo']},
    install_requires=['pytest>=2.2'],
    license="MIT License",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ])
