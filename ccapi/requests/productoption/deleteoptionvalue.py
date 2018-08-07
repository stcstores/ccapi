"""
deleteOptionValue request.

Deletes Product Option Value.
"""

from ..apirequest import APIRequest


class DeleteOptionValue(APIRequest):
    """deleteOptionValue request."""

    uri = "Handlers/ProductOption/deleteOptionValue.ashx"

    def __new__(self, value_id):
        """Create deleteOptionValue request.

        Args:
            value_id: ID of Product Option Value.
        """
        self.value_id = value_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        return response

    def get_data(self):
        """Get data for request."""
        return {"valid": self.value_id}

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "155"}
