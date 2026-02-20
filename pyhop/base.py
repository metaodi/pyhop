"""
Base classes for Apache Hop Python plugins.

These classes provide the foundation for creating different types of Hop plugins.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class HopPlugin(ABC):
    """
    Base class for all Apache Hop Python plugins.

    All plugin types should inherit from this base class and implement
    the required abstract methods.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initialize a Hop plugin.

        Args:
            name: The name of the plugin
            description: A description of what the plugin does
        """
        self.name = name
        self.description = description
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    def get_id(self) -> str:
        """
        Get the unique identifier for this plugin.

        Returns:
            A unique string identifier for the plugin
        """
        pass

    @abstractmethod
    def get_category(self) -> str:
        """
        Get the category this plugin belongs to.

        Returns:
            The category name (e.g., 'Transform', 'Action', 'Database')
        """
        pass

    def get_name(self) -> str:
        """
        Get the plugin name.

        Returns:
            The plugin name
        """
        return self.name

    def get_description(self) -> str:
        """
        Get the plugin description.

        Returns:
            The plugin description
        """
        return self.description

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set a metadata value for the plugin.

        Args:
            key: The metadata key
            value: The metadata value
        """
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get a metadata value for the plugin.

        Args:
            key: The metadata key
            default: Default value if key doesn't exist

        Returns:
            The metadata value or default
        """
        return self.metadata.get(key, default)


class HopTransform(HopPlugin):
    """
    Base class for Apache Hop Transform plugins.

    Transform plugins are used in pipelines to process data rows.
    They receive input rows, process them, and output transformed rows.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initialize a transform plugin.

        Args:
            name: The name of the transform
            description: A description of what the transform does
        """
        super().__init__(name, description)
        self.input_fields: List[str] = []
        self.output_fields: List[str] = []

    def get_category(self) -> str:
        """Get the category for transform plugins."""
        return "Transform"

    @abstractmethod
    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single data row.

        Args:
            row: Input row as a dictionary of field_name -> value

        Returns:
            Processed row as a dictionary, or None to filter out the row
        """
        pass

    def init(self) -> None:
        """
        Initialize the transform before processing starts.

        This method is called once before any rows are processed.
        Override this to set up resources, connections, etc.
        """
        pass

    def dispose(self) -> None:
        """
        Clean up the transform after processing completes.

        This method is called once after all rows are processed.
        Override this to close connections, release resources, etc.
        """
        pass

    def get_input_fields(self) -> List[str]:
        """
        Get the list of input field names this transform expects.

        Returns:
            List of input field names
        """
        return self.input_fields

    def get_output_fields(self) -> List[str]:
        """
        Get the list of output field names this transform produces.

        Returns:
            List of output field names
        """
        return self.output_fields


class HopAction(HopPlugin):
    """
    Base class for Apache Hop Action plugins.

    Action plugins are used in workflows to perform specific tasks,
    such as file operations, running scripts, or sending notifications.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initialize an action plugin.

        Args:
            name: The name of the action
            description: A description of what the action does
        """
        super().__init__(name, description)
        self.parameters: Dict[str, Any] = {}

    def get_category(self) -> str:
        """Get the category for action plugins."""
        return "Action"

    @abstractmethod
    def execute(self) -> bool:
        """
        Execute the action.

        Returns:
            True if the action succeeded, False otherwise
        """
        pass

    def set_parameter(self, name: str, value: Any) -> None:
        """
        Set an action parameter.

        Args:
            name: Parameter name
            value: Parameter value
        """
        self.parameters[name] = value

    def get_parameter(self, name: str, default: Any = None) -> Any:
        """
        Get an action parameter.

        Args:
            name: Parameter name
            default: Default value if parameter doesn't exist

        Returns:
            The parameter value or default
        """
        return self.parameters.get(name, default)

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get all action parameters.

        Returns:
            Dictionary of all parameters
        """
        return self.parameters.copy()
