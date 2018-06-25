"""TestCCAPI - The base class for CCAPI tests."""

import unittest

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
