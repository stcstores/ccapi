"""
checkRangesOnSalesChannel request.

Get details of channels of which a Product Range is listed.
"""

from ccapi.cc_objects import SalesChannel

from ..apirequest import APIRequest


class CheckRangesOnSalesChannel(APIRequest):
    """checkRangesOnSalesChannel request."""

    uri = "Handlers/Range/checkRangesOnSalesChannel.ashx"

    def __new__(self, range_id):
        """Create checkRangesOnSalesChannel request.

        Args:
            range_id: ID of Product Range.
        """
        self.range_id = range_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {"brandid": 341, "rangeid": self.range_id}
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            (
                f"Error getting sales channels for product range with "
                'ID "{self.range_id}"'
            ),
        )
        return [SalesChannel(channel) for channel in response.json()]
