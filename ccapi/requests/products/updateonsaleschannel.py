"""updateOnSalesChannel Request."""

from ..apirequest import APIRequest


class UpdateProductOnSalesChannel(APIRequest):
    """
    updateOnSalesChannel Request.

    Update product settings on sales channel.
    """

    uri = 'Handlers/Products/updateOnSalesChannel.ashx'

    def __new__(
            self,
            *,
            request_type,
            range_id,
            product_ids=[],
            act='',
            value_1='',
            value_2='',
            channels=[]):
        """
        Create updateOnSalesChannel request.

        Args:
            request_type: Setting to change on channel.
            range_id: ID of Product Range to update.

        Kwargs:
            product_ids: List containing IDs of products to update.
            act: Act.
            value_1: First updated value.
            value_2: Second updated value.
            channels: List containing IDs of channels to be updated.
        """
        self.request_type = request_type
        self.range_id = range_id
        self.product_ids = product_ids
        self.act = act
        self.value_1 = value_1
        self.value_2 = value_2
        self.channels = channels
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, (
                'Sales Channel not updated for product'
                f'ID(s) {", ".join(self.product_ids)}'))
        return response.json()

    def get_data(self):
        """Get data for request."""
        return {
            'brandid': 341,
            'rangeid': self.range_id,
            'prodids': ','.join([str(x) for x in self.product_ids]),
            'type': self.request_type,
            'act': self.act,
            'val1': self.value_1,
            'val2': self.value_2,
            'chans': ','.join([str(x) for x in self.channels])
        }

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '917'}
