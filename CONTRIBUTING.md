# Contributing to PyHop

Thank you for your interest in contributing to PyHop! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. A clear, descriptive title
2. Steps to reproduce the bug
3. Expected behavior
4. Actual behavior
5. Your environment (Python version, OS, PyHop version)
6. Any relevant code samples or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. A clear description of the enhancement
2. Use cases and examples
3. Why this enhancement would be useful
4. Any potential implementation ideas

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install development dependencies**: `pip install -r requirements-dev.txt`
3. **Make your changes** following our coding standards
4. **Add tests** for any new functionality
5. **Update documentation** as needed
6. **Run tests** to ensure everything works: `pytest`
7. **Format your code**: `black pyhop/ examples/ tests/`
8. **Lint your code**: `flake8 pyhop/ examples/ tests/`
9. **Commit your changes** with clear commit messages
10. **Push to your fork** and submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pyhop.git
cd pyhop

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 100)
- Use [flake8](https://flake8.pycqa.org/) for linting
- Use type hints where appropriate
- Write docstrings for all public classes and methods (Google style)

### Example

```python
from typing import Dict, Any, Optional


class MyPlugin(HopTransform):
    """
    Brief description of the plugin.

    Detailed description explaining what it does,
    how to use it, and any important notes.

    Args:
        name: The plugin name
        description: Plugin description

    Example:
        >>> plugin = MyPlugin("test")
        >>> result = plugin.process_row({"field": "value"})
    """

    def __init__(self, name: str, description: str = "") -> None:
        super().__init__(name, description)

    def process_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single row.

        Args:
            row: Input row as dictionary

        Returns:
            Processed row or None to filter out
        """
        return row
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Use `pytest` for testing
- Aim for high code coverage
- Test both success and failure cases

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyhop --cov-report=html

# Run specific test file
pytest tests/test_base.py

# Run specific test
pytest tests/test_base.py::test_transform_plugin
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def my_function(arg1: str, arg2: int) -> bool:
    """
    Brief description.

    Longer description with more details.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    """
    pass
```

### Documentation Files

- Update relevant `.md` files in `docs/` directory
- Keep documentation clear and concise
- Include code examples where helpful
- Update the README.md if adding major features

## Commit Messages

Write clear, descriptive commit messages:

```
Add uppercase transform plugin

- Implement UpperCaseTransform class
- Add unit tests for uppercase transformation
- Update documentation with usage example
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (if needed)
- List of changes (if multiple)

## Pull Request Process

1. Update the README.md and documentation with details of changes
2. Update the CHANGELOG.md (if exists) with your changes
3. Ensure all tests pass and code is properly formatted
4. The PR will be merged once reviewed and approved

## Plugin Contribution Guidelines

When contributing plugins:

1. **Unique ID**: Use a descriptive, namespaced ID
2. **Documentation**: Include comprehensive docstrings
3. **Tests**: Provide unit tests for your plugin
4. **Examples**: Add usage examples
5. **Dependencies**: Minimize external dependencies
6. **Error Handling**: Handle errors gracefully
7. **Resources**: Clean up resources in `dispose()` method

## Questions?

If you have questions:

- Check existing [Issues](https://github.com/metaodi/pyhop/issues)
- Create a new issue with the "question" label
- Reach out on [GitHub Discussions](https://github.com/metaodi/pyhop/discussions)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
