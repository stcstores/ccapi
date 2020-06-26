"""
FindWarehouseBay request.

Creates a new product range.
"""
from bs4 import BeautifulSoup

from ccapi.cc_objects import WarehouseBay

from ..apirequest import APIRequest


class FindWarehouseBay(APIRequest):
    """FindWarehouseBay request."""

    uri = "Handlers/WarehouseBay/FindWarehouseBay.ashx"

    def __new__(
        self,
        prog_type=None,
        operation=None,
        warehouse_id=None,
        product_id=None,
        warehouse_bay_id=None,
        skip_records=0,
        take_limit=100,
    ):
        """Create FindWarehouseBay request."""
        self.prog_type = prog_type
        self.operation = operation
        self.warehouse_id = warehouse_id
        self.product_id = product_id
        self.warehouse_bay_id = warehouse_bay_id
        self.skip_records = skip_records
        self.take_limit = take_limit
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        if self.prog_type == "normal":
            return [WarehouseBay(bay) for bay in response.json()]
        elif self.operation == "productbays":
            return [WarehouseBay(bay) for bay in response.json()["Data"]]
        else:
            return response

    def get_data(self):
        """Get data for request."""
        data = {}
        if self.prog_type is not None:
            data["ProgType"] = self.prog_type
        if self.prog_type == "normal":
            data["TakeLimit"] = self.take_limit
            data["SkipRecords"] = self.skip_records
        if self.operation is not None:
            data["operation"] = self.operation
        if self.warehouse_id is not None:
            data["WarehouseId"] = self.warehouse_id
        if self.product_id is not None:
            data["ProductId"] = self.product_id
        if self.warehouse_bay_id is not None:
            data["warehousebayid"] = self.warehouse_bay_id
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {}
