"""This module contains classes for working with Warehouses."""

from ccapi import ccapi


class MetaWarehouses(type):
    """Meta class for Warehouse class."""

    def __iter__(self):
        for warehouse in self.warehouses:
            yield warehouse

    def __getitem__(self, index):
        return self.warehouse_names[index]

    @property
    def warehouses(self):
        """Return all warehouses."""
        if self._warehouses is None:
            self._warehouses = ccapi.CCAPI.get_warehouses()
        return self._warehouses

    @property
    def warehouse_names(self):
        """Return dict oranising Warehouses by name."""
        if self._warehouse_names is None:
            self._warehouse_names = {
                warehouse.name: warehouse for warehouse in self.warehouses}
        return self._warehouse_names


class Warehouses(metaclass=MetaWarehouses):
    """Class for working with groups of warehouses."""

    _warehouses = None
    _warehouse_names = None

    def __init__(self, warehouses):
        """Create Warehouses object.

        Args:
            options: list containg Warehouse objects.
        """
        self.warehouses = warehouses
        self.warehouse_names = {
            warehouse.name: warehouse for warehouse in self.warehouses}

    def __iter__(self):
        for warehouse in self.warehouses:
            yield warehouse

    def __getitem__(self, index):
        return self.warehouse_names[index]

    def __repr__(self):
        return '{} Warehouses'.format(len(self.warehouses))


class Warehouse:
    """Wrapper for Warehouses."""

    _bays = None
    _bay_names = None

    def __init__(self, data):
        """
        Create Warehouse object.

        Args:
            data: Cloud Commerce Warehouse JSON object.
        """
        self.json = data
        self.id = data['ID']
        self.name = data['Name']
        if 'ShortDescription' in data:
            self.description = data['ShortDescription']
        self.date_created = data['DateCreated']
        self.date_updated = data['DateUpdated']
        self.warehouse_type_enum = data['WarehouseTypeEnum']
        self.sales_channel_inbound_links = data['SalesChannelInboundLinks']
        self.sales_channel_outbound_links = data['SalesChannelOutboundLinks']
        self.warehouse_type = data['WarehouseType']
        self.brand_details_id = data['BrandDetailsId']
        self.status_id = data['StatusId']
        self.address_id = data['AddressId']

    def __repr__(self):
        return self.name

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.bays[index]
        return self.bay_names[index]

    def __iter__(self):
        for bay in self.bays:
            yield bay

    @property
    def bays(self):
        """Return list of Bays in this Warehouse."""
        if self._bays is None:
            self.reload_bays()
        return self._bays

    @property
    def bay_names(self):
        """Return dict organising Bays by name."""
        if self._bay_names is None:
            self._bay_names = self.load_bay_names()
        return self._bay_names

    def load_bay_names(self):
        """Return dict organising Bays by name."""
        return {bay.name: bay for bay in self.bays}

    def reload_bays(self):
        """Get Bays for this Warehouse."""
        self._bays = ccapi.CCAPI.get_bays_for_warehouse(self.id)
        self._bay_names = self.load_bay_names()

    def add_bay(
            self, bay, bay_number=0, aisle='', shelf='',
            warehouse_bay_type='Default'):
        """
        Create Warehouse Bay for this Warehouse.

        Args:
            bay: Name of new Warehouse Bay.

        Returns: (str) ID of new Warehouse Bay.

        """
        if bay in self._bay_names:
            raise Exception(
                'Warehouse Bay {} already exists in Warehouse {}'.format(
                    bay, self.name))
        ccapi.CCAPI.add_bay_to_warehouse(
            self.id, bay, bay_number=bay_number, aisle=aisle, shelf=shelf,
            warehouse_bay_type=warehouse_bay_type)

    def get_bay(self, bay, create=False):
        """
        Get ID of Warehouse Bay by name for this Warehouse.

        Args:
            bay: Warehouse Bay to find.

        Kwargs:
            create: If True the Warehouse Bay will be added to the Warehouse.
                Default: False.

        Returns: WarehouseBay.

        """
        if bay in self.bay_names:
            return self.bay_names[bay]
        if create is True:
            self.add_bay(bay)
            self.reload_bays()
            return self.bay_names[bay]
        raise Exception(
            'Warehouse Bay {}  does not exist for Warehouse {}'.format(
                bay, self.name))


class WarehouseBay:
    """Contains data and methods for working with Warehouse Bays."""

    def __init__(self, data):
        """
        Create WarehouseBay object.

        Args:
            data: Cloud Commerce Warehouse Bay JSON object.
        """
        self.json = data
        self.id = data['ID']
        self.name = data['Name']
        self.warehouse_id = data['WarehouseID']
        self.bay_number = data['BayNumber']
        self.aisle = data['Aisle']
        self.shelf = data['Shelf']
        self.available_stock = data['AvailableStock']
        self.warehouse_bay_type = data['WarehouseBayType']
        self.warehouse_bay_type_enum = data['WarehouseBayTypeEnum']
        self.status_id = data['StatusId']
        self.statud_id_enum = data['StatusIdEnum']

    def __repr__(self):
        return self.name
