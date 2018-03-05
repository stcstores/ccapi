"""
FindProductFactoryLinks request.

Get Factory links for Product.
"""

from ccapi.inventoryitems import FactoryLink, FactoryLinks

from ..apirequest import APIRequest


class FindProductFactoryLinks(APIRequest):
    """FindProductFactoryLinks request."""

    uri = '/Handlers/Products/FindProductFactoryLinks.ashx'

    def __new__(self, product_id):
        self.product_id = product_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {'ProductID': self.product_id}

    def process_response(self, response):
        """Handle request response."""
        return FactoryLinks([FactoryLink(link) for link in response.json()])