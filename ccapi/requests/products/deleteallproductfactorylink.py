"""
deleteAllProductFactoryLink request.

Remove product factory links.
"""

from ..apirequest import APIRequest


class DeleteAllProductFactoryLink(APIRequest):
    """deleteAllProductFactoryLink request."""

    uri = '/Handlers/Products/deleteAllProductFactoryLink.ashx'

    def __new__(self, factory_id, corner_loader=True):
        self.factory_id = factory_id
        self.corner_loader = corner_loader
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'FactoryID': self.factory_id, 'cornerloader': self.corner_loader}
        return data

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response