"""
Example plugins for PyHop.

This package contains example implementations of various plugin types.
"""

# Import all example plugins to register them
from examples.uppercase_transform import UpperCaseTransform
from examples.calculated_field_transform import CalculatedFieldTransform
from examples.filewriter_action import FileWriterAction
from examples.http_request_action import HTTPRequestAction

__all__ = [
    "UpperCaseTransform",
    "CalculatedFieldTransform",
    "FileWriterAction",
    "HTTPRequestAction",
]
