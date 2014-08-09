# -*- coding: utf-8 -*-
import os
from pprint import pformat


__version__ = '1.3'


class RetrieveException(Exception):
    pass


def get_attr(obj, attr, default='NOT FOUND'):
    """Recursive get object's attribute. May use dot notation.

    >>> class C(object): pass
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
        except Exception as e:
            return str(e)
    else:
        L = attr.split('.')
        return get_attr(get_attr(obj, L[0], default), '.'.join(L[1:]), default)


def get_module_attribute(path):
    """
    Returns a attribute value base on it's full path.
    The `attribute` can be either a module attribute (ie. os.path.curdir)
    or a object attribute (ie. linecache.cache.__class__)

    Warning: Be careful when use thi function as it load any module in the path
    and this will execute any module's level code

    :param path: full path to the attribute
    :return:

    >>> print get_module_attribute('linecache.cache.__class__')
    <type 'dict'>
    >>> print get_module_attribute('os.path.curdir')
    '.'
    """
    parts = path.split('.')
    parent = ""
    pkg = None
    try:
        for i, el in enumerate(parts):
            try:
                if parent:
                    a = "{}.{}".format(parent, parts[i])
                else:
                    a = parts[i]
                pkg = __import__(a, fromlist=[parent])
                parent = a
            except ImportError:
                if hasattr(pkg, el):
                    return pformat(get_attr(pkg, ".".join(parts[i:])))
    except Exception as e:
        return str(e)


def _get_version(package_name):
    try:
        import pkg_resources

        return pkg_resources.require(package_name)[0].version
    except:
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
        ret.append("\n".join(["    %s: %s" % (k, os.environ.get(k, "<not set>"))
                              for k in config.option.echo_envs]))
    if config.option.echo_versions:
        ret.append("Package version:")
        ret.append("\n".join(["    %s: %s" % (k, _get_version(k))
                              for k in config.option.echo_versions]))
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
