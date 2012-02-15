# Module:   utils
# Date:     11th April 2010
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""Utils

This module defines utilities used by circuits.
"""

import re
import sys

from imp import reload

UNCAMELRE = re.compile("([a-z0-9])([A-Z])")


def uncamel(s):
    return UNCAMELRE.sub("\g<1>_\g<2>", s).lower()


def flatten(root, visited=None):
    if not visited:
        visited = set()
    yield root
    for component in root.components.copy():
        if component not in visited:
            visited.add(component)
            for child in flatten(component, visited):
                yield child


def findchannel(root, channel):
    components = [x for x in flatten(root)
            if x.channel == channel]
    if components:
        return components[0]


def findtype(root, component):
    components = [x for x in flatten(root)
            if issubclass(type(x), component)]
    if components:
        return components[0]

findcmp = findtype


def findroot(component):
    if component.parent == component:
        return component
    else:
        return findroot(component.parent)


def safeimport(name):
    modules = sys.modules.copy()
    try:
        if name in sys.modules:
            return reload(sys.modules[name])
        else:
            return __import__(name, globals(), locals(), [""])
    except:
        for name in sys.modules.copy():
            if not name in modules:
                del sys.modules[name]
