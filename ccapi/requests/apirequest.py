"""This module contains the APIRequest class.

This is the base class for Cloud Commerce Pro API requests.
"""

from . ccapisession import CloudCommerceAPISession


class APIRequest:
    """Base class for Cloud Commerce Pro API requests."""

    uri = None

    def __new__(self):
        """Create new API request."""
        self.headers = self.get_headers(self)
        self.data = self.get_data(self)
        self.params = self.get_params(self)
        response = CloudCommerceAPISession.api_request(self)
        return self.process_response(self, response)

    def get_data(self):
        """Get data for request."""
        return {}

    def get_params(self):
        """Get headers for request."""
        return {}

    def get_headers(self):
        """Get parameters for get request."""
        return {}

    def process_response(self, response):
        """Handle request response."""
        return response.json()
