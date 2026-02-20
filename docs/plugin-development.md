# Plugin Development Guide

This comprehensive guide will teach you how to create Python plugins for Apache Hop using PyHop.

## Table of Contents

1. [Plugin Basics](#plugin-basics)
2. [Transform Plugins](#transform-plugins)
3. [Action Plugins](#action-plugins)
4. [Plugin Registration](#plugin-registration)
5. [Best Practices](#best-practices)
6. [Testing Plugins](#testing-plugins)
7. [Packaging and Distribution](#packaging-and-distribution)

## Plugin Basics

### What is a Plugin?

A plugin is a Python class that extends Apache Hop's functionality. PyHop provides base classes that you inherit from to create different types of plugins.

### Plugin Types

PyHop currently supports two main plugin types:

- **Transform Plugins** (`HopTransform`): Process data rows in pipelines
- **Action Plugins** (`HopAction`): Perform tasks in workflows

### Plugin Structure

All plugins must:

1. Inherit from a base plugin class (`HopTransform`, `HopAction`, etc.)
2. Implement required abstract methods
3. Have a unique plugin ID
4. Be registered with the plugin registry

## Transform Plugins

Transform plugins process data rows in Apache Hop pipelines. They receive rows, transform them, and output the results.

### Basic Transform Plugin

Here's a minimal transform plugin:

```python
from pyhop import HopTransform, plugin_registry

class MyTransform(HopTransform):
    """A simple transform plugin."""

    def __init__(self, name="MyTransform", description=""):
        super().__init__(name, description or "My custom transform")

    def get_id(self):
        """Return unique plugin ID."""
        return "python.transform.mytransform"

    def process_row(self, row):
        """Process a single row."""
        # Your transformation logic here
        return row

# Register the plugin
plugin_registry.register(MyTransform)
```

### Transform Lifecycle

Transform plugins have a specific lifecycle:

1. **`__init__()`**: Plugin is instantiated
2. **`init()`**: Called once before processing starts (setup)
3. **`process_row()`**: Called for each data row
4. **`dispose()`**: Called once after processing ends (cleanup)

Example with lifecycle methods:

```python
from pyhop import HopTransform, plugin_registry

class LifecycleTransform(HopTransform):
    def __init__(self, name="LifecycleTransform", description=""):
        super().__init__(name, description or "Transform with lifecycle")
        self.row_count = 0
        self.connection = None

    def get_id(self):
        return "python.transform.lifecycle"

    def init(self):
        """Initialize resources before processing."""
        print("Initializing transform...")
        self.row_count = 0
        # Open database connections, files, etc.
        # self.connection = open_database_connection()

    def process_row(self, row):
        """Process each row."""
        self.row_count += 1
        row['row_number'] = self.row_count
        return row

    def dispose(self):
        """Clean up resources after processing."""
        print(f"Processed {self.row_count} rows")
        # Close connections, files, etc.
        # if self.connection:
        #     self.connection.close()

plugin_registry.register(LifecycleTransform)
```

### Accessing Row Data

Rows are passed as dictionaries with field names as keys:

```python
def process_row(self, row):
    # Access fields
    name = row.get('name', '')
    age = row.get('age', 0)

    # Modify fields
    row['name'] = name.upper()
    row['age'] = age + 1

    # Add new fields
    row['full_name'] = f"{row['first_name']} {row['last_name']}"

    # Filter out rows (return None)
    if age < 18:
        return None

    return row
```

### Field Definitions

Define input and output fields:

```python
class FieldAwareTransform(HopTransform):
    def __init__(self, name="FieldAware", description=""):
        super().__init__(name, description)
        # Define expected input fields
        self.input_fields = ['first_name', 'last_name', 'age']
        # Define output fields this transform adds
        self.output_fields = ['full_name', 'age_group']

    def get_id(self):
        return "python.transform.fieldaware"

    def process_row(self, row):
        row['full_name'] = f"{row['first_name']} {row['last_name']}"

        age = row.get('age', 0)
        if age < 18:
            row['age_group'] = 'minor'
        elif age < 65:
            row['age_group'] = 'adult'
        else:
            row['age_group'] = 'senior'

        return row

plugin_registry.register(FieldAwareTransform)
```

### Advanced Transform Example

A more complex transform with configuration:

```python
from pyhop import HopTransform, plugin_registry
import re

class DataCleanerTransform(HopTransform):
    """Clean and validate data fields."""

    def __init__(self, name="DataCleaner", description=""):
        super().__init__(name, description or "Clean and validate data")
        self.email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        self.phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        self.validation_errors = []
        self.fields_to_clean = []

    def get_id(self):
        return "python.transform.datacleaner"

    def configure(self, fields_to_clean):
        """Configure which fields to clean."""
        self.fields_to_clean = fields_to_clean

    def init(self):
        self.validation_errors = []

    def process_row(self, row):
        # Clean whitespace from all string fields
        for field in self.fields_to_clean:
            if field in row and isinstance(row[field], str):
                row[field] = row[field].strip()

        # Validate email
        if 'email' in row:
            email = row['email']
            if not self.email_pattern.match(email):
                self.validation_errors.append(f"Invalid email: {email}")
                row['email_valid'] = False
            else:
                row['email_valid'] = True

        # Clean and validate phone
        if 'phone' in row:
            phone = re.sub(r'[^\d+]', '', row['phone'])
            row['phone'] = phone
            row['phone_valid'] = bool(self.phone_pattern.match(phone))

        return row

    def dispose(self):
        if self.validation_errors:
            print(f"Validation errors: {len(self.validation_errors)}")
            for error in self.validation_errors[:10]:  # Show first 10
                print(f"  - {error}")

plugin_registry.register(DataCleanerTransform)
```

## Action Plugins

Action plugins perform tasks in Apache Hop workflows. They return True for success or False for failure.

### Basic Action Plugin

```python
from pyhop import HopAction, plugin_registry

class MyAction(HopAction):
    """A simple action plugin."""

    def __init__(self, name="MyAction", description=""):
        super().__init__(name, description or "My custom action")

    def get_id(self):
        """Return unique plugin ID."""
        return "python.action.myaction"

    def execute(self):
        """Execute the action."""
        # Your action logic here
        print("Action executed!")
        return True  # True for success, False for failure

# Register the plugin
plugin_registry.register(MyAction)
```

### Working with Parameters

Action plugins use parameters for configuration:

```python
from pyhop import HopAction, plugin_registry
import smtplib
from email.mime.text import MIMEText

class EmailAction(HopAction):
    """Send email notifications."""

    def __init__(self, name="EmailAction", description=""):
        super().__init__(name, description or "Send email notification")
        # Set default parameters
        self.set_parameter('smtp_server', 'smtp.gmail.com')
        self.set_parameter('smtp_port', 587)
        self.set_parameter('from_email', '')
        self.set_parameter('to_email', '')
        self.set_parameter('subject', 'Notification from Apache Hop')
        self.set_parameter('body', '')
        self.set_parameter('use_tls', True)

    def get_id(self):
        return "python.action.email"

    def execute(self):
        """Send the email."""
        try:
            # Get parameters
            server = self.get_parameter('smtp_server')
            port = self.get_parameter('smtp_port')
            from_email = self.get_parameter('from_email')
            to_email = self.get_parameter('to_email')
            subject = self.get_parameter('subject')
            body = self.get_parameter('body')
            use_tls = self.get_parameter('use_tls', True)

            # Create message
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email

            # Send email
            with smtplib.SMTP(server, port) as smtp:
                if use_tls:
                    smtp.starttls()
                smtp.send_message(msg)

            print(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

plugin_registry.register(EmailAction)
```

### File Operations Action

```python
from pyhop import HopAction, plugin_registry
import shutil
from pathlib import Path

class FileCopyAction(HopAction):
    """Copy files or directories."""

    def __init__(self, name="FileCopy", description=""):
        super().__init__(name, description or "Copy files or directories")
        self.set_parameter('source', '')
        self.set_parameter('destination', '')
        self.set_parameter('overwrite', False)

    def get_id(self):
        return "python.action.filecopy"

    def execute(self):
        """Execute the file copy."""
        try:
            source = Path(self.get_parameter('source'))
            destination = Path(self.get_parameter('destination'))
            overwrite = self.get_parameter('overwrite', False)

            # Validate source exists
            if not source.exists():
                print(f"Source does not exist: {source}")
                return False

            # Check if destination exists
            if destination.exists() and not overwrite:
                print(f"Destination exists and overwrite is False: {destination}")
                return False

            # Copy file or directory
            if source.is_file():
                shutil.copy2(source, destination)
                print(f"Copied file: {source} -> {destination}")
            elif source.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
                print(f"Copied directory: {source} -> {destination}")

            return True

        except Exception as e:
            print(f"File copy failed: {e}")
            return False

plugin_registry.register(FileCopyAction)
```

## Plugin Registration

### Method 1: Using the Decorator

The simplest way to register a plugin:

```python
from pyhop import HopTransform
from pyhop.plugin import register_plugin

@register_plugin
class MyTransform(HopTransform):
    def get_id(self):
        return "python.transform.mytransform"

    def process_row(self, row):
        return row
```

### Method 2: Manual Registration

Register plugins explicitly:

```python
from pyhop import HopTransform, plugin_registry

class MyTransform(HopTransform):
    def get_id(self):
        return "python.transform.mytransform"

    def process_row(self, row):
        return row

# Register manually
plugin_registry.register(MyTransform)
```

### Method 3: Auto-Discovery

Place plugins in a directory and use auto-discovery:

```python
from pyhop import plugin_registry

# Discover all plugins in a directory
count = plugin_registry.discover_plugins('/path/to/plugins')
print(f"Discovered {count} plugins")

# List all registered plugins
plugins = plugin_registry.list_plugins()
print(f"Registered plugins: {plugins}")
```

## Best Practices

### 1. Unique Plugin IDs

Use a consistent naming convention:

```python
# Good: Descriptive, namespaced IDs
"python.transform.uppercase"
"python.action.send_email"
"python.transform.datacleaner"

# Bad: Generic, collision-prone IDs
"transform"
"action1"
"myPlugin"
```

### 2. Error Handling

Always handle errors gracefully:

```python
def process_row(self, row):
    try:
        # Transformation logic
        result = complex_operation(row)
        return result
    except KeyError as e:
        print(f"Missing required field: {e}")
        return None  # Filter out invalid rows
    except Exception as e:
        print(f"Error processing row: {e}")
        # Decide: skip row or re-raise
        return None
```

### 3. Resource Management

Clean up resources properly:

```python
class DatabaseTransform(HopTransform):
    def init(self):
        self.connection = database.connect()

    def process_row(self, row):
        # Use self.connection
        return row

    def dispose(self):
        if self.connection:
            self.connection.close()
```

### 4. Logging

Use meaningful log messages:

```python
def process_row(self, row):
    print(f"Processing row {self.row_count}: {row.get('id')}")
    # Better: Use Python's logging module
    # import logging
    # logging.info(f"Processing row {self.row_count}")
```

### 5. Type Hints

Use type hints for better code quality:

```python
from typing import Dict, Any, Optional

def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process a row with type hints."""
    return row
```

### 6. Documentation

Document your plugins thoroughly:

```python
class WellDocumentedTransform(HopTransform):
    """
    Transform that does something useful.

    This transform processes data rows by performing XYZ operation.
    It expects the following input fields:
    - field1: Description of field1
    - field2: Description of field2

    And produces these output fields:
    - result: Description of result field

    Example:
        >>> transform = WellDocumentedTransform()
        >>> row = {'field1': 'value', 'field2': 42}
        >>> result = transform.process_row(row)
    """

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single data row.

        Args:
            row: Input row dictionary

        Returns:
            Transformed row, or None to filter out
        """
        # Implementation
        return row
```

## Testing Plugins

### Unit Tests

Create unit tests for your plugins:

```python
# test_mytransform.py
import pytest
from my_plugins.mytransform import UpperCaseTransform

def test_uppercase_transform():
    """Test uppercase transformation."""
    transform = UpperCaseTransform()
    transform.init()

    # Test data
    input_row = {'name': 'john', 'city': 'boston'}
    expected = {'name': 'JOHN', 'city': 'BOSTON'}

    # Process
    result = transform.process_row(input_row)

    # Assert
    assert result == expected

    transform.dispose()

def test_uppercase_with_numbers():
    """Test that numbers are not affected."""
    transform = UpperCaseTransform()

    input_row = {'name': 'john', 'age': 30}
    result = transform.process_row(input_row)

    assert result['name'] == 'JOHN'
    assert result['age'] == 30
```

### Integration Tests

Test plugins with actual data:

```python
def test_plugin_with_real_data():
    """Test plugin with realistic data."""
    transform = DataCleanerTransform()
    transform.configure(['name', 'email'])
    transform.init()

    # Real-world data
    rows = [
        {'name': '  John Doe  ', 'email': 'john@example.com'},
        {'name': 'Jane Smith', 'email': 'invalid-email'},
        {'name': 'Bob  ', 'email': 'bob@test.org'},
    ]

    results = [transform.process_row(row) for row in rows]

    # Verify
    assert results[0]['name'] == 'John Doe'
    assert results[0]['email_valid'] == True
    assert results[1]['email_valid'] == False

    transform.dispose()
```

## Packaging and Distribution

### Create a Plugin Package

Structure your plugin package:

```
my-hop-plugins/
├── setup.py
├── README.md
├── requirements.txt
├── my_hop_plugins/
│   ├── __init__.py
│   ├── transforms/
│   │   ├── __init__.py
│   │   ├── uppercase.py
│   │   └── datacleaner.py
│   └── actions/
│       ├── __init__.py
│       ├── email.py
│       └── filecopy.py
└── tests/
    ├── test_transforms.py
    └── test_actions.py
```

### setup.py

```python
from setuptools import setup, find_packages

setup(
    name='my-hop-plugins',
    version='1.0.0',
    description='Custom Apache Hop plugins in Python',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pyhop>=0.1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
    ],
)
```

### Distribution

Package and distribute your plugins:

```bash
# Build distribution
python setup.py sdist bdist_wheel

# Install locally
pip install -e .

# Upload to PyPI
pip install twine
twine upload dist/*
```

## Next Steps

- Explore [examples/](../examples/) for more plugin implementations
- Read the [API Reference](api-reference.md) for detailed class documentation
- Check the [Installation Guide](installation.md) for setup instructions
- Join the community and share your plugins!
