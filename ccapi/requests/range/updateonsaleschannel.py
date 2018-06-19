"""
updateOnSalesChannel request.

Update Product Range settings on sales channel.
"""

from ..apirequest import APIRequest


class UpdateRangeOnSalesChannel(APIRequest):
    """setOptionSelect request."""

    uri = '/Handlers/Range/updateOnSalesChannel.ashx'

    def __new__(
            self,
            range_id,
            request_type='select',
            act='update',
            value=None,
            option_id=None,
            channel_ids=[]):
        """Create updateOnSalesChannel request.

        Args:
            range_id: ID of Product Range.

        Kwargs:
            option_id: ID of Product Option.
            value: (Bool) Product Option is a drop down.
        """
        self.range_id = range_id
        self.request_type = request_type
        self.act = act
        if isinstance(value, bool):
            self.value = str(int(value))
        else:
            self.value = str(value)
        self.option_id = option_id
        self.channel_ids = channel_ids
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'brandid': 341,
            'rangeid': self.range_id,
            'type': self.request_type,
            'act': self.act,
            'val': self.value,
            'optid': self.option_id,
            'chans': ','.join(
                (str(channel_id) for channel_id in self.channel_ids))
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        pass
