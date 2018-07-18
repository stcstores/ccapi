"""
customer request.

Handle customers.
"""

from ccapi.requests import APIRequest


class Customer(APIRequest):
    """Customer request."""

    uri = 'Handlers/Customer.ashx'

    def __new__(self, program_type, **kwargs):
        """Create addCustomer request."""
        self.program_type = program_type
        self.kwargs = kwargs
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {'ProgType': self.program_type}
        data.update(self.kwargs)
        return data

    def process_response(self, response):
        """Handle request response."""
        return response
