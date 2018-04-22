===========
pytest-echo
===========


.. image:: https://badge.fury.io/py/pytest-echo.svg
   :target: http://badge.fury.io/py/pytest-echo
   :alt: PyPI package


Print environment variables, package version and generic attributes,
as they are at the begining of the test.

Useful in the continuous integration to dump test
configuration/environment and or to check if attributes are properly set
(ie. you change environment with `os.environ`)


Install
=======

install via::

    pip install pytest-echo



Examples
========

Dump environment variables
--------------------------

.. code-block:: sh

    $ py.test --echo-env=HOME
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    Environment:
        HOME: /Users/sax
    plugins: echo, pydev, cov, cache, django


Dump package version
--------------------

.. code-block:: sh

    $ py.test --echo-version=pytest_echo
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    Package version:
        pytest_echo: 0.1
    plugins: echo, pydev, cov, cache, django


.. warning:: The first attempt to retrieve the version is done via setuptools
    if it fails, the module is imported (``__import__(package)``) to retrieve the version reading
    ``get_version``, ``__version__``, ``VERSION``, ``version`` so any module
    level code is executed. This should be not an issue as no problematic code
    should be present in the first level of the package

Dump attributes
---------------

.. code-block:: sh

    $ py.test --echo-attr=django.conf.settings.DEBUG
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    Inspections
        django.conf.settings.DEBUG: False
    plugins: echo, pydev, cov, cache, django

.. warning:: Be careful when use ``--echo-attr``. It loads any module in the path and this will
    execute any module level code
    If you try to dump a property, related ``getter`` will be executed.

.. note:: You cannot dump callable result.


Configure via tox.ini/setup.cfg/pytest.cfg
------------------------------------------

Example of use in a django project:

.. code-block:: inifile

    [pytest]
    addopts = -vvv
            --tb=short
            --capture=no
            --echo-env PWD
            --echo-env VIRTUAL_ENV
            --echo-env DBENGINE
            --echo-version django
            --echo-version pip
            --echo-version pytest-echo
            --echo-attr django.conf.settings.DATABASES.default.ENGINE



.. code-block:: sh

    $ py.test
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    Environment:
        DJANGO_SETTINGS_MODULE: tests.settings
        PWD: /data/PROGETTI/sem
        VIRTUAL_ENV: /data/VENV/sem
        DBENGINE: <not set>
    Package version:
        django: 1.6.5
        pip: 1.5.6
        pytest_echo: 1.2
    Inspections:
        django.conf.settings.DATABASES.default.ENGINE: 'django.db.backends.postgresql_psycopg2'
    plugins: echo, cache, capturelog, contextfixture, cov, django, pydev
    collected 14 items
    .............
    14 passed in 4.95 seconds


Globbing
--------

Starting from version 1.5, is possible to glob packages version and environment variables,
as:

.. code-block:: sh

    $ py.test --echo-version=pytest-* --echo-env=VIRTUAL*

or

.. code-block:: inifile

    [pytest]
    addopts = -vvv
            --echo-env VIRTUAL*
            --echo-version pytest-*




Links
-----

+--------------------+-----------------+---------------+----------------+
| Stable             |  |master-build| |  |master-cov| |  |master-doc|  |
+--------------------+-----------------+---------------+----------------+
| Development        |  |dev-build|    |  |dev-cov|    |  |dev-doc|     |
+--------------------+-----------------+---------------+----------------+
| Project home page: | https://github.com/saxix/pytest-echo             |
+--------------------+--------------------------------------------------+
| Issue tracker:     | https://github.com/saxix/pytest-echo/issues?sort |
+--------------------+--------------------------------------------------+
| CI:                | https://travis-ci.org/saxix/pytest-echo          |
+--------------------+--------------------------------------------------+
| Download:          | http://pypi.python.org/pypi/pytest-echo/         |
+--------------------+--------------------------------------------------+
| Documentation:     | https://pytest-echo.readthedocs.org/en/latest/   |
+--------------------+--------------------------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/saxix/pytest-echo.png?branch=master
                    :target: http://travis-ci.org/saxix/pytest-echo/

.. |master-cov| image:: https://codecov.io/gh/saxix/pytest-echo/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/saxix/pytest-echo

.. |master-doc| image:: https://readthedocs.org/projects/pytest-echo/badge/?version=stable
                    :target: http://pytest-echo.readthedocs.io/en/stable/

.. |dev-build| image:: https://secure.travis-ci.org/saxix/pytest-echo.png?branch=develop
                  :target: http://travis-ci.org/saxix/pytest-echo/

.. |dev-cov| image:: https://codecov.io/gh/saxix/pytest-echo/branch/develop/graph/badge.svg
                :target: https://codecov.io/gh/saxix/pytest-echo

.. |dev-doc| image:: https://readthedocs.org/projects/pytest-echo/badge/?version=latest
                :target: http://pytest-echo.readthedocs.io/en/latest/

