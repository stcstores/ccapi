"""ProductBarcodeInUse request.

Check if a barcode is in use
"""

from ..apirequest import APIRequest


class ProductBarcodeInUse(APIRequest):
    """saveBarcode request class."""

    uri = "Handlers/ProductBarcode/ProductBarcodeInUse.ashx"

    def __new__(self, barcode):
        """Create saveBarcode request.

        Args:
            barcode: Barcode to set.
        """
        self.barcode = barcode
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        return response.json()["Success"]

    def get_data(self):
        """Get data for request."""
        return {"BarcodeNumber": self.barcode}
