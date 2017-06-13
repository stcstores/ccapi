"""This module contains the Location class."""


class Location:
    """Contains data and methods for working with Product Locations."""

    def __init__(self, data):
        """
        Create Location object.

        Args:
            data: Cloud Commerce location JSON object.
        """
        self.id = data['ID']
        self.warehouse_id = data['WarehouseID']
        self.name = data['Name']
        self.bay_number = data['BayNumber']
        self.aisle = data['Aisle']
        self.shelf = data['Shelf']
        self.available_stock = data['AvailableStock']
        self.warehouse_bay_type = data['WarehouseBayType']
        self.warehouse_bay_type_enum = data['WarehouseBayTypeEnum']
        self.status_id = data['StatusId']
        self.status_id_enum = data['StatusIdEnum']

    def __repr__(self):
        return self.name
