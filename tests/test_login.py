"""Test the login process."""

from ccapi.requests.ccapisession import CloudCommerceAPISession

from .test_CCAPI import TestCCAPI


class TestCloudCommerceAPISession(TestCCAPI):
    """Test the login process."""

    def test_login(self):
        """Test the login process."""
        username = 'USERNAME'
        password = 'PASSWORD'
        CloudCommerceAPISession.get_session(
            username=username, password=password)
        self.assertEqual(CloudCommerceAPISession.username, username)
        self.assertEqual(CloudCommerceAPISession.password, password)
        self.assertTrue(CloudCommerceAPISession.is_logged_in())
