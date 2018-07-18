"""TestCCAPI - The base class for CCAPI tests."""

import json
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

    def get_sent_request(self, skip=1):
        """
        Return a recently made request.

        Kwargs:
            skip: The number of requests to skip. 0 will retrun the most recent
            request, 1 will return the one before that etc. Default: 0.
        """
        return self.adapter.request_history[-skip]

    def get_sent_request_query(self, request=None):
        """Return the data sent in a previous request's URL."""
        if request is None:
            request = self.get_sent_request()
        return urllib.parse.parse_qs(request.query)

    def get_sent_request_data(self, request=None):
        """Return the data sent in a previous request's body."""
        if request is None:
            request = self.get_sent_request()
        return urllib.parse.parse_qs(request.text)

    def get_executed_request_json(self, request=None):
        """Return parsed JSON sent in a previous request."""
        if request is None:
            request = self.get_sent_request()
        return json.loads(self.adapter.request_history[-1].text)

    def assertDataSent(self, data_key, expected_value, request=None):
        """Test the last request body contained the correct data."""
        if request is None:
            request = self.get_sent_request()
        sent_data = self.get_sent_request_data(request=request)
        self.assertDataValueEqual(sent_data, data_key, expected_value)

    def assertQuerySent(self, data_key, expected_value, request=None):
        """Test the last request URL query contained the correct data."""
        if request is None:
            request = self.get_sent_request()
        sent_data = self.get_sent_request_query(request=request)
        data_key = data_key.lower()
        self.assertDataValueEqual(sent_data, data_key, expected_value)

    def assertDataValueIsNotNone(self, sent_data, data_key):
        """Raise AssertionError if sent value is None."""
        if sent_data.get(data_key) is None:
            raise AssertionError(
                f'Sent value "{data_key}" was unexpectedly None.')

    def assertListSent(self, sent_data, data_key, expected_values):
        """Raise Assertion Error if expected values are not in sent data."""
        missing_values = [
            value for value in expected_values
            if str(value) not in str(sent_data[data_key])
        ]
        if missing_values:
            raise AssertionError(
                (
                    f'Values {", ".join(missing_values)} not sent in data '
                    f'key {data_key}. The value sent was '
                    f'"{sent_data[data_key]}"'))

    def assertDataValueEqual(self, sent_data, data_key, expected_value):
        """Test that request data contains the correct data."""
        self.assertDataValueIsNotNone(sent_data, data_key)
        if isinstance(expected_value, list):
            self.assertListSent(sent_data, data_key, expected_value)
        else:
            if sent_data[data_key][0] != [str(expected_value)][0]:
                raise AssertionError(
                    (
                        f'Value "{expected_value}" was not sent for data key '
                        f'"{data_key}". "{sent_data[data_key]}" was sent.'))

    def assertJsonValueSent(self, data_key, expected_value, request=None):
        """Test that a value was sent in the JSON body of the last request."""
        if request is None:
            request = self.get_sent_request()
        sent_data = self.get_executed_request_json(request=request)
        if isinstance(expected_value, list):
            self.assertListSent(sent_data, data_key, expected_value)
        else:
            if sent_data[data_key] != expected_value:
                raise AssertionError(
                    (
                        f'"{expected_value}" was not sent for data key '
                        f'"{data_key}". "{sent_data[data_key]}" was sent '
                        'instead.'))

    def assertDataValueIsNone(self, data_key, request=None):
        """Test that request data contains the correct data."""
        if request is None:
            request = self.get_sent_request()
        sent_data = self.get_sent_request_data(request=request)
        self.assertIsNone(sent_data.get(data_key), None)

    def assertRequestUsesRequestClassURI(self, request, request_class):
        """Test that a sent request uses the URI of a request class."""
        if request_class.uri not in request.url:
            raise AssertionError(
                (
                    f'Request expected to use URI "{request_class.uri}", used '
                    '"{request.url}"'))
