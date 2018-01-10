pytest-echo
===========

(https://pypip.in/v/pytest-echo/badge.png)[`target: https://crate.io/packages/pytest-echo/`]

.. image:: https://pypip.in/d/pytest-echo/badge.png
   :target: https://crate.io/packages/pytest-echo/


Print environment variables, package version and generic attributes,
as they are at the begining of the test.

Useful in the continuous integration to dump test
configuration/environment and or to check is attributes are properly set
(ie. you change environment with `os.environ`)

Install
-------

install via::

    pip install pytest-echo



The plugin provides ability to print some extra information prior to run the tests.



Example
-------

Dump environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ py.test --echo-env=HOME
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    HOME: /home/sax
    plugins: echo, pydev, cov, cache, django


Dump package version
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ py.test --echo-version=pytest_echo
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    pytest_echo: 0.1
    plugins: echo, pydev, cov, cache, django

.. warning:: The first attempt to retrieve the version is done via setuptools
    if it fails, the module is imported (``__import__(package)``) to retrieve the version reading
    ``get_version``, ``__version__``, ``VERSION``, ``version`` so any module
    level code is executed. This should be not an issue as no problematic code
    should be present in the first level of the package

Dump attributes
~~~~~~~~~~~~~~~

.. code-block:: sh

    $ py.test --echo-attr=django.conf.settings.DEBUG
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    DEBUG: False
    plugins: echo, pydev, cov, cache, django

.. warning:: Be careful when use ``--echo-attr``. It loads any module in the path and this will
    execute any module level code
    If you try to dump a property, related ``getter`` will be executed.

.. note:: You cannot dump callable result.


Configure via tox.ini/setup.cfg/pytest.cfg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
            --echo-version pytest_echo
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

Links
~~~~~

+--------------------+-------------------------------------------------+
| Project home page: |https://github.com/saxix/pytest-echo             |
+--------------------+-------------------------------------------------+
| Issue tracker:     |https://github.com/saxix/pytest-echo/issues?sort |
+--------------------+-------------------------------------------------+
| Download:          |http://pypi.python.org/pypi/pytest-echo/         |
+--------------------+-------------------------------------------------+
| Documentation:     |https://pytest-echo.readthedocs.org/en/latest/   |
+--------------------+-------------------------------------------------+
