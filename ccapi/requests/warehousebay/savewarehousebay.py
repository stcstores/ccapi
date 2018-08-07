"""SaveWarehouseBay request."""

from ..apirequest import APIRequest


class SaveWarehouseBay(APIRequest):
    """
    SaveWarehouseBay request.

    Creates a new Warehouse Bay in a Warehouse.
    """

    uri = "Handlers/WarehouseBay/SaveWarehouseBay.ashx"

    def __new__(
        self,
        warehouse_id,
        name,
        aisle="",
        bay_number=0,
        shelf="",
        warehouse_bay_type="Default",
        status_id=1,
        bay_id=0,
        add_object=True,
    ):
        """
        Create FindWarehouseBay request.

        Args:
            warehouse_id: ID of Warehouse Bay will be added to.
            name: Name of new Warehouse Bay.
        """
        self.warehouse_id = warehouse_id
        self.name = name
        self.aisle = aisle
        self.bay_number = bay_number
        self.shelf = shelf
        self.warehouse_bay_type = warehouse_bay_type
        self.status_id = status_id
        self.bay_id = bay_id
        self.add_object = add_object
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            "WarehouseID": self.warehouse_id,
            "Name": self.name,
            "Aisle": self.aisle,
            "BayNumber": self.bay_number,
            "Shelf": self.shelf,
            "WarehouseBayType": self.warehouse_bay_type,
            "StatusId": self.status_id,
            "id": self.bay_id,
            "addObject": self.add_object,
        }

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "57"}
