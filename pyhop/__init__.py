"""
PyHop - Python Plugin Framework for Apache Hop

This package provides a framework for creating Apache Hop plugins in Python.
"""

__version__ = "0.1.0"

from pyhop.base import HopPlugin, HopTransform, HopAction
from pyhop.plugin import plugin_registry

__all__ = [
    "HopPlugin",
    "HopTransform",
    "HopAction",
    "plugin_registry",
]
