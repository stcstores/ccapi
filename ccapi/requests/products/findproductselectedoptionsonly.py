"""
FindSelectedOptionsOnly request.

Gets selected product options for given product.
"""

from .. apirequest import APIRequest
from ccapi.inventoryitems import Product, ProductOptions, ProductOption


class FindProductSelectedOptionsOnly(APIRequest):
    """FindProductSelectedOptionsOnly request."""

    uri = 'Handlers/Products/findProductSelectedOptionsOnly.ashx'

    def __new__(self, product_id, channel_id=0):
        """
        Create FindProductSelectedOptionsOnly request.

        Args:
            product_id: ID of product
        """
        self.product_id = product_id
        self.channel_id = channel_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {'ProductID': self.product_id, 'channelID': self.channel_id}

    def process_response(self, response):
        """Handle request response."""
        results = response.json()
        return FindProductSelectedOptionsOnlyResult(results)


class FindProductSelectedOptionsOnlyResult:
    """Response from FindProductSelectedOptionsOnly."""

    def __init__(self, data):
        """Get information from response from request."""
        self.stock_level = data['StockLevel']
        self.fba_stock_level = data['FBAStockLevel']
        if data['product'] is not None:
            self.product = Product(data['product'])
            self.product.stock_level = self.stock_level
        self.options = ProductOptions(
            [ProductOption(option) for option in data['options']])
