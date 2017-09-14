"""ProductOperations request.

Save description for products.
"""

from .. apirequest import APIRequest


class SaveDescription(APIRequest):
    """saveDescription request."""

    uri = 'Handlers/Products/saveDescription.ashx'

    def __new__(self, description, product_ids=[], channel_id=0):
        """Create saveDescription request.

        Args:
            request_mode: requestmode header
        """
        self.description = str(description)
        self.product_ids = [str(x) for x in product_ids]
        self.channel_id = channel_id
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {
            'channelID': self.channel_id,
            'desc': self.description,
            'prodids': ','.join(self.product_ids)}
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '769'}

    def process_response(self, response):
        """Handle request response."""
        return response
