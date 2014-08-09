import os
import sys
import pytest_echo

pytest_plugins = "pytester",

ATTR_INT = 111
ATTR_DICT = {'key': 'value'}
ATTR_LIST = [11, 12, 13, (21, 22)]
ATTR_COMPOSITE = {'key1': 'value1', 'key2': [11, 12, 13, 14], 'key3': 99}


class Dummy():
    attr = 1


def FUNC():
    pass


dummy = Dummy()


def test_version():
    import pytest_echo
    assert pytest_echo.__version__


def test_echo_env(testdir):
    os.environ['PYTESTECHO'] = '123'
    result = testdir.runpytest('--echo-env=PYTESTECHO')
    result.stdout.fnmatch_lines([
        "    PYTESTECHO: 123"
    ])


def test_echo_version(testdir):
    result = testdir.runpytest('--echo-version=pytest_echo')
    result.stdout.fnmatch_lines(["    pytest_echo: %s" % pytest_echo.__version__])


def test_echo_all(testdir):
    os.environ['PYTESTECHO'] = '123'
    result = testdir.runpytest('--echo-version=pytest_echo',
                               '--echo-env=PYTESTECHO')
    result.stdout.fnmatch_lines(["    PYTESTECHO: 123"])
    result.stdout.fnmatch_lines(["    pytest_echo: %s" % pytest_echo.__version__])


def test_echo_attr(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.ATTR_INT')
    result.stdout.fnmatch_lines(['    test_echo.ATTR_INT: 111'])


def test_echo_attr_dict(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.ATTR_DICT.key')
    result.stdout.fnmatch_lines(["    test_echo.ATTR_DICT.key: 'value'"])


def test_echo_attr_list(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.ATTR_LIST.2')
    result.stdout.fnmatch_lines([u"    test_echo.ATTR_LIST.2: 13"])


def test_echo_attr_list_inner(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.ATTR_LIST.3.1')
    assert u"    test_echo.ATTR_LIST.3.1: 22" in result.stdout.lines


def test_echo_attr_list_composite(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.ATTR_COMPOSITE.key1',
                               '--echo-attr=test_echo.ATTR_COMPOSITE.key2.3')
    assert u"    test_echo.ATTR_COMPOSITE.key1: 'value1'" in result.stdout.lines
    assert u"    test_echo.ATTR_COMPOSITE.key2.3: 14" in result.stdout.lines


def test_echo_attr_list_callable(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.FUNC')
    result.stdout.fnmatch_lines([
        "    test_echo.FUNC: <function FUNC*",
    ])


def test_echo_attr_object_attr(testdir):
    result = testdir.runpytest('--echo-attr=test_echo.dummy.attr')
    result.stdout.fnmatch_lines([
        "    test_echo.dummy.attr: 1",
    ])


def test_echo_attr_module_object_attr(testdir):
    result = testdir.runpytest('--echo-attr=linecache.cache.__class__')
    if sys.version_info[0] == 2:
        match = "    linecache.cache.__class__: <type 'dict'>"
    elif sys.version_info[0] == 3:
        match = "    linecache.cache.__class__: <class 'dict'>"

    result.stdout.fnmatch_lines([match])


def test_django_settings(testdir):
    testdir.makeconftest("""
        def pytest_configure(config):
            import django
            from django.conf import settings  # noqa
            settings.configure()
    """)
    result = testdir.runpytest('--echo-attr=django.conf.settings.DEBUG')
    result.stdout.fnmatch_lines([
        "    django.conf.settings.DEBUG: False",
    ])

def test_django_settings_extended(testdir):
    testdir.makeconftest("""
        def pytest_configure(config):
            import django
            from django.conf import settings  # noqa
            settings.configure()
            settings.DATABASES = {'default':{ 'ENGINE': 'sqlite3'}}
    """)
    result = testdir.runpytest('--echo-attr=django.conf.settings.DATABASES.default.ENGINE')
    result.stdout.fnmatch_lines([
        "    django.conf.settings.DATABASES.default.ENGINE: 'sqlite3'"
    ])

