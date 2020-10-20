"""deleteRequest request."""


from ccapi.requests import APIRequest


class DeleteRequest(APIRequest):
    """deleteRequest request."""

    uri = "/Handlers/Export/deleteRequest.ashx"

    ROWID = "rowid"
    NAME = "name"

    def __new__(self, export_ID, export_name):
        """Delete a product export."""
        self.export_ID = export_ID
        self.export_name = export_name
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {self.ROWID: self.export_ID, self.NAME: self.export_name}
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, "Failed to get HS code options")
        return response
