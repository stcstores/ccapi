"""saveBarcode request.

Set a product's barcode.
"""

from ..apirequest import APIRequest


class SaveBarcode(APIRequest):
    """saveBarcode request class."""

    uri = "Handlers/Products/saveBarcode.ashx"

    def __new__(self, *, barcode, product_id):
        """Create saveBarcode request.

        Args:
            barcode: Barcode to set.
            proudct_id: ID of the product for which to set the barcode.
        """
        self.barcode = barcode
        self.product_id = product_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Failed to save barcode for product with ID "{}"'.format(self.product_id),
        )
        return response.text

    def get_data(self):
        """Get data for request."""
        return {"bcode": self.barcode, "prodid": self.product_id}
