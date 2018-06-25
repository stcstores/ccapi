"""TestRequest - The base class for request tests."""

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
