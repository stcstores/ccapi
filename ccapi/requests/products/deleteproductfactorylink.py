"""
deleteProductFactoryLink request.

Delete Factory links for Product.
"""

from ..apirequest import APIRequest


class DeleteProductFactoryLink(APIRequest):
    """deleteProductFactoryLink request."""

    uri = "Handlers/Products/deleteProductFactoryLink.ashx"

    def __new__(self, factory_link_id):
        """Make deleteProductFactoryLink request."""
        self.factory_link_id = factory_link_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {"factoryLinkIds": self.factory_link_id}

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Factory link with ID "{}" was not deleted.'.format(self.factory_link_id),
        )
        return response.text
