"""AddProduct request.

Creates a new product within a given range.
"""

from .. apirequest import APIRequest


class AddProduct(APIRequest):
    """AddProduct request class."""

    uri = 'Handlers/Products/AddProduct.ashx'

    def __new__(
            self, range_id, name, barcode, sku, description, vat_rate_id):
        """Create AddProduct request.

        Args:
            range_id: ID of range to which to add the product
            name: Name of new product
            barcode: Barcode for new product
            sku: SKU of new product
            description: Description of new product
            vat_rate_id: ID of VAT rate for new product
        """
        self.range_id = range_id
        self.name = name
        self.barcode = barcode
        self.sku = sku
        self.description = description
        self.vat_rate_id = vat_rate_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            'ProductID': "0",
            'ProdRangeID': self.range_id,
            'ProdName': self.name,
            'BarCode': self.barcode,
            'SKUCode': self.sku,
            'ProdDescription': self.description,
            'VatRateID': self.vat_rate_id,
            'CopyDesc': "0",
            'BrandID': "341"}

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '1496918496099'}
