#!/usr/bin/env python
from setuptools import setup
from importlib import metadata

setup(
    description="pytest plugin with mechanisms for echoing environment "
    "variables, package version and generic attributes",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    version="1.8.1",
    author="Stefano Apostolico",
    author_email="s.apostolico@gmail.com",
    url="https://github.com/pytest-dev/pytest-echo",
    py_modules=["pytest_echo"],
    entry_points={"pytest11": ["echo = pytest_echo"]},
    install_requires=["pytest>=6.0"],
    license="MIT License",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
