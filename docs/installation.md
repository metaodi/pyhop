# Installation Guide

This guide provides detailed instructions for installing PyHop and setting it up to work with Apache Hop.

## Prerequisites

Before installing PyHop, ensure you have the following:

- **Python 3.8 or higher**: PyHop requires Python 3.8+
- **pip**: Python package manager (usually included with Python)
- **Apache Hop 2.0+**: Download from [hop.apache.org](https://hop.apache.org/)
- **Java 17**: Required by Apache Hop

## Installation Methods

### Method 1: Install from PyPI (Recommended)

Once PyHop is published to PyPI, you can install it with:

```bash
pip install pyhop
```

### Method 2: Install from Source

For development or to use the latest features:

```bash
# Clone the repository
git clone https://github.com/metaodi/pyhop.git
cd pyhop

# Install in editable mode
pip install -e .
```

### Method 3: Install from GitHub

Install directly from GitHub without cloning:

```bash
pip install git+https://github.com/metaodi/pyhop.git
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv pyhop-env

# Activate on Linux/macOS
source pyhop-env/bin/activate

# Activate on Windows
pyhop-env\Scripts\activate

# Install PyHop
pip install pyhop
```

## Verifying Installation

Verify that PyHop is installed correctly:

```python
import pyhop
print(pyhop.__version__)
```

You should see the version number (e.g., `0.1.0`).

## Setting Up Apache Hop Integration

To use Python plugins with Apache Hop, you need to configure the integration:

### Step 1: Install Apache Hop

1. Download Apache Hop from [hop.apache.org/download/](https://hop.apache.org/download/)
2. Extract the archive to a directory (e.g., `/opt/hop`)
3. Set the `HOP_HOME` environment variable:

```bash
# Linux/macOS
export HOP_HOME=/opt/hop

# Windows
set HOP_HOME=C:\hop
```

### Step 2: Configure Python Environment

Apache Hop needs to know where to find Python and PyHop:

1. Create a configuration file: `$HOP_HOME/config/python-config.json`

```json
{
  "pythonExecutable": "/path/to/python",
  "pythonPath": [
    "/path/to/pyhop",
    "/path/to/your/plugins"
  ],
  "virtualEnv": "/path/to/pyhop-env"
}
```

2. Alternatively, set environment variables:

```bash
export PYHOP_PYTHON=/usr/bin/python3
export PYHOP_PATH=/home/user/pyhop:/home/user/my-plugins
```

### Step 3: Install JPype (Java-Python Bridge)

JPype enables communication between Java (Apache Hop) and Python:

```bash
pip install JPype1
```

Verify JPype installation:

```python
import jpype
print(jpype.__version__)
```

### Step 4: Configure Hop Python Plugin Loader

Create or edit `$HOP_HOME/config/hop-config.json` to enable Python plugins:

```json
{
  "plugins": {
    "python": {
      "enabled": true,
      "pluginDirectories": [
        "/home/user/my-python-plugins",
        "/home/user/pyhop/examples"
      ],
      "autoDiscovery": true
    }
  }
}
```

## Installing Development Dependencies

For plugin development, install additional tools:

```bash
pip install -r requirements-dev.txt
```

This installs:
- `pytest` - Testing framework
- `pytest-cov` - Code coverage
- `black` - Code formatter
- `flake8` - Linter
- `mypy` - Type checker

## Platform-Specific Notes

### Linux

Most distributions come with Python 3. Install pip if needed:

```bash
# Debian/Ubuntu
sudo apt-get install python3-pip

# Fedora/RHEL
sudo dnf install python3-pip
```

### macOS

Use Homebrew to install Python:

```bash
brew install python3
pip3 install pyhop
```

### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Open Command Prompt and run:

```cmd
pip install pyhop
```

## Docker Installation

Run PyHop in a Docker container:

```dockerfile
FROM python:3.11-slim

# Install PyHop
RUN pip install pyhop

# Copy your plugins
COPY my-plugins/ /app/plugins/

WORKDIR /app
CMD ["python"]
```

Build and run:

```bash
docker build -t pyhop-env .
docker run -it pyhop-env
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pyhop'`

**Solution**: Ensure PyHop is installed in the correct Python environment:

```bash
python -m pip install pyhop
python -c "import pyhop; print(pyhop.__version__)"
```

### Issue: JPype fails to start JVM

**Solution**: Verify Java is installed and `JAVA_HOME` is set:

```bash
# Check Java
java -version

# Set JAVA_HOME (Linux/macOS)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk

# Set JAVA_HOME (Windows)
set JAVA_HOME=C:\Program Files\Java\jdk-17
```

### Issue: Python plugins not discovered by Hop

**Solution**: Check the plugin directory configuration:

1. Verify `hop-config.json` has correct paths
2. Ensure plugins are properly registered (use `@register_plugin` decorator)
3. Check Hop logs: `$HOP_HOME/logs/hop.log`

### Issue: Permission errors on Linux

**Solution**: Install in user directory or use virtual environment:

```bash
pip install --user pyhop
# or
python -m venv venv && source venv/bin/activate && pip install pyhop
```

## Upgrading PyHop

To upgrade to the latest version:

```bash
pip install --upgrade pyhop
```

To upgrade from source:

```bash
cd pyhop
git pull
pip install -e . --upgrade
```

## Uninstalling

To remove PyHop:

```bash
pip uninstall pyhop
```

## Next Steps

After installation:

1. Read the [Plugin Development Guide](plugin-development.md) to create your first plugin
2. Explore [examples/](../examples/) for sample implementations
3. Check the [API Reference](api-reference.md) for detailed documentation

## Getting Help

If you encounter issues:

- Check the [Troubleshooting](#troubleshooting) section above
- Search [GitHub Issues](https://github.com/metaodi/pyhop/issues)
- Create a new issue with:
  - Your Python version (`python --version`)
  - Your OS and version
  - PyHop version (`python -c "import pyhop; print(pyhop.__version__)"`)
  - Complete error message and stack trace
