"""TestRequest - The base class for request tests."""

from ..test_CCAPI import TestCCAPI


class TestRequest(TestCCAPI):
    """TestRequest - The base class for request tests."""

    METHOD = "POST"

    def mock_request(self, *args, **kwargs):
        """Make mock request."""
        return self.request_class(*args, **kwargs)

    def register(self, *args, **kwargs):
        """Register request URI."""
        if "method" not in kwargs:
            kwargs["method"] = self.METHOD
        self.register_request(self.request_class, *args, **kwargs)
