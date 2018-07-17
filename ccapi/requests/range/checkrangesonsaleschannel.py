"""
checkRangesOnSalesChannel request.

Get details of channels of which a Product Range is listed.
"""

from ccapi.cc_objects import SalesChannel

from ..apirequest import APIRequest


class CheckRangesOnSalesChannel(APIRequest):
    """checkRangesOnSalesChannel request."""

    uri = 'Handlers/Range/checkRangesOnSalesChannel.ashx'

    def __new__(self, range_id):
        """Create checkRangesOnSalesChannel request.

        Args:
            range_id: ID of Product Range.
        """
        self.range_id = range_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'brandid': 341,
            'rangeid': self.range_id,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        return [SalesChannel(channel) for channel in response.json()]
        self.loyalty_value_per_point = data.get('LoyaltyValuePerPoint', None)
        self.disabled = data.get('disabled', None)
        self.deleted = data.get('deleted', None)
        self.note = data.get('Note', None)

    def __repr__(self):
        return 'Sales Channel: {}'.format(self.name)
