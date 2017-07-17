"""This module contains the CloudCommerceAPISession class."""

from datetime import datetime, timedelta

import requests
from urllib.parse import urljoin


class CloudCommerceAPISession:
    """Contains session object."""

    domain = 'http://seatontradingcompany.cloudcommercepro.com'
    login_url = domain
    timeout = timedelta(hours=1)

    @classmethod
    def get_session(cls, username, password):
        """Create logged in session with Cloud Commerce."""
        cls.username = username
        cls.password = password
        cls.session = requests.Session()
        login_post_data = {
            'usernameInput': username, 'passwordInput': password}
        cls.session.post(cls.login_url, data=login_post_data)
        cls.last_login = datetime.now()

    @classmethod
    def api_request(cls, request):
        """Perform API request."""
        cls.check_login()
        url = urljoin(cls.domain, request.uri)
        response = cls.session.post(
            url, headers=request.headers, params=request.params,
            data=request.data)
        return response

    @classmethod
    def check_login(cls):
        """Get new session if current session has expired."""
        if cls.last_login + cls.timeout < datetime.now():
            cls.get_session(cls.username, cls.password)
