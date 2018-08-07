"""
deleteProductRange request.

Deletes Product Ranges.
"""

from ..apirequest import APIRequest


class DeleteProductRange(APIRequest):
    """deleteProductRange request."""

    uri = "Handlers/Range/deleteProductRange.ashx"

    def __new__(self, range_id):
        """Create deleteProductRange request.

        Args:
            range_id: ID of range.
        """
        self.range_id = range_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            "ProgType": "DeleteProductRange",
            "BrandID": 341,
            "ProdRangeID": self.range_id,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, f'Product Range with ID "{self.range_id}" was not deleted.'
        )
