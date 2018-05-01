"""This module contains the APIRequest class.

This is the base class for Cloud Commerce Pro API requests.
"""

import http
import json

from ccapi import exceptions

from .ccapisession import CloudCommerceAPISession


class APIRequest:
    """Base class for Cloud Commerce Pro API requests."""

    uri = None

    def __new__(self):
        """Create new API request."""
        self.headers = self.get_headers(self)
        self.data = self.get_data(self)
        self.params = self.get_params(self)
        self.files = self.get_files(self)
        try:
            response = CloudCommerceAPISession.api_request(self)
        except http.client.RemoteDisconnected as e:
            raise exceptions.CloudCommerceNoResponseError from e
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
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise NonJSONResponse(response.text)
        return data

    def get_files(self):
        """Get file for request."""
        return {}


class NonJSONResponse(Exception):
    """Attempted to JSON decode string which was not valid JSON."""

    def __init__(self, response_text):
        """Create NonJSONResponse."""
        self.response_text = response_text
