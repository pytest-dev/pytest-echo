# pytest-echo

[![PyPI](https://img.shields.io/pypi/v/pytest-echo?style=flat-square)](https://pypi.org/project/pytest-echo/)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/pytest-echo.svg)](https://pypi.org/project/pytest-echo/)
[![tests](https://github.com/pytest-dev/pytest-echo/actions/workflows/tests.yml/badge.svg)](https://github.com/pytest-dev/pytest-echo/actions/workflows/tests.yml)
[![Downloads](https://static.pepy.tech/badge/pytest-echo/month)](https://pepy.tech/project/pytest-echo)
[![Coverage](https://codecov.io/gh/pytest-dev/pytest-echo/branch/develop/graph/badge.svg)](https://codecov.io/gh/pytest-dev/pytest-echo)
[![Documentation](https://readthedocs.org/projects/pytest-echo/badge/?version=latest)](https://pytest-echo.readthedocs.io/en/latest/)

Print environment variables, package version and generic attributes,
as they are at the beginning of the test.

Useful in the continuous integration to dump test
configuration/environment and or to check if attributes are properly set
(ie. you change environment with `os.environ`)

## Install

install via::

    pip install pytest-echo
