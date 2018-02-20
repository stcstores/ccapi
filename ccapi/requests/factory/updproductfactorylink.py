"""
UpdProductFactoryLink request.

Update Product Factory link.
"""

from ..apirequest import APIRequest


class UpdProductFactoryLink(APIRequest):
    """UpdProductFactoryLink request."""

    uri = '/Handlers/Factory/UpdProductFactoryLink.ashx'

    def __new__(
            self, product_id=None, factory_id=None, dropship=False,
            supplier_sku='', price=0):
        self.product_id = product_id
        self.factory_id = factory_id
        self.dropship = dropship
        self.supplier_sku = supplier_sku
        self.price = price
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {
            'dropship': self.dropship,
            'FactoryID': self.factory_id,
            'Price': self.price,
            'ProductID': self.product_id,
            'SupplierSKU': self.supplier_sku}

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response
