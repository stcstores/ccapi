"""This module contains the CloudCommerceAPISession class."""

import logging
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class CloudCommerceAPISession:
    """Contains session object."""

    domain = 'http://seatontradingcompany.cloudcommercepro.com'
    login_url = domain
    login_handler_uri = '/Handlers/loginHandler.ashx'
    last_login = datetime.now() - timedelta(days=5)
    timeout = timedelta(hours=1)
    verbose = False
    request_count = 0
    session = requests.Session()

    @classmethod
    def credentials(cls, username, password, verbose=False):
        """Set username and password."""
        cls.username = username
        cls.password = password
        cls.request_count = 0
        cls.verbose = verbose

    @classmethod
    def get_session(cls, username=None, password=None):
        """Create logged in session with Cloud Commerce."""
        if username is not None:
            cls.username = username
        if password is not None:
            cls.password = password
        login_post_data = {
            'usernameInput': username,
            'passwordInput': password
        }
        cls.session.post(cls.login_url, data=login_post_data)
        cls.login_handler(username, password)
        cls.last_login = datetime.now()
        logger.info('Logged in to Cloud Commerce.')
        return cls.session

    @classmethod
    def login_handler(cls, username, password):
        """Perform login handler request to set session parameters."""
        login_handler_url = cls.domain + cls.login_handler_uri
        params = {'uName': username, 'pWord': password}
        response = cls.session.get(login_handler_url, params=params)
        response.raise_for_status()

    @classmethod
    def api_request(cls, request):
        """Perform API request."""
        cls.check_login()
        url = urljoin(cls.domain, request.uri)
        cls.request_count += 1
        logger.info('Request to {}.'.format(request.uri))
        logger.debug(
            'Request to {} with headers: {}, params: {}, data:{}, files: {}'.
            format(
                request.uri, request.headers, request.params, request.data,
                request.files))
        try:
            response = cls.session.post(
                url,
                headers=request.headers,
                params=request.params,
                data=request.data,
                files=request.files)
        except Exception as e:
            logging.error(e)
        logger.debug(
            'Response from {} with text: {}'.format(
                request.uri, response.text))
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
