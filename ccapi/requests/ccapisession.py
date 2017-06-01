import requests
from urllib.parse import urljoin


class CloudCommerceAPISession:
    domain = 'http://seatontradingcompany.cloudcommercepro.com'
    login_url = domain

    @classmethod
    def get_session(cls, username, password):
        cls.session = requests.Session()
        login_post_data = {
            'usernameInput': username, 'passwordInput': password}
        cls.session.post(cls.login_url, data=login_post_data)

    @classmethod
    def api_request(cls, request):
        url = urljoin(cls.domain, request.uri)
        response = cls.session.post(
            url, headers=request.headers, params=request.params,
            data=request.data)
        return response


class APIRequest:
    uri = None

    def __new__(self):
        self.headers = self.get_headers(self)
        self.data = self.get_data(self)
        self.params = self.get_params(self)
        response = CloudCommerceAPISession.api_request(self)
        return self.process_response(self, response)

    def get_data(self):
        return {}

    def get_params(self):
        return {}

    def get_headers(self):
        return {}

    def process_response(self, response):
        return response.json()
