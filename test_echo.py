import os
import pytest
import pytest_echo

pytest_plugins = "pytester",
try:
    import django

    django_present = True
except ImportError:
    django_present = False


def test_version():
    import pytest_echo

    assert pytest_echo.__version__


def test_echo_env(testdir):
    os.environ['PYTESTECHO'] = '123'
    result = testdir.runpytest('--echo-env=PYTESTECHO')
    assert "PYTESTECHO: 123" in result.stdout.lines


def test_echo_version(testdir):
    result = testdir.runpytest('--echo-version=pytest_echo')
    assert "pytest_echo: %s" % pytest_echo.__version__ in result.stdout.lines


def test_echo_all(testdir):
    os.environ['PYTESTECHO'] = '123'
    result = testdir.runpytest('--echo-version=pytest_echo', '--echo-env=PYTESTECHO')
    assert "PYTESTECHO: 123" in result.stdout.lines
    assert "pytest_echo: %s" % pytest_echo.__version__ in result.stdout.lines


@pytest.mark.skipif('not django_present')
def test_echo_settings(testdir):
    result = testdir.runpytest('--echo-settings=DEBUG')
    assert 'DEBUG: False' in result.stdout.lines

