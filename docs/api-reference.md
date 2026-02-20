# API Reference

Complete API documentation for PyHop classes and functions.

## Module: `pyhop`

Main package for Python plugins for Apache Hop.

### Exported Members

- `HopPlugin` - Base class for all plugins
- `HopTransform` - Base class for transform plugins
- `HopAction` - Base class for action plugins
- `plugin_registry` - Global plugin registry instance

## Class: `HopPlugin`

Base class for all Apache Hop Python plugins.

**Module:** `pyhop.base`

### Constructor

```python
HopPlugin(name: str, description: str = "")
```

**Parameters:**
- `name` (str): The name of the plugin
- `description` (str, optional): A description of what the plugin does

### Abstract Methods

These methods must be implemented by subclasses:

#### `get_id() -> str`

Get the unique identifier for this plugin.

**Returns:** A unique string identifier for the plugin

**Example:**
```python
def get_id(self):
    return "python.transform.myPlugin"
```

#### `get_category() -> str`

Get the category this plugin belongs to.

**Returns:** The category name (e.g., 'Transform', 'Action', 'Database')

**Example:**
```python
def get_category(self):
    return "Transform"
```

### Instance Methods

#### `get_name() -> str`

Get the plugin name.

**Returns:** The plugin name

#### `get_description() -> str`

Get the plugin description.

**Returns:** The plugin description

#### `set_metadata(key: str, value: Any) -> None`

Set a metadata value for the plugin.

**Parameters:**
- `key` (str): The metadata key
- `value` (Any): The metadata value

**Example:**
```python
plugin.set_metadata('version', '1.0.0')
plugin.set_metadata('author', 'John Doe')
```

#### `get_metadata(key: str, default: Any = None) -> Any`

Get a metadata value for the plugin.

**Parameters:**
- `key` (str): The metadata key
- `default` (Any, optional): Default value if key doesn't exist

**Returns:** The metadata value or default

**Example:**
```python
version = plugin.get_metadata('version', '0.0.0')
```

### Instance Attributes

- `name` (str): The plugin name
- `description` (str): The plugin description
- `metadata` (Dict[str, Any]): Plugin metadata dictionary

---

## Class: `HopTransform`

Base class for Apache Hop Transform plugins.

**Module:** `pyhop.base`

**Inherits from:** `HopPlugin`

Transform plugins are used in pipelines to process data rows. They receive input rows, process them, and output transformed rows.

### Constructor

```python
HopTransform(name: str, description: str = "")
```

**Parameters:**
- `name` (str): The name of the transform
- `description` (str, optional): A description of what the transform does

### Abstract Methods

#### `process_row(row: Dict[str, Any]) -> Optional[Dict[str, Any]]`

Process a single data row. This method is called for each row in the pipeline.

**Parameters:**
- `row` (Dict[str, Any]): Input row as a dictionary of field_name -> value

**Returns:**
- `Dict[str, Any]`: Processed row as a dictionary
- `None`: To filter out the row (don't output it)

**Example:**
```python
def process_row(self, row):
    # Modify the row
    row['name'] = row['name'].upper()

    # Add a new field
    row['processed'] = True

    # Filter out rows conditionally
    if row.get('age', 0) < 18:
        return None  # Don't output this row

    return row
```

### Lifecycle Methods

These methods are called at specific points in the transform lifecycle:

#### `init() -> None`

Initialize the transform before processing starts. This method is called once before any rows are processed.

Override this to set up resources, connections, etc.

**Example:**
```python
def init(self):
    self.connection = database.connect()
    self.row_count = 0
```

#### `dispose() -> None`

Clean up the transform after processing completes. This method is called once after all rows are processed.

Override this to close connections, release resources, etc.

**Example:**
```python
def dispose(self):
    if self.connection:
        self.connection.close()
    print(f"Processed {self.row_count} rows")
```

### Instance Methods

#### `get_category() -> str`

Get the category for transform plugins.

**Returns:** `"Transform"`

#### `get_input_fields() -> List[str]`

Get the list of input field names this transform expects.

**Returns:** List of input field names

#### `get_output_fields() -> List[str]`

Get the list of output field names this transform produces.

**Returns:** List of output field names

### Instance Attributes

- `input_fields` (List[str]): List of expected input field names
- `output_fields` (List[str]): List of output field names this transform adds

**Example:**
```python
class MyTransform(HopTransform):
    def __init__(self, name="MyTransform", description=""):
        super().__init__(name, description)
        self.input_fields = ['first_name', 'last_name']
        self.output_fields = ['full_name']
```

---

## Class: `HopAction`

Base class for Apache Hop Action plugins.

**Module:** `pyhop.base`

**Inherits from:** `HopPlugin`

Action plugins are used in workflows to perform specific tasks, such as file operations, running scripts, or sending notifications.

### Constructor

```python
HopAction(name: str, description: str = "")
```

**Parameters:**
- `name` (str): The name of the action
- `description` (str, optional): A description of what the action does

### Abstract Methods

#### `execute() -> bool`

Execute the action. This method contains the main logic of the action.

**Returns:**
- `True`: If the action succeeded
- `False`: If the action failed

**Example:**
```python
def execute(self):
    try:
        # Perform the action
        result = do_something()
        print(f"Action completed: {result}")
        return True
    except Exception as e:
        print(f"Action failed: {e}")
        return False
```

### Instance Methods

#### `get_category() -> str`

Get the category for action plugins.

**Returns:** `"Action"`

#### `set_parameter(name: str, value: Any) -> None`

Set an action parameter.

**Parameters:**
- `name` (str): Parameter name
- `value` (Any): Parameter value

**Example:**
```python
action.set_parameter('output_file', '/tmp/output.txt')
action.set_parameter('timeout', 30)
```

#### `get_parameter(name: str, default: Any = None) -> Any`

Get an action parameter.

**Parameters:**
- `name` (str): Parameter name
- `default` (Any, optional): Default value if parameter doesn't exist

**Returns:** The parameter value or default

**Example:**
```python
output_file = self.get_parameter('output_file', '/tmp/default.txt')
timeout = self.get_parameter('timeout', 60)
```

#### `get_parameters() -> Dict[str, Any]`

Get all action parameters.

**Returns:** Dictionary of all parameters

**Example:**
```python
all_params = self.get_parameters()
for key, value in all_params.items():
    print(f"{key}: {value}")
```

### Instance Attributes

- `parameters` (Dict[str, Any]): Dictionary of action parameters

---

## Class: `PluginRegistry`

Registry for managing Apache Hop Python plugins.

**Module:** `pyhop.plugin`

This class maintains a registry of all available plugins and provides methods for registering, discovering, and retrieving plugins.

### Constructor

```python
PluginRegistry()
```

### Instance Methods

#### `register(plugin_class: Type[HopPlugin]) -> None`

Register a plugin class.

**Parameters:**
- `plugin_class` (Type[HopPlugin]): The plugin class to register

**Raises:**
- `TypeError`: If the plugin_class is not a subclass of HopPlugin
- `ValueError`: If the plugin ID is already registered

**Example:**
```python
from pyhop import plugin_registry
from my_plugin import MyTransform

plugin_registry.register(MyTransform)
```

#### `register_instance(plugin: HopPlugin) -> None`

Register a plugin instance.

**Parameters:**
- `plugin` (HopPlugin): The plugin instance to register

**Raises:**
- `ValueError`: If the plugin ID is already registered

**Example:**
```python
from pyhop import plugin_registry
from my_plugin import MyTransform

plugin = MyTransform("MyTransform", "Description")
plugin_registry.register_instance(plugin)
```

#### `get_plugin_class(plugin_id: str) -> Optional[Type[HopPlugin]]`

Get a plugin class by ID.

**Parameters:**
- `plugin_id` (str): The plugin ID

**Returns:** The plugin class, or None if not found

**Example:**
```python
plugin_class = plugin_registry.get_plugin_class("python.transform.uppercase")
if plugin_class:
    instance = plugin_class("MyInstance", "Description")
```

#### `get_plugin_instance(plugin_id: str) -> Optional[HopPlugin]`

Get a plugin instance by ID.

**Parameters:**
- `plugin_id` (str): The plugin ID

**Returns:** The plugin instance, or None if not found

**Example:**
```python
plugin = plugin_registry.get_plugin_instance("python.transform.uppercase")
if plugin:
    plugin.process_row(row)
```

#### `list_plugins(category: Optional[str] = None) -> List[str]`

List all registered plugin IDs, optionally filtered by category.

**Parameters:**
- `category` (str, optional): Optional category to filter by (e.g., 'Transform', 'Action')

**Returns:** List of plugin IDs

**Example:**
```python
# List all plugins
all_plugins = plugin_registry.list_plugins()

# List only transform plugins
transforms = plugin_registry.list_plugins(category='Transform')

# List only action plugins
actions = plugin_registry.list_plugins(category='Action')
```

#### `discover_plugins(plugin_dir: str) -> int`

Discover and register plugins from a directory.

This method scans the specified directory for Python modules and automatically registers any HopPlugin subclasses found.

**Parameters:**
- `plugin_dir` (str): Path to the directory containing plugin modules

**Returns:** Number of plugins discovered and registered

**Raises:**
- `ValueError`: If the plugin directory doesn't exist or is not a directory

**Example:**
```python
count = plugin_registry.discover_plugins('/path/to/plugins')
print(f"Discovered {count} plugins")
```

#### `clear() -> None`

Clear all registered plugins.

**Example:**
```python
plugin_registry.clear()
```

---

## Global Instance: `plugin_registry`

Global plugin registry instance.

**Module:** `pyhop.plugin`

**Type:** `PluginRegistry`

Use this instance to register and manage plugins throughout your application.

**Example:**
```python
from pyhop import plugin_registry

# Register a plugin
plugin_registry.register(MyPlugin)

# List all plugins
plugins = plugin_registry.list_plugins()

# Discover plugins from directory
plugin_registry.discover_plugins('/path/to/plugins')
```

---

## Decorator: `register_plugin`

Decorator to register a plugin class.

**Module:** `pyhop.plugin`

**Signature:**
```python
def register_plugin(plugin_class: Type[HopPlugin]) -> Type[HopPlugin]
```

**Parameters:**
- `plugin_class` (Type[HopPlugin]): The plugin class to register

**Returns:** The plugin class (unchanged)

**Example:**
```python
from pyhop import HopTransform
from pyhop.plugin import register_plugin

@register_plugin
class MyPlugin(HopTransform):
    def get_id(self):
        return "python.transform.myplugin"

    def process_row(self, row):
        return row
```

---

## Type Definitions

### Row Type

Rows are represented as dictionaries mapping field names to values:

```python
Row = Dict[str, Any]
```

**Example:**
```python
row = {
    'id': 1,
    'name': 'John Doe',
    'age': 30,
    'email': 'john@example.com',
    'active': True
}
```

### Field Types

Fields can be any Python type:

- `str`: Text data
- `int`: Integer numbers
- `float`: Decimal numbers
- `bool`: Boolean values
- `datetime`: Date/time values
- `bytes`: Binary data
- `None`: Null values
- `list`: Lists/arrays
- `dict`: Nested dictionaries

---

## Complete Example

Here's a complete example using the API:

```python
from typing import Dict, Any, Optional
from pyhop import HopTransform, plugin_registry

class ExampleTransform(HopTransform):
    """Complete example of a transform plugin."""

    def __init__(self, name: str = "Example", description: str = ""):
        super().__init__(name, description or "Example transform")
        self.input_fields = ['input_field']
        self.output_fields = ['output_field']
        self.row_count = 0

        # Set metadata
        self.set_metadata('version', '1.0.0')
        self.set_metadata('author', 'Your Name')

    def get_id(self) -> str:
        return "python.transform.example"

    def init(self) -> None:
        """Initialize the transform."""
        print(f"Starting {self.get_name()}")
        self.row_count = 0

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process each row."""
        self.row_count += 1

        # Transform the data
        input_value = row.get('input_field', '')
        row['output_field'] = f"Processed: {input_value}"

        return row

    def dispose(self) -> None:
        """Clean up."""
        print(f"Processed {self.row_count} rows")
        version = self.get_metadata('version')
        print(f"Plugin version: {version}")

# Register the plugin
plugin_registry.register(ExampleTransform)

# Or use the decorator
from pyhop.plugin import register_plugin

@register_plugin
class AnotherExample(HopTransform):
    def get_id(self) -> str:
        return "python.transform.another"

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return row
```

---

## Error Handling

### Common Exceptions

- `TypeError`: Raised when registering a class that isn't a HopPlugin subclass
- `ValueError`: Raised when registering a plugin with a duplicate ID
- `KeyError`: May be raised when accessing missing fields in rows
- `AttributeError`: May be raised when accessing undefined attributes

### Best Practices

Always handle exceptions in your plugin methods:

```python
def process_row(self, row):
    try:
        result = row['required_field']
        # Process result
        return row
    except KeyError:
        print(f"Missing required field in row: {row}")
        return None  # Filter out invalid row
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise  # Re-raise unexpected errors
```

---

## Version Information

Get the PyHop version:

```python
import pyhop
print(pyhop.__version__)  # e.g., "0.1.0"
```

---

## See Also

- [Plugin Development Guide](plugin-development.md) - Learn how to create plugins
- [Installation Guide](installation.md) - Setup instructions
- [Examples](../examples/) - Example implementations
