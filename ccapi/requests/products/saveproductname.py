"""
saveProductName request.

Set name of Product.
"""

from ..apirequest import APIRequest


class SaveProductName(APIRequest):
    """setOptionSelect request."""

    uri = '/Handlers/Products/saveProductName.ashx'

    def __new__(self, name, product_ids):
        """Create saveProductName request.

        Args:
            name: New name for Product.
            product_ids: IDs of Products to update.

        """
        self.name = name
        self.product_ids = product_ids
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'prodids': ','.join([str(x) for x in self.product_ids]),
            'name': self.name,
            'channelID': 0
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        return response
