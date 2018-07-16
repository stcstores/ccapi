"""
FindProductFactoryLinks request.

Get Factory links for Product.
"""

from ccapi.cc_objects import FactoryLink, FactoryLinks

from ..apirequest import APIRequest


class FindProductFactoryLinks(APIRequest):
    """FindProductFactoryLinks request."""

    uri = 'Handlers/Products/FindProductFactoryLinks.ashx'

    def __new__(self, product_id):
        """Make FindProductFactoryLinks request."""
        self.product_id = product_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {'ProductID': self.product_id}

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response,
            'Error finding factory links for product ID "{}"'.format(
                self.product_id))
        return FactoryLinks([FactoryLink(link) for link in response.json()])
