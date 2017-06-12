"""
GetOptionData request.

Gets values for a given product option.
"""

from .. apirequest import APIRequest
from ccapi.inventoryitems import ProductOptionValue


class GetOptionData(APIRequest):
    """Wrapper for GetOptionData request."""

    uri = 'Handlers/ProductOption/getOptionData.ashx'

    def __new__(self, option_id):
        """Create GetOptionData request.

        Args:
            option_id: ID of option
        """
        self.option_id = option_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        results = response.json()
        return [ProductOptionValue(item) for item in results]

    def get_data(self):
        """Get data for request."""
        return {
            'optid': self.option_id}
