pytest-echo
===========

Echoing environment variables, package version and django settings

Usage
-----

install via::

    pip install pytest-echo



The plugin provides ability to print some extra information prior to run the tests.


Examples
--------

Dump environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    $ py.test --echo-env=HOME
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    HOME: /home/sax
    plugins: echo, pydev, cov, cache, django


Dump package version
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    $ py.test --echo-version=pytest_echo
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    pytest_echo: 0.1
    plugins: echo, pydev, cov, cache, django


Dump django settings
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    $ py.test --echo-settings=DEBUG
    ============================= test session starts =========================
    platform linux2 -- Python 2.7.4 -- py-1.4.22 -- pytest-2.6.0 -- /bin/python
    DEBUG: False
    plugins: echo, pydev, cov, cache, django





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
