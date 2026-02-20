"""
Example Python Transform Plugin for Apache Hop.

This example demonstrates how to create a simple transform plugin
that converts text to uppercase.
"""

from typing import Any, Dict, Optional
from pyhop import HopTransform, plugin_registry


class UpperCaseTransform(HopTransform):
    """
    A transform that converts specified text fields to uppercase.

    This is a simple example that demonstrates the basic structure
    of a transform plugin.
    """

    def __init__(self, name: str = "UpperCase", description: str = ""):
        """Initialize the UpperCase transform."""
        if not description:
            description = "Converts text fields to uppercase"
        super().__init__(name, description)
        self.fields_to_convert = []

    def get_id(self) -> str:
        """Return the unique identifier for this plugin."""
        return "python.transform.uppercase"

    def init(self) -> None:
        """Initialize the transform before processing starts."""
        print(f"Initializing {self.name} transform")
        # Any initialization logic goes here

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single data row.

        Args:
            row: Input row as a dictionary

        Returns:
            Processed row with specified fields converted to uppercase
        """
        # If no fields specified, convert all string fields
        if not self.fields_to_convert:
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = value.upper()
        else:
            # Convert only specified fields
            for field in self.fields_to_convert:
                if field in row and isinstance(row[field], str):
                    row[field] = row[field].upper()

        return row

    def dispose(self) -> None:
        """Clean up the transform after processing completes."""
        print(f"Disposing {self.name} transform")
        # Any cleanup logic goes here

    def set_fields_to_convert(self, fields: list) -> None:
        """
        Set which fields should be converted to uppercase.

        Args:
            fields: List of field names to convert
        """
        self.fields_to_convert = fields


# Register the plugin
plugin_registry.register(UpperCaseTransform)
