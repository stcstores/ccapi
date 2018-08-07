"""UpdateProductStockLevel request.

Changes stock level for given product to a given quantity.
"""

from ..apirequest import APIRequest


class UpdateProductStockLevel(APIRequest):
    """UpdateProductStockLevel request."""

    uri = "Handlers/Products/UpdateProductStockLevel.ashx"

    def __new__(self, *, product_id, new_stock_level, old_stock_level):
        """
        Create UpdateProductStockLevel request.

        Args:
            product_id: ID of product
            new_stock_level: Stock level after update
            old_stock_level: Stock level before update
        """
        self.product_id = product_id
        self.new_stock_level = new_stock_level
        self.old_stock_level = old_stock_level
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {
            "AccountID": "4419651",
            "ProductID": self.product_id,
            "newStockLevel": self.new_stock_level,
            "oldStockLevel": self.old_stock_level,
        }

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Error updating stock level for prouduct with ID "{}".'.format(
                self.product_id
            ),
        )
        return response.text
