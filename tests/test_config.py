from __future__ import annotations

import os
from unittest import mock

import pytest


@pytest.mark.parametrize(
    ("ini", "env"),
    [
        pytest.param(
            "[pytest]\necho_envs = ENV1\n   ENV2\n   ENV3",
            {"ENV1": "1", "ENV2": "2", "ENV3": "3"},
            id="echo environment variables",
        ),
    ],
)
def test_ini_config(
    testdir: pytest.Testdir,
    ini: str,
    env: dict[str, str],
) -> None:
    new_env = {
        **env,
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTEST_PLUGINS": "pytest_echo.plugin",
    }
    testdir.makeini(ini)

    with mock.patch.dict(os.environ, new_env, clear=True):
        result = testdir.runpytest(testdir)
        result.stdout.fnmatch_lines(["    ENV1: 1"])


@pytest.mark.parametrize(
    ("toml", "env", "expected"),
    [
        pytest.param(
            '[tool.pytest.ini_options]\necho_envs = ["ENV1", "ENV2", "ENV3"]',
            {"ENV1": "1", "ENV2": "2", "ENV3": "3"},
            "    ENV2: 2",
            id="echo environment variables",
        ),
        pytest.param(
            '[tool.pytest.ini_options]\necho_attributes = ["test_echo.ATTR_LIST"]',
            {},
            "    test_echo.ATTR_LIST: [11, 12, 13, (21, 22)]",
            id="echo environment variables",
        ),
        pytest.param(
            '[tool.pytest.ini_options]\necho_versions = ["pytest_echo"]',
            {},
            "    pytest_echo: *",
            id="echo environment variables",
        ),
    ],
)
def test_toml_config(
    testdir: pytest.Testdir,
    toml: str,
    env: dict[str, str],
    expected: str,
) -> None:
    new_env = {
        **env,
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTEST_PLUGINS": "pytest_echo.plugin",
    }
    with mock.patch.dict(os.environ, new_env, clear=True):
        testdir.makepyfile("""def test_pass(request): pass""")
        testdir.makepyprojecttoml(toml)
        result = testdir.runpytest()
        result.stdout.fnmatch_lines([expected])
    result.assert_outcomes(passed=1)
