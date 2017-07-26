"""This module contains the CloudCommerceAPISession class."""

from datetime import datetime, timedelta

import requests
from urllib.parse import urljoin


class CloudCommerceAPISession:
    """Contains session object."""

    domain = 'http://seatontradingcompany.cloudcommercepro.com'
    login_url = domain
    last_login = datetime.now() - timedelta(days=5)
    timeout = timedelta(hours=1)

    @classmethod
    def credentials(cls, username, password):
        """Set username and password."""
        cls.username = username
        cls.password = password

    @classmethod
    def get_session(cls, username=None, password=None):
        """Create logged in session with Cloud Commerce."""
        if username is not None:
            cls.username = username
        if password is not None:
            cls.password = password
        cls.session = requests.Session()
        login_post_data = {
            'usernameInput': username, 'passwordInput': password}
        print('Getting Cloud Commerce Session')
        cls.session.post(cls.login_url, data=login_post_data)
        cls.last_login = datetime.now()
        return cls.session

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
    def is_logged_in(cls):
        """Check current session is valid."""
        if cls.last_login and cls.last_login + cls.timeout > datetime.now():
            return True
        return False

    @classmethod
    def check_login(cls):
        """Get new session if current session has expired."""
        if not cls.is_logged_in():
            cls.get_session(cls.username, cls.password)
