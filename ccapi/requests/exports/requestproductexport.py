"""
requestProductExport request.

Trigger a new product export.
"""


from ..apirequest import APIRequest


class RequestProductExport(APIRequest):
    """
    requestProductExport request.

    Trigger a new product export.
    """

    uri = "Handlers/Export/requestProductExport.ashx"

    COPY = "copy"

    def __new__(self, copy_images=False):
        """Trigger a new product export.

        Args:
            copy_images (bool): Include images in export.

        Returns:
            True if successfull.

        """
        self.copy_images = copy_images
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {"brandid": 341, self.COPY: int(bool(self.copy_images))}

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, "Failed to trigger product exports.")
        return response.text == "OK"
