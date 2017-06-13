"""saveHandlingTime Request."""


from .. apirequest import APIRequest


class SaveHandlingTime(APIRequest):
    """
    saveHandlingTime Request.

    Sets Handling Time for Product.
    """

    uri = 'Handlers/Products/saveHandlingTime.ashx'

    def __new__(self, product_id, handling_time, update_channels):
        """
        Create saveHandlingTime request.

        Args:
            product_id: ID of Product to update.
            handling_time: New handling time.
            update_channels: If True will update handling time on channels.
        """
        self.product_id = product_id
        self.handling_time = handling_time
        self.update_channels = update_channels
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            'ProductID': self.product_id,
            'handlingTime': self.handling_time,
            'updateChannels': self.update_channels}

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '886'}
