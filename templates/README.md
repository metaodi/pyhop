# Plugin Templates

This directory contains templates for creating PyHop plugins.

## Available Templates

### Transform Template
**File:** `transform_template.py`

Use this template to create transform plugins that process data rows in pipelines.

**Usage:**
```bash
cp templates/transform_template.py my_plugins/my_transform.py
# Edit my_transform.py and implement your logic
```

### Action Template
**File:** `action_template.py`

Use this template to create action plugins that perform tasks in workflows.

**Usage:**
```bash
cp templates/action_template.py my_plugins/my_action.py
# Edit my_action.py and implement your logic
```

## Quick Start

1. Copy the appropriate template to your plugin directory
2. Rename the class and file to match your plugin name
3. Update the `get_id()` method with a unique plugin ID
4. Implement the required methods (`process_row()` for transforms, `execute()` for actions)
5. Uncomment the registration line at the bottom
6. Import your plugin module to register it

## Example

Create a new transform:

```bash
# Copy template
cp templates/transform_template.py my_plugins/uppercase_transform.py
```

Edit `uppercase_transform.py`:

```python
from typing import Any, Dict, Optional
from pyhop import HopTransform, plugin_registry

class UpperCaseTransform(HopTransform):
    def __init__(self, name: str = "UpperCase", description: str = ""):
        super().__init__(name, description or "Convert text to uppercase")

    def get_id(self) -> str:
        return "python.transform.uppercase"

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.upper()
        return row

plugin_registry.register(UpperCaseTransform)
```

## Best Practices

1. **Unique IDs**: Use descriptive, namespaced IDs (e.g., `python.transform.company.plugin_name`)
2. **Documentation**: Add docstrings explaining what your plugin does
3. **Error Handling**: Wrap your code in try-except blocks
4. **Resource Cleanup**: Use `init()` and `dispose()` methods for resource management
5. **Type Hints**: Use type hints for better code quality
6. **Testing**: Create unit tests for your plugins

## See Also

- [Plugin Development Guide](../docs/plugin-development.md) - Comprehensive guide
- [Examples](../examples/) - Working plugin examples
- [API Reference](../docs/api-reference.md) - Complete API documentation
