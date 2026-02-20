"""
Plugin registration and discovery system.

This module provides functionality to register and discover Python plugins
for Apache Hop.
"""

from typing import Dict, Type, List, Optional
import importlib
import inspect
import sys
from pathlib import Path

from pyhop.base import HopPlugin


class PluginRegistry:
    """
    Registry for managing Apache Hop Python plugins.

    This class maintains a registry of all available plugins and provides
    methods for registering, discovering, and retrieving plugins.
    """

    def __init__(self):
        """Initialize the plugin registry."""
        self._plugins: Dict[str, Type[HopPlugin]] = {}
        self._instances: Dict[str, HopPlugin] = {}

    def register(self, plugin_class: Type[HopPlugin]) -> None:
        """
        Register a plugin class.

        Args:
            plugin_class: The plugin class to register

        Raises:
            ValueError: If the plugin ID is already registered
        """
        if not issubclass(plugin_class, HopPlugin):
            raise TypeError(f"{plugin_class.__name__} must be a subclass of HopPlugin")

        # Create a temporary instance to get the ID
        temp_instance = plugin_class("temp", "")
        plugin_id = temp_instance.get_id()

        if plugin_id in self._plugins:
            raise ValueError(f"Plugin with ID '{plugin_id}' is already registered")

        self._plugins[plugin_id] = plugin_class

    def register_instance(self, plugin: HopPlugin) -> None:
        """
        Register a plugin instance.

        Args:
            plugin: The plugin instance to register

        Raises:
            ValueError: If the plugin ID is already registered
        """
        plugin_id = plugin.get_id()

        if plugin_id in self._instances:
            raise ValueError(f"Plugin instance with ID '{plugin_id}' is already registered")

        self._instances[plugin_id] = plugin

        # Also register the class if not already registered
        if plugin_id not in self._plugins:
            self._plugins[plugin_id] = type(plugin)

    def get_plugin_class(self, plugin_id: str) -> Optional[Type[HopPlugin]]:
        """
        Get a plugin class by ID.

        Args:
            plugin_id: The plugin ID

        Returns:
            The plugin class, or None if not found
        """
        return self._plugins.get(plugin_id)

    def get_plugin_instance(self, plugin_id: str) -> Optional[HopPlugin]:
        """
        Get a plugin instance by ID.

        Args:
            plugin_id: The plugin ID

        Returns:
            The plugin instance, or None if not found
        """
        return self._instances.get(plugin_id)

    def list_plugins(self, category: Optional[str] = None) -> List[str]:
        """
        List all registered plugin IDs, optionally filtered by category.

        Args:
            category: Optional category to filter by (e.g., 'Transform', 'Action')

        Returns:
            List of plugin IDs
        """
        if category is None:
            return list(self._plugins.keys())

        result = []
        for plugin_id, plugin_class in self._plugins.items():
            temp_instance = plugin_class("temp", "")
            if temp_instance.get_category() == category:
                result.append(plugin_id)
        return result

    def discover_plugins(self, plugin_dir: str) -> int:
        """
        Discover and register plugins from a directory.

        This method scans the specified directory for Python modules
        and automatically registers any HopPlugin subclasses found.

        Args:
            plugin_dir: Path to the directory containing plugin modules

        Returns:
            Number of plugins discovered and registered
        """
        plugin_path = Path(plugin_dir)
        if not plugin_path.exists() or not plugin_path.is_dir():
            raise ValueError(f"Plugin directory not found: {plugin_dir}")

        # Add plugin directory to Python path
        if str(plugin_path.parent) not in sys.path:
            sys.path.insert(0, str(plugin_path.parent))

        count = 0

        # Scan for Python files
        for py_file in plugin_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue

            module_name = py_file.stem
            try:
                # Import the module
                module = importlib.import_module(f"{plugin_path.name}.{module_name}")

                # Find all HopPlugin subclasses
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, HopPlugin) and obj is not HopPlugin:
                        try:
                            self.register(obj)
                            count += 1
                        except ValueError:
                            # Plugin already registered
                            pass
            except Exception as e:
                print(f"Error loading plugin from {py_file}: {e}")

        return count

    def clear(self) -> None:
        """Clear all registered plugins."""
        self._plugins.clear()
        self._instances.clear()


# Global plugin registry instance
plugin_registry = PluginRegistry()


def register_plugin(plugin_class: Type[HopPlugin]) -> Type[HopPlugin]:
    """
    Decorator to register a plugin class.

    Usage:
        @register_plugin
        class MyPlugin(HopTransform):
            ...

    Args:
        plugin_class: The plugin class to register

    Returns:
        The plugin class (unchanged)
    """
    plugin_registry.register(plugin_class)
    return plugin_class
