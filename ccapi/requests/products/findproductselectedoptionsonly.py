"""
FindSelectedOptionsOnly request.

Gets selected product options for given product.
"""

from ccapi.cc_objects import AppliedProductOptions, Product
from ccapi.exceptions import ProductNotFoundError

from ..apirequest import APIRequest


class FindProductSelectedOptionsOnly(APIRequest):
    """FindProductSelectedOptionsOnly request."""

    uri = "Handlers/Products/findProductSelectedOptionsOnly.ashx"

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
        return {"ProductID": self.product_id, "channelID": self.channel_id}

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Error finding product information for product ID "{}"'.format(
                self.product_id
            ),
        )
        results = response.json()
        return FindProductSelectedOptionsOnlyResult(self.product_id, results)


class FindProductSelectedOptionsOnlyResult:
    """Response from FindProductSelectedOptionsOnly."""

    def __init__(self, product_id, data):
        """Get information from response from request."""
        self.stock_level = data["StockLevel"]
        self.fba_stock_level = data["FBAStockLevel"]
        if data["product"] is None:
            raise ProductNotFoundError(product_id)
        else:
            data["product"]["StockLevel"] = data["StockLevel"]
            self.product = Product(data["product"])
            self.options = AppliedProductOptions(data["options"])
