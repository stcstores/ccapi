"""
getProductExportUpdate request.

Retrieve information about product exports.
"""


from ..apirequest import APIRequest


class GetProductExportUpdate(APIRequest):
    """
    getProductExportUpdate request.

    Retrieve information about product exports.
    """

    uri = "Handlers/Export/getProductExportUpdate.ashx"

    def get_data(self):
        """Get data for request."""
        return {"brandID": 341}

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, "Failed to retrive product exports.")
        return response.json()
