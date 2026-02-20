"""
Template for creating a Transform Plugin.

Copy this file and modify it to create your own transform plugin.
"""

from typing import Any, Dict, Optional
from pyhop import HopTransform, plugin_registry


class TemplateTransform(HopTransform):
    """
    Brief description of what this transform does.

    Detailed description explaining:
    - What this transform does
    - What input fields it expects
    - What output fields it produces
    - Any special behavior or requirements
    """

    def __init__(self, name: str = "TemplateTransform", description: str = ""):
        """Initialize the transform."""
        super().__init__(name, description or "Template transform description")

        # Define input fields (optional)
        self.input_fields = []

        # Define output fields this transform adds (optional)
        self.output_fields = []

        # Add any custom instance variables here
        self.custom_config = None

    def get_id(self) -> str:
        """
        Return unique plugin ID.

        Use a descriptive, namespaced ID like:
        python.transform.your_transform_name
        """
        return "python.transform.template"

    def init(self) -> None:
        """
        Initialize the transform before processing starts.

        This method is called once before any rows are processed.
        Use it to:
        - Set up database connections
        - Open files
        - Initialize counters
        - Validate configuration
        """
        # Example: Initialize counter
        # self.row_count = 0

        # Example: Open connection
        # self.connection = open_connection()

        pass

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single data row.

        Args:
            row: Input row as a dictionary of field_name -> value

        Returns:
            Processed row as a dictionary, or None to filter out the row
        """
        # Example: Access a field
        # value = row.get('field_name', default_value)

        # Example: Modify a field
        # row['field_name'] = new_value

        # Example: Add a new field
        # row['new_field'] = calculated_value

        # Example: Filter out rows (return None to skip)
        # if some_condition:
        #     return None

        # Return the modified row
        return row

    def dispose(self) -> None:
        """
        Clean up the transform after processing completes.

        This method is called once after all rows are processed.
        Use it to:
        - Close database connections
        - Close files
        - Print summary statistics
        - Release resources
        """
        # Example: Close connection
        # if self.connection:
        #     self.connection.close()

        # Example: Print stats
        # print(f"Processed {self.row_count} rows")

        pass

    # Optional: Add configuration methods
    def configure(self, **kwargs: Any) -> None:
        """
        Configure the transform with custom parameters.

        Args:
            **kwargs: Configuration parameters
        """
        # Example: Set configuration
        # self.custom_config = kwargs.get('config_param', default_value)
        pass


# Register the plugin
# plugin_registry.register(TemplateTransform)

# Or use the decorator (uncomment to use)
# from pyhop.plugin import register_plugin
# @register_plugin
# class TemplateTransform(HopTransform):
#     ...
