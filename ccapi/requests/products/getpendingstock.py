"""updateProductBasePrice Request."""

from ..apirequest import APIRequest


class GetPendingStock(APIRequest):
    """
    GetPendingStock Request.

    Returns the number of items in currently pending orders.
    """

    uri = "Handlers/Products/GetPendingStock.ashx"

    def __new__(self, product_id):
        """
        Create GetPendingStock request.

        Args:
            product_id: ID of Product to update.
        """
        self.product_id = product_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Error getting the pending stock level for product with ID "{}".'.format(
                self.product_id
            ),
        )
        return response.json()["TotalPending"]

    def get_data(self):
        """Get data for request."""
        return {"ProductID": self.product_id}
