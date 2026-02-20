# Quick Start Guide

Get started with PyHop in 5 minutes!

## Step 1: Install PyHop

```bash
pip install pyhop
```

Or install from source:

```bash
git clone https://github.com/metaodi/pyhop.git
cd pyhop
pip install -e .
```

## Step 2: Create Your First Plugin

Create a file `my_transform.py`:

```python
from pyhop import HopTransform, plugin_registry

class UpperCaseTransform(HopTransform):
    """Convert text fields to uppercase."""

    def get_id(self):
        return "python.transform.uppercase"

    def process_row(self, row):
        # Convert all string fields to uppercase
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = value.upper()
        return row

# Register the plugin
plugin_registry.register(UpperCaseTransform)
```

## Step 3: Test Your Plugin

Create a file `test_plugin.py`:

```python
from my_transform import UpperCaseTransform

# Create an instance
transform = UpperCaseTransform("Test", "Test transform")

# Initialize
transform.init()

# Test with sample data
row = {"name": "john doe", "city": "boston"}
result = transform.process_row(row)

print(f"Input:  {{'name': 'john doe', 'city': 'boston'}}")
print(f"Output: {result}")
# Output: {'name': 'JOHN DOE', 'city': 'BOSTON'}

# Clean up
transform.dispose()
```

Run it:

```bash
python test_plugin.py
```

## Step 4: Try the Examples

PyHop comes with ready-to-use examples:

```python
from examples.uppercase_transform import UpperCaseTransform
from examples.calculated_field_transform import CalculatedFieldTransform
from examples.filewriter_action import FileWriterAction

# Use the uppercase transform
transform = UpperCaseTransform()
transform.init()
result = transform.process_row({"name": "alice", "city": "NYC"})
transform.dispose()
print(result)  # {'name': 'ALICE', 'city': 'NYC'}

# Use the calculated field transform
calc = CalculatedFieldTransform()
calc.configure("quantity", "price", "total")
calc.init()
result = calc.process_row({"quantity": 5, "price": 10.0})
calc.dispose()
print(result)  # {'quantity': 5, 'price': 10.0, 'total': 50.0}

# Use the file writer action
action = FileWriterAction()
action.set_parameter("filepath", "/tmp/test.txt")
action.set_parameter("message", "Hello from PyHop!")
success = action.execute()
print(f"Success: {success}")
```

## Step 5: Run the Demo

PyHop includes a comprehensive demo:

```bash
python demo.py
```

This demonstrates:
- Transform plugins processing data
- Action plugins executing tasks
- Plugin registry functionality

## Next Steps

### Learn More

- **[Installation Guide](docs/installation.md)** - Detailed installation and setup
- **[Plugin Development Guide](docs/plugin-development.md)** - Comprehensive guide to creating plugins
- **[API Reference](docs/api-reference.md)** - Complete API documentation

### Explore Examples

Check out the `examples/` directory for:
- `uppercase_transform.py` - Simple text transformation
- `calculated_field_transform.py` - Field calculations
- `filewriter_action.py` - File operations
- `http_request_action.py` - HTTP requests

### Use Templates

Start with a template from `templates/`:

```bash
# Copy a template
cp templates/transform_template.py my_plugins/my_transform.py

# Edit and customize
# nano my_plugins/my_transform.py
```

### Create Your Own Plugins

Follow this pattern:

```python
from pyhop import HopTransform, plugin_registry

class MyCustomTransform(HopTransform):
    def __init__(self, name="MyTransform", description=""):
        super().__init__(name, description or "My custom transform")
        # Your initialization here

    def get_id(self):
        return "python.transform.my_custom"  # Unique ID

    def init(self):
        # Setup (called once before processing)
        pass

    def process_row(self, row):
        # Your transformation logic
        row['new_field'] = "processed"
        return row

    def dispose(self):
        # Cleanup (called once after processing)
        pass

# Register
plugin_registry.register(MyCustomTransform)
```

## Common Use Cases

### Data Validation

```python
class ValidatorTransform(HopTransform):
    def get_id(self):
        return "python.transform.validator"

    def process_row(self, row):
        # Filter out invalid rows
        if row.get('age', 0) < 0:
            return None  # Skip invalid rows

        # Add validation flag
        row['valid'] = True
        return row
```

### Data Enrichment

```python
class EnrichmentTransform(HopTransform):
    def get_id(self):
        return "python.transform.enrichment"

    def process_row(self, row):
        # Add calculated fields
        row['full_name'] = f"{row['first_name']} {row['last_name']}"
        row['age_group'] = 'adult' if row['age'] >= 18 else 'minor'
        return row
```

### File Operations

```python
class BackupAction(HopAction):
    def get_id(self):
        return "python.action.backup"

    def execute(self):
        import shutil
        source = self.get_parameter('source')
        dest = self.get_parameter('destination')
        shutil.copy2(source, dest)
        return True
```

## Troubleshooting

### Import Error

```python
# Error: ModuleNotFoundError: No module named 'pyhop'
# Solution: Install PyHop
pip install pyhop
```

### Plugin Not Found

```python
# Error: Plugin with ID '...' is already registered
# Solution: Use unique plugin IDs
def get_id(self):
    return "python.transform.mycompany.myplugin"  # Namespaced ID
```

## Getting Help

- **Documentation**: Check `docs/` directory
- **Examples**: Look at `examples/` directory
- **Issues**: [GitHub Issues](https://github.com/metaodi/pyhop/issues)
- **Discussions**: [GitHub Discussions](https://github.com/metaodi/pyhop/discussions)

## What's Next?

1. **Build Your Plugin**: Start with templates and examples
2. **Test Thoroughly**: Write unit tests for your plugins
3. **Share**: Contribute your plugins to the community
4. **Integrate**: Use your plugins in Apache Hop pipelines

Happy coding! 🚀
