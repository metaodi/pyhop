"""
Template for creating an Action Plugin.

Copy this file and modify it to create your own action plugin.
"""

from typing import Any, Dict
from pyhop import HopAction, plugin_registry


class TemplateAction(HopAction):
    """
    Brief description of what this action does.

    Detailed description explaining:
    - What this action does
    - What parameters it accepts
    - What it returns (success/failure conditions)
    - Any side effects or requirements
    """

    def __init__(self, name: str = "TemplateAction", description: str = ""):
        """Initialize the action."""
        super().__init__(name, description or "Template action description")

        # Set default parameters
        # Use set_parameter() to define configurable parameters
        # self.set_parameter('param_name', default_value)

        # Example parameters:
        # self.set_parameter('output_file', '/tmp/output.txt')
        # self.set_parameter('timeout', 30)
        # self.set_parameter('enabled', True)

    def get_id(self) -> str:
        """
        Return unique plugin ID.

        Use a descriptive, namespaced ID like:
        python.action.your_action_name
        """
        return "python.action.template"

    def execute(self) -> bool:
        """
        Execute the action.

        This is the main method that performs the action's work.
        It should return True if successful, False if failed.

        Returns:
            True if the action succeeded, False otherwise
        """
        try:
            # Get parameters
            # param_value = self.get_parameter('param_name', default_value)

            # Example: Get a parameter with a default
            # output_file = self.get_parameter('output_file', '/tmp/default.txt')
            # timeout = self.get_parameter('timeout', 60)

            # Validate parameters (optional)
            # if not output_file:
            #     print("Error: output_file parameter is required")
            #     return False

            # Perform the action
            # result = do_something(param_value)

            # Example: Write to file
            # with open(output_file, 'w') as f:
            #     f.write("Action completed successfully\n")

            # Print success message
            # print(f"Action completed successfully: {result}")

            # Return True for success
            return True

        except Exception as e:
            # Handle errors
            print(f"Action failed: {e}")
            return False

    # Optional: Add helper methods
    def validate_parameters(self) -> bool:
        """
        Validate action parameters before execution.

        Returns:
            True if parameters are valid, False otherwise
        """
        # Example validation
        # required_params = ['param1', 'param2']
        # for param in required_params:
        #     if not self.get_parameter(param):
        #         print(f"Error: Required parameter '{param}' is missing")
        #         return False
        return True

    def configure(self, **kwargs: Any) -> None:
        """
        Configure the action with multiple parameters at once.

        Args:
            **kwargs: Parameter name-value pairs
        """
        for key, value in kwargs.items():
            self.set_parameter(key, value)


# Register the plugin
# plugin_registry.register(TemplateAction)

# Or use the decorator (uncomment to use)
# from pyhop.plugin import register_plugin
# @register_plugin
# class TemplateAction(HopAction):
#     ...
