"""TestCCAPI - The base class for CCAPI tests."""

import unittest
import urllib

import requests_mock
from ccapi.requests.ccapisession import CloudCommerceAPISession


class TestCCAPI(unittest.TestCase):
    """TestCCAPI - The base class for CCAPI tests."""

    DOMAIN = 'http://seatontradingcompany.cloudcommercepro.com/'
    LOGIN_HANDLER_URI = 'Handlers/loginHandler.ashx'

    def setUp(self):
        """Mock session and login."""
        self.set_mock_session()
        self.mock_login()

    def register_uri(self, method, url, response_list=None, **kwargs):
        """Register a URI with the mock adapter."""
        self.adapter.register_uri(
            method, url, response_list=response_list, **kwargs)

    def register_request(self, request_class, *args, **kwargs):
        """Register mock URI for a request class."""
        uri = self.cloud_commerce_URI(request_class.uri)
        self.register_uri(kwargs.pop('method', 'POST'), uri, *args, **kwargs)

    def cloud_commerce_URI(self, uri):
        """Return URI for the Cloud Commerce domain."""
        return self.DOMAIN + uri

    def set_mock_session(self):
        """Mount mock adapters to the session."""
        self.adapter = requests_mock.Adapter()
        CloudCommerceAPISession.session.mount('https://', self.adapter)
        CloudCommerceAPISession.session.mount('http://', self.adapter)
        self.set_login_URIs()

    def set_login_URIs(self):
        """Add login URIs to mock adapter."""
        self.register_uri('POST', self.DOMAIN, text='mock_text')
        self.register_uri(
            'GET', self.cloud_commerce_URI(self.LOGIN_HANDLER_URI))

    def mock_login(self):
        """Mock the login process."""
        username = 'USERNAME'
        password = 'PASSWORD'
        CloudCommerceAPISession.get_session(
            username=username, password=password)

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
            for value in expected_value:
                self.assertIn(str(value), str(sent_data[data_key]))
        else:
            self.assertEqual(sent_data[data_key][0], [str(expected_value)][0])

    def assertDataValueIsNone(self, data_key):
        """Test that request data contains the correct data."""
        sent_data = self.get_last_request_data()
        self.assertIsNone(sent_data.get(data_key), None)
