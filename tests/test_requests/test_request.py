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

    def assertDataSent(self, data_key, expected_value):
        """Test the last request body contained the correct data."""
        sent_data = self.get_last_request_data()
        self.assertDataValueEqual(sent_data, data_key, expected_value)

    def assertQuerySent(self, data_key, expected_value):
        """Test the last request URL query contained the correct data."""
        data_key = data_key.lower()
        sent_data = self.get_last_request_query()
        self.assertDataValueEqual(sent_data, data_key, expected_value)

    def assertDataValueEqual(self, sent_data, data_key, expected_value):
        """Test that request data contains the correct data."""
        self.assertIsNotNone(sent_data.get(data_key), None)
        if isinstance(expected_value, list):
            self.assertEqual(
                sent_data[data_key], [str(value) for value in expected_value])
        else:
            self.assertEqual(sent_data[data_key][0], [str(expected_value)][0])
