# -*- coding: utf-8 -*-
from __future__ import print_function

import fnmatch
import os
from pprint import pformat

import pkg_resources
from pkg_resources import DistributionNotFound

__version__ = '1.7.1'


def get_installed_distributions():
    """
    Return a list of installed Distribution objects.
    """
    return [d for d in pkg_resources.working_set]


def get_attr(obj, attr, default='NOT FOUND'):
    """Recursive get object's attribute. May use dot notation.

    >>> class C(object):
    ...     pass
    >>> a = C()
    >>> a.b = C()
    >>> a.b.c = 4
    >>> get_attr(a, 'b.c')
    4

    >>> get_attr(a, 'b.c.y', None)

    >>> get_attr(a, 'b.c.y', 1)
    1
    >>> get_attr([0,1,2], '2')
    2
    >>> get_attr([0,1,(21, 22)], '2.1')
    22
    >>> get_attr({'key': 11}, 'key')
    11
    >>> get_attr({'key': {'key': 11}}, 'key.key')
    11
    """

    if '.' not in attr:
        try:
            if hasattr(obj, attr):
                return getattr(obj, attr, default)
            elif isinstance(obj, (list, tuple, set)):
                return obj[int(attr)]
            elif isinstance(obj, dict):
                return obj[attr]
            else:
                return default
        except Exception as e:  # pragma: no cover
            return str(e)
    else:
        L = attr.split('.')
        return get_attr(get_attr(obj, L[0], default), '.'.join(L[1:]), default)


def get_module_attribute(path):
    """
    Returns a attribute value base on it's full path.
    The `attribute` can be either a module attribute (ie. os.path.curdir)
    or a object attribute (ie. linecache.cache.__class__)

    Warning: Be careful when use this function as it load any module in the path
    and this will execute any module's level code

    :param path: full path to the attribute
    :return:

    >>> print(get_module_attribute('linecache.cache.__class__'))
    <... 'dict'>
    >>> print(get_module_attribute('os.path.curdir'))
    '.'
    >>> print(get_module_attribute('wrong'))
    ('Unable to load %s', 'wrong')
    """
    parts = path.split('.')
    parent = ""
    pkg = None
    try:
        for i, part in enumerate(parts):
            try:
                if parent:
                    module_name = "%s.%s" % (parent, parts[i])
                else:
                    module_name = parts[i]
                pkg = __import__(module_name, fromlist=[parent])
                parent = module_name
            except ImportError:
                if hasattr(pkg, part):
                    return pformat(get_attr(pkg, ".".join(parts[i:])))
        raise Exception('Unable to load %s', path)
    except Exception as e:
        return str(e)


def get_env(var_name):
    if '*' in var_name:
        targets = [(key, value)
                   for key, value in os.environ.items()
                   if fnmatch.fnmatch(key, var_name)]
    else:
        targets = [(var_name, os.environ.get(var_name, "<not set>"))]

    return targets


def get_version(package_name):
    if '*' in package_name:
        targets = [(i.key, i.version)
                   for i in get_installed_distributions()
                   if fnmatch.fnmatch(i.key, package_name)]
    else:
        targets = [(package_name, _get_version(package_name))]

    return targets


def _get_version(package_name):
    try:
        import pkg_resources

        return pkg_resources.require(package_name)[0].version
    except (ImportError, AttributeError, TypeError, DistributionNotFound):
        pass

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


def pytest_report_header(config):
    ret = []
    if config.option.echo_envs:
        ret.append("Environment:")
        data = []
        for k in config.option.echo_envs:
            data.extend(get_env(k))
        ret.append("\n".join(["    %s: %s" % (k, v)
                              for k, v in sorted(data)]))

    if config.option.echo_versions:
        ret.append("Package version:")
        data = []
        for k in config.option.echo_versions:
            data.extend(get_version(k))
        ret.append("\n".join(["    %s: %s" % (k, v)
                              for k, v in sorted(data)]))

    if config.option.echo_attribues:
        ret.append("Inspections:")
        ret.append("\n".join(["    %s: %s" % (k, get_module_attribute(k))
                              for k in config.option.echo_attribues]))
    if ret:
        return "\n".join(ret)


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--echo-env', action='append', dest="echo_envs",
                    default=[], help="environment to print")
    group.addoption('--echo-version', action='append', dest="echo_versions",
                    default=[], help="package version to print")
    group.addoption('--echo-attr', action='append', dest="echo_attribues",
                    default=[], help="attribute to print (full path)")
