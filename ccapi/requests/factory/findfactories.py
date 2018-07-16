"""
FindFactories request.

Get list of suppliers.
"""

from ccapi.cc_objects import Factories, Factory

from ..apirequest import APIRequest


class FindFactories(APIRequest):
    """FindFactories request."""

    uri = '/Handlers/Factory/FindFactories.ashx'

    def get_data(self):
        """Get data for request."""
        data = {'ProgType': 'extended'}
        return data

    def process_response(self, response):
        """Handle request response."""
        data = response.json()
        return Factories([Factory(factory) for factory in data])
