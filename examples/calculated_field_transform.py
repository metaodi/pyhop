"""
Example Python Transform Plugin - Add Calculated Field.

This example demonstrates a more advanced transform that adds
a calculated field to each row.
"""

from typing import Any, Dict, Optional
from pyhop import HopTransform, plugin_registry


class CalculatedFieldTransform(HopTransform):
    """
    A transform that adds a calculated field based on other fields.

    This example calculates a total price from quantity and unit price.
    """

    def __init__(self, name: str = "CalculatedField", description: str = ""):
        """Initialize the CalculatedField transform."""
        if not description:
            description = "Adds a calculated field to each row"
        super().__init__(name, description)
        self.quantity_field = "quantity"
        self.price_field = "unit_price"
        self.output_field = "total_price"

    def get_id(self) -> str:
        """Return the unique identifier for this plugin."""
        return "python.transform.calculated_field"

    def init(self) -> None:
        """Initialize the transform."""
        # Update output fields list
        if self.output_field not in self.output_fields:
            self.output_fields.append(self.output_field)
        print(f"Initialized {self.name}: {self.quantity_field} × {self.price_field} = {self.output_field}")

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single data row.

        Args:
            row: Input row

        Returns:
            Row with calculated field added
        """
        try:
            quantity = float(row.get(self.quantity_field, 0))
            price = float(row.get(self.price_field, 0))
            row[self.output_field] = quantity * price
        except (ValueError, TypeError):
            # If conversion fails, set to 0
            row[self.output_field] = 0

        return row

    def configure(self, quantity_field: str, price_field: str, output_field: str) -> None:
        """
        Configure the field names.

        Args:
            quantity_field: Name of the quantity field
            price_field: Name of the unit price field
            output_field: Name of the output field for total
        """
        self.quantity_field = quantity_field
        self.price_field = price_field
        self.output_field = output_field


# Register the plugin
plugin_registry.register(CalculatedFieldTransform)
