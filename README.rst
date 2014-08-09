pytest-echo
===========


.. image:: https://pypip.in/v/pytest-echo/badge.png
   :target: https://crate.io/packages/pytest-echo/

.. image:: https://pypip.in/d/pytest-echo/badge.png
   :target: https://crate.io/packages/pytest-echo/


Print environment variables, package version and generic attributes.

Useful in the continuous integration to dump test configuration/environment.


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


Dump attributes
~~~~~~~~~~~~~~~

.. code-block:: sh

    $ py.test --echo-attr=django.conf.settings.DEBUG
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    DEBUG: False
    plugins: echo, pydev, cov, cache, django

.. warning:: Be careful when use ``--echo-attr``. It load any module in the path and this will
    execute any module's level code
    If you try to dump a property, related ``getter`` will be executed.

.. note:: You cannot dump callable result.


Configure via tox.ini/setup.cfg/pytest.cfg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example of use in a django project:

.. code-block:: inifile

    [pytest]
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
        PWD: /data/PROGETTI/ONU_WorldFoodProgramme/wfp-auth
        VIRTUAL_ENV: /data/VENV/sem
        DBENGINE: <not set>
    Package version:
        django: 1.6.5
        pip: 1.5.6
        pytest_echo: 1.2
    Inspections:
        django.conf.settings.DATABASES.default.ENGINE: 'django.db.backends.postgresql_psycopg2'

Links
~~~~~

+--------------------+----------------+--------------+----------------+
| Project home page: |https://github.com/saxix/pytest-echo            |
+--------------------+---------------+--------------------------------+
| Issue tracker:     |https://github.com/saxix/pytest-echo/issues?sort|
+--------------------+---------------+--------------------------------+
| Download:          |http://pypi.python.org/pypi/pytest-echo/        |
+--------------------+---------------+--------------------------------+
| Documentation:     |https://pytest-echo.readthedocs.org/en/latest/  |
+--------------------+---------------+--------------+-----------------+
