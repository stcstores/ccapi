"""
PreEmployee request.

Get list of users.
"""

from . apirequest import APIRequest

from bs4 import BeautifulSoup


class PreEmployee(APIRequest):
    """GetProductsForRange request."""

    uri = '/Handlers/PreEmployee.ashx'

    def __new__(self, search_string=''):
        """Create FindPrintQueue request."""
        self.search_string = search_string
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'ProgType': 'Search',
            'Lname': self.search_string}
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '57'}

    def process_response(self, response):
        """Handle request response."""
        return Users(response.text)


class Users:
    """Wrapper for Cloud Commerce Users."""

    def __init__(self, html):
        """Create Users from HTML."""
        self.html = html
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.divs = self.soup.find_all("div", class_="ListItem")
        self.users = [User(div) for div in self.divs]

    def __iter__(self):
        for user in self.users:
            yield user

    def __getitem__(self, index):
        for user in self.users:
            if index in (user.username, user.id, user.full_name):
                return user
        raise IndexError('User not found {}'.format(index))


class User:
    """Container for Cloud Commerce Users."""

    def __init__(self, html):
        """Get User information from HTML."""
        self.soup = html
        self.html = str(html)
        labels = self.soup.find_all('label')
        self.values = [label.text for label in labels]
        self.id = self.values[0]
        self.username = self.values[1]
        self.first_name = self.values[2]
        self.second_name = self.values[3]
        self.role = self.values[4]
        self.status = self.values[5] == 'Enabled'

    @property
    def full_name(self):
        """Return User's full name."""
        return ' '.join([self.first_name, self.second_name])

    def __repr__(self):
        return self.full_name
