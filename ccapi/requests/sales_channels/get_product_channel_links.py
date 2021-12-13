"""
getProductChannelLinks request.

Get linked channels for a product.
"""

from ..apirequest import APIRequest


class GetProductChannelLinks(APIRequest):
    """getProductChannelLinks request."""

    uri = "/Handlers/SalesChannels/getProductChannelLinks.ashx"

    def __new__(self, product_id=None):
        """Make UpdProductFactoryLink request."""
        self.product_id = product_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {"ProductID": self.product_id, "brandid": "341"}

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response.json()
