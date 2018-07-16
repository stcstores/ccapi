"""
GetProductsForRange request.

Gets information about a given product range.
"""

from ..cc_objects import ProductRange
from .apirequest import APIRequest


class GetProductsForRange(APIRequest):
    """GetProductsForRange request."""

    uri = 'Handlers/getProductsForRange.ashx'

    def __new__(self, product_id):
        """Create GetProductsForRange request.

        Args:
            product_id: ID of range.
        """
        self.product_id = product_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        result = super().process_response(self, response)
        return ProductRange(result)

    def get_data(self):
        """Get data for request."""
        return {'ProdRangeID': self.product_id, 'salesChannelID': "0"}

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '155'}
