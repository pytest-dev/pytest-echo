# -*- coding: utf-8 -*-
import os
from pprint import pformat


__version__ = '1.0'


def _get_version(package_name):
    try:
        pkg = __import__(package_name)
    except ImportError:
        return '<unable to load package>'
    for attr_name in ('get_version', '__version__', 'VERSION', 'version'):
        if hasattr(pkg, attr_name):
            attr = getattr(pkg, attr_name)
            if callable(attr):
                return attr()
            else:
                return attr


def _get_settings(entry):
    try:
        from django.core.exceptions import ImproperlyConfigured

        try:
            from django.conf import settings

            getattr(settings, 'DEBUG')  # force settings loading
        except ImproperlyConfigured:
            settings.configure()
        try:
            entry = getattr(settings, entry)
            return pformat(entry)
        except AttributeError as e:
            return "ERROR: %s" % str(e)
    except ImportError:
        return ""


def pytest_report_header(config):
    ret = []
    if config.option.echo_settings:
        ret.append("\n".join(["%s: %s" % (k, _get_settings(k))
                              for k in config.option.echo_settings]))
    if config.option.echo_envs:
        ret.append("\n".join(["%s: %s" % (k, os.environ.get(k, "<not set>"))
                              for k in config.option.echo_envs]))
    if config.option.echo_versions:
        ret.append("\n".join(["%s: %s" % (k, _get_version(k))
                              for k in config.option.echo_versions]))
    if ret:
        return "\n".join(ret)


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--echo-env', action='append', dest="echo_envs",
                    default=[], help="environment to print")
    group.addoption('--echo-version', action='append', dest="echo_versions",
                    default=[], help="package version to print")
    group.addoption('--echo-settings', action='append', dest="echo_settings",
                    default=[], help="django settings to print")
