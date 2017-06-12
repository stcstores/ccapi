"""This module contains the CloudCommerceAPISession class."""

import requests
from urllib.parse import urljoin


class CloudCommerceAPISession:
    """Contains session object."""

    domain = 'http://seatontradingcompany.cloudcommercepro.com'
    login_url = domain

    @classmethod
    def get_session(cls, username, password):
        """Create logged in session with Cloud Commerce."""
        cls.session = requests.Session()
        login_post_data = {
            'usernameInput': username, 'passwordInput': password}
        cls.session.post(cls.login_url, data=login_post_data)

    @classmethod
    def api_request(cls, request):
        """Perform API request."""
        url = urljoin(cls.domain, request.uri)
        response = cls.session.post(
            url, headers=request.headers, params=request.params,
            data=request.data)
        return response
