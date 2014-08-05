pytest-echo
===========

Print environment variables, package version and django settings.

Useful in the continuous integration to dump env configuration.


Install
-------

install via::

    pip install pytest-echo



The plugin provides ability to print some extra information prior to run the tests.


Examples
--------

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
~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ py.test --echo-attr=django.conf.settings.DEBUG
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    DEBUG: False
    plugins: echo, pydev, cov, cache, django

.. warning:: Be careful when use ``--echo-attr``. It load any module in the path and this will 
    execute any module's level code




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
