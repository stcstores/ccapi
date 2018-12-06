"""
GetProductsForRange request.

Gets information about a given product range.
"""

import json

from ccapi.cc_objects import ProductRange
from ccapi.exceptions import CloudCommerceResponseError
from ccapi.requests import APIRequest


class GetProductsForRange(APIRequest):
    """GetProductsForRange request."""

    uri = "Handlers/getProductsForRange.ashx"

    PRODUCT_RANGE_ID = "ProdRangeID"
    SALES_CHANNEL_ID = "salesChannelID"
    SALES_CHANNEL_ID_VALUE = "0"

    def __new__(self, product_id):
        """Create GetProductsForRange request.

        Args:
            product_id: ID of range.
        """
        self.product_id = product_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, "Error retriveing product details: {}".format(response.text)
        )
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise CloudCommerceResponseError(
                "Recieved invalid response: {}".format(response.text)
            )
        return ProductRange(response_data)

    def get_data(self):
        """Get data for request."""
        return {
            self.PRODUCT_RANGE_ID: self.product_id,
            self.SALES_CHANNEL_ID: self.SALES_CHANNEL_ID_VALUE,
        }
