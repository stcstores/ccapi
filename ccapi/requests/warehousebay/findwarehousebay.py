"""
FindWarehouseBay request.

Creates a new product range.
"""

from .. apirequest import APIRequest
from ccapi.inventoryitems import WarehouseBay


class FindWarehouseBay(APIRequest):
    """FindWarehouseBay request."""

    uri = 'Handlers/WarehouseBay/FindWarehouseBay.ashx'

    def __new__(
            self, prog_type=None, operation=None, warehouse_id=None,
            product_id=None, warehouse_bay_id=None):
        """Create FindWarehouseBay request."""
        self.prog_type = prog_type
        self.operation = operation
        self.warehouse_id = warehouse_id
        self.product_id = product_id
        self.warehouse_bay_id = warehouse_bay_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        if len(response.text) > 0:
            json = response.json()
            if isinstance(json, list):
                return [WarehouseBay(bay) for bay in json]
            return json

    def get_data(self):
        """Get data for request."""
        data = {'BrandID': "341"}
        if self.prog_type is not None:
            data['ProgType'] = self.prog_type
        if self.operation is not None:
            data['operation'] = self.operation
        if self.warehouse_id is not None:
            data['WarehouseId'] = self.warehouse_id
        if self.product_id is not None:
            data['ProductId'] = self.product_id
        if self.warehouse_bay_id is not None:
            data['warehousebayid'] = self.warehouse_bay_id
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '57'}
