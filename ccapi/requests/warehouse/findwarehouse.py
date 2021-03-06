"""
FindWarehouse request.

Creates a new product range.
"""

from ccapi.cc_objects import Warehouse, Warehouses

from ..apirequest import APIRequest


class FindWarehouse(APIRequest):
    """FindWarehouse request."""

    uri = "Handlers/Warehouse/FindWarehouse.ashx"

    def __new__(self, prog_type="normal"):
        """Create FindWarehouse request."""
        self.prog_type = prog_type
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        if response.json() is not None:
            return Warehouses([Warehouse(warehouse) for warehouse in response.json()])

    def get_data(self):
        """Get data for request."""
        return {"ProgType": "normal", "BrandID": "341"}

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "57"}
