"""Test the login process."""

import datetime
import time

from ccapi import requests
from ccapi.requests.ccapisession import CloudCommerceAPISession

from .test_CCAPI import TestCCAPI


class TestCloudCommerceAPISession(TestCCAPI):
    """Test the login process."""

    def setUp(self):
        """Mock session."""
        super().setUp()
        self.original_timeout = CloudCommerceAPISession.timeout

    def tearDown(self):
        """Reset class variables."""
        CloudCommerceAPISession.timeout = self.original_timeout

    def test_login_handler_request_is_made(self):
        """Test that the login handler request is made at login."""
        self.assertURIused(self.LOGIN_HANDLER_URI)

    def test_login_sets_the_domain(self):
        """Test that the session domain is set when the session is created."""
        self.assertEqual(CloudCommerceAPISession.domain, self.DOMAIN)

    def test_login_sets_the_username(self):
        """Test that the session username is set when the session is created."""
        self.assertEqual(CloudCommerceAPISession.username, self.USERNAME)

    def test_login_sets_the_password(self):
        """Test that the session password is set when the session is created."""
        self.assertEqual(CloudCommerceAPISession.password, self.PASSWORD)

    def test_session_timeout(self):
        """Test the session_logout."""
        CloudCommerceAPISession.timeout = datetime.timedelta(seconds=0.25)
        self.mock_login()
        self.assertFalse(CloudCommerceAPISession.session_timed_out())
        time.sleep(0.3)
        self.assertTrue(CloudCommerceAPISession.session_timed_out())

    def test_session_is_recreated_if_timed_out(self):
        """Test that a new session is created if a request is made and it has timed out."""
        self.register_request(
            requests.ProductOperations,
            json={
                "Success": None,
                "Message": None,
                "RecordCount": 1,
                "Data": "VSG-H3R-G0R",
            },
        )
        CloudCommerceAPISession.timeout = datetime.timedelta(seconds=0.25)
        self.mock_login()
        time.sleep(0.3)
        self.assertTrue(CloudCommerceAPISession.session_timed_out())
        requests.ProductOperations("getgeneratedsku")
        self.assertFalse(CloudCommerceAPISession.session_timed_out())
