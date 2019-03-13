"""This module contains the CloudCommerceAPISession class."""

import logging
import os
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
import yaml

logger = logging.getLogger(__name__)
error_logger = logging.getLogger("ccapi_errors")


class CloudCommerceAPISession:
    """Contains session object."""

    login_handler_uri = "/Handlers/loginHandler.ashx"
    last_login = datetime.now() - timedelta(days=5)
    timeout = timedelta(hours=1)
    YAMLFILE = "cc_login.yaml"
    PROTOCOL = "http://"
    session = requests.Session()

    domain = None
    username = None
    password = None

    @classmethod
    def get_session(cls, *, domain=None, username=None, password=None):
        """Create logged in session with Cloud Commerce."""
        cls.get_credentials(domain=domain, username=username, password=password)
        if not all([cls.domain, cls.username, cls.password]):
            raise AttributeError(
                (
                    "Login credentials are missing. One or all of the "
                    "required credentials (domain, usrname, password) were "
                    "not found.\nEnusre these are provided to the login "
                    "method or are present in the cc_login.yaml file."
                )
            )
        login_post_data = {"usernameInput": cls.username, "passwordInput": cls.password}
        login_url = cls.domain_url()
        try:
            cls.session.post(login_url, data=login_post_data)
            cls.login_handler(cls.username, cls.password)
        except Exception as e:
            error_logger.error(e)
            raise e
        else:
            cls.last_login = datetime.now()
            logger.info(f"Logged in to {domain}.")
        return cls.session

    @classmethod
    def add_credentials(cls, *, domain=None, username=None, password=None):
        """Set the domain, username and password."""
        if domain is not None:
            cls.domain = domain
        if username is not None:
            cls.username = username
        if password is not None:
            cls.password = password

    @classmethod
    def get_credentials(cls, *, domain=None, username=None, password=None):
        """Load the domain, username and password for login."""
        cls.get_credentials_from_yaml(
            domain=domain, username=username, password=password
        )
        cls.add_credentials(domain=domain, username=username, password=password)

    @classmethod
    def get_credentials_from_yaml(cls, *, domain=None, username=None, password=None):
        """Load login credentials from a cc_login.yaml file."""
        yaml_config_path = cls.find_yaml()
        if yaml_config_path is not None:
            with open(yaml_config_path, "r") as yaml_file:
                config = yaml.load(yaml_file)
            try:
                cls.add_credentials(**config)
            except Exception as e:
                raise e
                raise Exception(f"Could not load config from {yaml_config_path}.")

    @classmethod
    def find_yaml(cls, directory=None):
        """Return the directory of a cc_login.yaml if it exists in the tree."""
        if directory is None:
            directory = os.getcwd()
        if os.path.exists(os.path.join(directory, cls.YAMLFILE)):
            return os.path.join(directory, cls.YAMLFILE)
        elif os.path.dirname(directory) == directory:
            return None
        else:
            return cls.find_yaml(directory=os.path.dirname(directory))

    @classmethod
    def domain_url(cls):
        """Return the domain with the protocol prefix."""
        return f"{cls.PROTOCOL}{cls.domain}"

    @classmethod
    def login_handler(cls, username, password):
        """Perform login handler request to set session parameters."""
        login_handler_url = f"{cls.domain_url()}{cls.login_handler_uri}"
        params = {"uName": username, "pWord": password}
        response = cls.session.get(login_handler_url, params=params)
        response.raise_for_status()

    @classmethod
    def api_request(cls, request):
        """Perform API request."""
        cls.check_login()
        url = urljoin(cls.domain_url(), request.uri)
        logger.info("CCAPI Request to {}.".format(request.uri))
        try:
            response = cls.session.post(
                url,
                headers=request.headers,
                params=request.params,
                data=request.data,
                files=request.files,
            )
        except Exception as e:
            logger.exception(e)
            raise e
        try:
            response.raise_for_status()
        except Exception:
            logger.error(
                (
                    f"CCAPI Failed Request to {request.uri} with headers: "
                    f"{request.headers}, params: {request.params}, data:{request.data}, "
                    f"files: {request.files}"
                )
            )
            logger.error(
                (
                    f"CCAPI Response from Request to {request.uri} returned with response "
                    f"{response.status_code}: {response.text}"
                )
            )
        else:
            logger.debug(
                (
                    f"CCAPI Response from request to {request.uri} returned with "
                    f"{response.status_code}."
                )
            )
        return response

    @classmethod
    def session_timed_out(cls):
        """Check current session is valid."""
        if cls.last_login:
            login_expires = cls.last_login + cls.timeout
            logger.debug(
                f"Last Login: {cls.last_login} Timeout: {cls.timeout} Expires: {login_expires} Current: {datetime.now()}"
            )
            if datetime.now() < login_expires:
                return False
        return True

    @classmethod
    def check_login(cls):
        """Get new session if current session has expired."""
        if cls.session_timed_out():
            logger.info("Timed out")
            cls.get_session(
                domain=cls.domain, username=cls.username, password=cls.password
            )
