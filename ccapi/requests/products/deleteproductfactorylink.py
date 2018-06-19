"""
deleteProductFactoryLink request.

Delete Factory links for Product.
"""

from ..apirequest import APIRequest


class DeleteProductFactoryLink(APIRequest):
    """deleteProductFactoryLink request."""

    uri = '/Handlers/Products/deleteProductFactoryLink.ashx'

    def __new__(self, factory_link_id):
        """Make deleteProductFactoryLink request."""
        self.factory_link_id = factory_link_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {'factoryLinkId': self.factory_link_id}

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response
