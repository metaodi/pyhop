"""
Example Python Action Plugin - HTTP Request.

This example demonstrates a more advanced action that makes
HTTP requests.
"""

from typing import Any, Dict
from pyhop import HopAction, plugin_registry
import json


class HTTPRequestAction(HopAction):
    """
    An action that makes HTTP requests.

    This example demonstrates how to interact with external APIs.
    """

    def __init__(self, name: str = "HTTPRequest", description: str = ""):
        """Initialize the HTTPRequest action."""
        if not description:
            description = "Makes an HTTP request to a specified URL"
        super().__init__(name, description)
        self.set_parameter("url", "")
        self.set_parameter("method", "GET")
        self.set_parameter("headers", {})
        self.set_parameter("body", "")
        self.set_parameter("timeout", 30)

    def get_id(self) -> str:
        """Return the unique identifier for this plugin."""
        return "python.action.http_request"

    def execute(self) -> bool:
        """
        Execute the HTTP request.

        Returns:
            True if request succeeded (status 200-299), False otherwise
        """
        try:
            # Note: In a real implementation, you'd use the requests library
            # This is a simplified example
            import urllib.request
            import urllib.error

            url = self.get_parameter("url")
            method = self.get_parameter("method", "GET")
            headers = self.get_parameter("headers", {})
            body = self.get_parameter("body", "")
            timeout = self.get_parameter("timeout", 30)

            if not url:
                print("Error: URL is required")
                return False

            # Create request
            data = body.encode('utf-8') if body else None
            req = urllib.request.Request(url, data=data, method=method)

            # Add headers
            for key, value in headers.items():
                req.add_header(key, value)

            # Make request
            with urllib.request.urlopen(req, timeout=timeout) as response:
                status_code = response.getcode()
                response_body = response.read().decode('utf-8')

                print(f"HTTP {method} {url}")
                print(f"Status: {status_code}")
                print(f"Response: {response_body[:100]}...")  # First 100 chars

                # Consider 2xx status codes as success
                return 200 <= status_code < 300

        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            return False
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
            return False
        except Exception as e:
            print(f"Error making HTTP request: {e}")
            return False


# Register the plugin
plugin_registry.register(HTTPRequestAction)
