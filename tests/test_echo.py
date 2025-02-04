from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import mock

import pytest

ATTR_INT = 111
ATTR_DICT = {"key": "value"}
ATTR_LIST = [11, 12, 13, (21, 22)]
ATTR_COMPOSITE = {"key1": "value1", "key2": [11, 12, 13, 14], "key3": 99}
ATTR_SET = {11, 12, 13}


class Dummy:
    attr = 1


def test_function() -> None:
    pass


dummy = Dummy()


def test_echo_env(testdir: pytest.Testdir) -> None:
    with mock.patch.dict(os.environ, {"PYTESTECHO": "123"}, clear=True):
        result = testdir.runpytest("--echo-env=PYTESTECHO")
        result.stdout.fnmatch_lines(["    PYTESTECHO: 123"])


def test_echo_env_glob(testdir: pytest.Testdir) -> None:
    with mock.patch.dict(os.environ, {"PYTESTECHO-a": "1", "PYTESTECHO-b": "2"}, clear=True):
        result = testdir.runpytest("--echo-env=PYTESTECHO*")
        result.stdout.fnmatch_lines(["    PYTESTECHO-a: 1", "    PYTESTECHO-b: 2"])


def test_echo_version(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-version=pytest-echo")
    result.stdout.fnmatch_lines(["*echo: *"])


def test_echo_version_error(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-version=missing-package")
    result.stdout.fnmatch_lines(["    missing-package: <unable to load package>"])


def test_echo_version_missing(testdir: pytest.Testdir) -> None:
    sys.path.insert(0, str(Path(__file__).parent / "extras"))
    result = testdir.runpytest("--echo-version=v3")
    result.stdout.fnmatch_lines(["    v3: <unable get package version>"])


@pytest.mark.parametrize("module", ["v1", "v2"])
def test_echo_version_non_standard(testdir: pytest.Testdir, module: str) -> None:
    sys.path.insert(0, str(Path(__file__).parent / "extras"))
    result = testdir.runpytest(f"--echo-version={module}")
    result.stdout.fnmatch_lines([f"    {module}: 9.9"])


def test_echo_version_glob(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-version=pytest*")
    result.stdout.fnmatch_lines(["*echo-*"])


def test_echo_all(testdir: pytest.Testdir) -> None:
    os.environ["PYTESTECHO"] = "123"
    result = testdir.runpytest("--echo-version=pytest_echo", "--echo-env=PYTESTECHO")
    result.stdout.fnmatch_lines(["    PYTESTECHO: 123"])
    result.stdout.fnmatch_lines(["    pytest_echo: *"])


def test_echo_attr(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.ATTR_INT")
    result.stdout.fnmatch_lines(["    test_echo.ATTR_INT: 111"])


def test_echo_attr_missing(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.MISSING")
    result.stdout.fnmatch_lines(["    test_echo.MISSING: unknown attribute"])


def test_echo_attr_dict(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.ATTR_DICT.key")
    result.stdout.fnmatch_lines(["    test_echo.ATTR_DICT.key: 'value'"])


def test_echo_attr_list(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.ATTR_LIST.2")
    result.stdout.fnmatch_lines(["    test_echo.ATTR_LIST.2: 13"])


def test_echo_attr_set(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.ATTR_SET.2")
    result.stdout.fnmatch_lines(["    test_echo.ATTR_SET.2: 13"])


def test_echo_attr_list_inner(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.ATTR_LIST.3.1")
    assert "    test_echo.ATTR_LIST.3.1: 22" in result.stdout.lines


def test_echo_attr_list_composite(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest(
        "--echo-attr=test_echo.ATTR_COMPOSITE.key1",
        "--echo-attr=test_echo.ATTR_COMPOSITE.key2.3",
    )
    assert "    test_echo.ATTR_COMPOSITE.key1: 'value1'" in result.stdout.lines
    assert "    test_echo.ATTR_COMPOSITE.key2.3: 14" in result.stdout.lines


def test_echo_attr_list_callable(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.test_function")
    result.stdout.fnmatch_lines([
        "    test_echo.test_function: <function test_function*",
    ])


def test_echo_attr_object_attr(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.dummy.attr")
    result.stdout.fnmatch_lines(["    test_echo.dummy.attr: 1"])


def test_echo_attr_object_attr_missig(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=test_echo.dummy.missing")
    result.stdout.fnmatch_lines(["    test_echo.dummy.missing: 'unknown attribute'"])


def test_echo_no_inspections(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("")
    result.stdout.fnmatch_lines(["pytest-echo: nothing to echoing"])


def test_echo_attr_module_object_attr(testdir: pytest.Testdir) -> None:
    result = testdir.runpytest("--echo-attr=linecache.cache.__class__")
    match = "    linecache.cache.__class__: <class 'dict'>"
    result.stdout.fnmatch_lines([match])
