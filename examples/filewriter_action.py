"""
Example Python Action Plugin for Apache Hop.

This example demonstrates how to create a simple action plugin
that writes a message to a file.
"""

from typing import Any
from pyhop import HopAction, plugin_registry
from pathlib import Path
from datetime import datetime


class FileWriterAction(HopAction):
    """
    An action that writes a message to a file.

    This is a simple example that demonstrates the basic structure
    of an action plugin.
    """

    def __init__(self, name: str = "FileWriter", description: str = ""):
        """Initialize the FileWriter action."""
        if not description:
            description = "Writes a message to a file"
        super().__init__(name, description)
        self.set_parameter("filepath", "output.txt")
        self.set_parameter("message", "Hello from PyHop!")
        self.set_parameter("append", False)

    def get_id(self) -> str:
        """Return the unique identifier for this plugin."""
        return "python.action.filewriter"

    def execute(self) -> bool:
        """
        Execute the action.

        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.get_parameter("filepath")
            message = self.get_parameter("message")
            append = self.get_parameter("append", False)

            # Add timestamp to message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_message = f"[{timestamp}] {message}\n"

            # Write to file
            mode = "a" if append else "w"
            with open(filepath, mode) as f:
                f.write(full_message)

            print(f"Successfully wrote message to {filepath}")
            return True

        except Exception as e:
            print(f"Error writing to file: {e}")
            return False


# Register the plugin
plugin_registry.register(FileWriterAction)
