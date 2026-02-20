# PyHop - Python Plugins for Apache Hop

PyHop is a Python framework that enables developers to create Apache Hop plugins using Python instead of Java. This makes it easier for Python developers to extend Apache Hop's functionality with custom transforms, actions, and other plugin types.

## What is Apache Hop?

[Apache Hop](https://hop.apache.org/) (Hop Orchestration Platform) is an open-source data orchestration and ETL (Extract, Transform, Load) platform. It provides a visual environment for designing data pipelines and workflows, with support for various execution engines and data sources.

## Why PyHop?

While Apache Hop is primarily Java-based, many data engineers and scientists prefer Python for data processing tasks. PyHop bridges this gap by:

- **Enabling Python development**: Write Hop plugins in Python using familiar libraries and tools
- **Simplifying plugin creation**: Provides a clean, Pythonic API for plugin development
- **Leveraging Python ecosystem**: Use popular Python libraries (pandas, numpy, scikit-learn, etc.) in your Hop pipelines
- **Reducing complexity**: No need to learn Java to extend Hop's functionality

## Features

- **Transform Plugins**: Create custom data transformation steps for pipelines
- **Action Plugins**: Build workflow actions for file operations, API calls, and more
- **Plugin Discovery**: Automatic discovery and registration of Python plugins
- **Easy Integration**: Designed to work seamlessly with Apache Hop's plugin system
- **Extensible Architecture**: Clean base classes and interfaces for different plugin types

## Quick Start

### Installation

```bash
pip install pyhop
```

Or install from source:

```bash
git clone https://github.com/metaodi/pyhop.git
cd pyhop
pip install -e .
```

### Your First Plugin

Create a simple transform plugin:

```python
from pyhop import HopTransform, plugin_registry

class UpperCaseTransform(HopTransform):
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

## Documentation

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Plugin Development Guide](docs/plugin-development.md) - Learn how to create plugins
- [API Reference](docs/api-reference.md) - Complete API documentation
- [Examples](examples/) - Example plugin implementations

## Plugin Types

PyHop currently supports the following plugin types:

### Transform Plugins
Used in pipelines to process data rows. Inherit from `HopTransform` and implement the `process_row()` method.

**Examples:**
- Data validation and cleaning
- Field calculations and transformations
- Data enrichment from external sources
- Format conversions

### Action Plugins
Used in workflows to perform specific tasks. Inherit from `HopAction` and implement the `execute()` method.

**Examples:**
- File operations (copy, move, delete)
- HTTP/API requests
- Email notifications
- Database operations

## Project Structure

```
pyhop/
├── pyhop/              # Core framework
│   ├── __init__.py     # Package initialization
│   ├── base.py         # Base plugin classes
│   └── plugin.py       # Plugin registry and discovery
├── examples/           # Example plugins
│   ├── uppercase_transform.py
│   ├── calculated_field_transform.py
│   ├── filewriter_action.py
│   └── http_request_action.py
├── docs/               # Documentation
│   ├── installation.md
│   ├── plugin-development.md
│   └── api-reference.md
├── tests/              # Unit tests
├── pyproject.toml      # Project configuration
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Requirements

- Python 3.8 or higher
- Apache Hop 2.0 or higher (for integration)
- JPype1 1.4.1+ (for Java-Python bridge)

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/metaodi/pyhop.git
cd pyhop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

### Running tests

```bash
pytest tests/
```

### Code formatting

```bash
black pyhop/ examples/ tests/
flake8 pyhop/ examples/ tests/
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development workflow
- Submitting pull requests
- Coding standards

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/metaodi/pyhop/issues)
- **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/metaodi/pyhop/discussions)
- **Apache Hop**: Visit [hop.apache.org](https://hop.apache.org/) for Apache Hop documentation

## Roadmap

- [ ] Full Java-Python bridge implementation
- [ ] Support for additional plugin types (Database, Engine, etc.)
- [ ] Visual plugin configuration UI integration
- [ ] Plugin packaging and distribution tools
- [ ] Performance optimizations
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline

## Acknowledgments

- [Apache Hop](https://hop.apache.org/) - The core platform
- [JPype](https://jpype.readthedocs.io/) - Java-Python integration
- All contributors and the Apache Hop community

## Links

- **PyHop Repository**: https://github.com/metaodi/pyhop
- **Apache Hop**: https://hop.apache.org/
- **Apache Hop GitHub**: https://github.com/apache/hop
- **Documentation**: https://hop.apache.org/manual/latest/
