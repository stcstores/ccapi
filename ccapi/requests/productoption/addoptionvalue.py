"""AddOptionValue Request."""


from .. ccapisession import APIRequest


class AddOptionValue(APIRequest):
    """Wrapper for AddOptionValueRequest."""

    uri = 'Handlers/ProductOption/addOptionValue.ashx'

    def __new__(self, option_id, value):
        """
        Create AddOptionValue request.

        Args:
            option_id: ID of product option
            value: Value to add to product option
        """
        self.option_id = option_id
        self.value = value
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            'optid': self.option_id,
            'val': self.value,
            'brandID': '341'}
