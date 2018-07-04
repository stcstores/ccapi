"""TestRequest - The base class for request tests."""

import urllib

from ..test_CCAPI import TestCCAPI


class TestRequest(TestCCAPI):
    """TestRequest - The base class for request tests."""

    METHOD = 'POST'

    def mock_request(self, *args, **kwargs):
        """Make mock request."""
        return self.request_class(*args, **kwargs)

    def register(self, *args, **kwargs):
        """Register request URI."""
        uri = self.cloud_commerce_URI(self.request_class.uri)
        self.register_uri(self.METHOD, uri, *args, **kwargs)

    def get_last_request_query(self):
        """Return the data sent in the last request URL."""
        return urllib.parse.parse_qs(self.adapter.request_history[-1].query)

    def get_last_request_data(self):
        """Return the data sent in the last request body."""
        return urllib.parse.parse_qs(self.adapter.request_history[-1].text)
