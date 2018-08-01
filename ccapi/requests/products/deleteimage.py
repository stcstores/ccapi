"""
deleteImage request.

Delete Product Image.
"""

from ..apirequest import APIRequest


class DeleteImage(APIRequest):
    """deleteImage request."""

    uri = "Handlers/Products/deleteImage.ashx"

    def __new__(self, image_id):
        """Create deleteImage request.

        Args:
            image_id: ID of image to be deleted.
        """
        self.image_id = int(image_id)
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, f"Image with ID {self.image_id} was not saved."
        )
        return response.text

    def get_data(self):
        """Get data for request."""
        return {"imgID": self.image_id}

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "155"}
