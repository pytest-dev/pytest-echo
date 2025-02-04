"""Adopt environment section in pytest configuration files."""

from __future__ import annotations

import fnmatch
import importlib.metadata as meta
import os
from dataclasses import dataclass
from pprint import pformat
from typing import Any, Iterator

import pytest

UNKNOWN_TYPE = "unknown type"
UNKNOWN_ATTR = "unknown attribute"


@dataclass
class Entry:
    """Configuration entries."""

    key: str
    type: str


def get_installed_distributions() -> list[tuple[str, str]]:
    """Return a list of installed Distribution objects."""
    try:
        return [(d.name, d.version) for d in meta.distributions()]
    except (ImportError, AttributeError, TypeError):  # pragma: no cover
        return []


def get_attr(obj: Any, attr: str, default: str | None = "NOT FOUND") -> Any:
    """Recursive get object's attribute. May use dot notation."""
    if "." not in attr:
        try:
            if hasattr(obj, attr):
                ret = getattr(obj, attr, default)
            elif isinstance(obj, (list, tuple)):
                ret = obj[int(attr)]
            elif isinstance(obj, set):
                ret = list(obj)[int(attr)]
            elif isinstance(obj, dict):
                ret = obj[attr]
            else:
                ret = UNKNOWN_ATTR
        except Exception as e:  # noqa: BLE001 # pragma: no cover
            return str(e)
        else:
            return ret
    else:
        parts = attr.split(".")
        return get_attr(get_attr(obj, parts[0], default), ".".join(parts[1:]), default)


def get_module_attribute(path: str) -> Any:
    """
    Return a attribute value based on it's full path. AttributeError is raised if the attribute cannot be found.

    The `attribute` can be either a module attribute (ie. os.path.curdir)
    or a object attribute (ie. linecache.cache.__class__)

    Warning: Be careful when use this function as it load any module in the path
    and this will execute any module's level code

    :param path: full path to the attribute
    :return: attribute value
    :raises AttributeError: if attribute cannot be found
    """
    parts = path.split(".")
    parent = ""
    pkg = None
    try:
        for i, part in enumerate(parts):
            try:
                module_name = f"{parent}.{parts[i]}" if parent else parts[i]
                pkg = __import__(module_name, fromlist=[parent])
                parent = module_name
            except ImportError:  # noqa: PERF203
                if hasattr(pkg, part):
                    return pformat(get_attr(pkg, ".".join(parts[i:])))
        raise AttributeError(UNKNOWN_ATTR)  # noqa: TRY301
    except Exception as e:  # noqa: BLE001
        return str(e)


def get_env(var_name: str) -> list[tuple[str, str]]:
    """Return environment variable key/value."""
    if "*" in var_name:
        targets = [(key, value) for key, value in os.environ.items() if fnmatch.fnmatch(key, var_name)]
    else:
        targets = [(var_name, os.environ.get(var_name, "<not set>"))]

    return targets


def get_version(package_name: str) -> list[tuple[str, str]]:
    """Return list of package versions."""
    if "*" in package_name:
        targets = [i for i in get_installed_distributions() if fnmatch.fnmatch(i[0], package_name)]
    else:
        targets = [(package_name, _get_version(package_name))]

    return targets


def _get_version(package_name: str) -> Any:
    try:
        return meta.version(package_name)
    except (ImportError, AttributeError, TypeError):
        pass

    try:
        pkg = __import__(package_name)
    except ImportError:
        return "<unable to load package>"
    else:
        for attr_name in ("get_version", "__version__", "VERSION", "version"):
            if hasattr(pkg, attr_name):
                attr = getattr(pkg, attr_name)
                if callable(attr):
                    return attr()
                return attr
        return "<unable get package version>"


def pytest_report_header(config: pytest.Config) -> str | None:
    """Pytest report header."""
    ret = []
    if config.option.echo_envs:
        ret.append("Environment:")
        data = []
        for k in config.option.echo_envs:
            data.extend(get_env(k))
        ret.append("\n".join([f"    {k}: {v}" for k, v in sorted(data)]))

    if config.option.echo_versions:
        ret.append("Package version:")
        data = []
        for k in config.option.echo_versions:
            data.extend(get_version(k))
        ret.append("\n".join([f"    {k}: {v}" for k, v in sorted(data)]))

    if config.option.echo_attributes:
        ret.extend([
            "Inspections:",
            "\n".join([f"    {k}: {get_module_attribute(k)}" for k in config.option.echo_attributes]),
        ])
    if not ret:
        ret = ["pytest-echo: nothing to echoing"]
    return "\n".join(ret)


@pytest.hookimpl
def pytest_addoption(parser: pytest.Parser) -> None:
    """Add section to configuration files."""
    parser.addini(
        "echo_envs",
        type="linelist",
        default=[],
        help="environment to print",
    )
    parser.addini(
        "echo_attributes",
        type="linelist",
        default=[],
        help="attribute to print (full path)",
    )
    parser.addini(
        "echo_versions",
        type="linelist",
        default=[],
        help="package version to print",
    )

    group = parser.getgroup("general")
    group.addoption(
        "--echo-env",
        action="append",
        dest="echo_envs",
        default=[],
        help="environment to print",
    )
    group.addoption(
        "--echo-version",
        action="append",
        dest="echo_versions",
        default=[],
        help="package version to print",
    )
    group.addoption(
        "--echo-attr",
        action="append",
        dest="echo_attributes",
        default=[],
        help="attribute to print (full path)",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(
    args: list[str],  # noqa: ARG001
    early_config: pytest.Config,
    parser: pytest.Parser,  # noqa: ARG001
) -> None:
    """Load environment variables from configuration files."""
    for entry in _load_values(early_config):
        if entry.type in {"env", "envs", "echo_envs"}:
            early_config.option.echo_envs.append(entry.key)
        if entry.type in {"attr", "attribute", "echo_attributes"}:
            early_config.option.echo_attributes.append(entry.key)
        if entry.type in {"version", "echo_version"}:
            early_config.option.echo_versions.append(entry.key)


def _load_values(early_config: pytest.Config) -> Iterator[Entry]:
    for var in early_config.getini("echo_envs"):
        yield Entry(var, "env")
    for var in early_config.getini("echo_attributes"):
        yield Entry(var, "attr")
    for var in early_config.getini("echo_versions"):
        yield Entry(var, "version")
