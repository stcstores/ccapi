"""
ViewFile request.

Download a product export.
"""


from ..apirequest import APIRequest


class ViewFile(APIRequest):
    """
    ViewFile request.

    Download a product export.
    """

    uri = "Handlers/Export/ViewFile.ashx"

    NAME = "name"
    DISP = "disp"
    BRAND_ID = "brandID"
    DISP_VALUE = "attach"
    BRAND_ID_VALUE = "341"

    def __new__(self, name):
        """
        Download a product export.

        Args:
            copy_images (bool): Include images in export.

        Returns:
            requests.models.Response

        """
        self.name = name
        return super().__new__(self)

    def get_params(self):
        """Get data for request."""
        return {
            self.NAME: self.name,
            self.DISP: self.DISP_VALUE,
            self.BRAND_ID: self.BRAND_ID_VALUE,
        }

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, "Failed to download product export.")
        return response
