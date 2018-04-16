"""This module contains classes for working with Warehouses."""


from ccapi import ccapi


class Warehouses():
    """Class for working with groups of warehouses."""

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

    def get_bay(self, warehouse_name, bay_name, create=False):
        """Get Warehouse Bay by warehouse name and bay name."""
        return self.warehouse_names[warehouse_name].get_bay(
            bay_name, create=create)

    def items(self):
        return self.warehouse_names.items()


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
        for bay in self._bays:
            bay.warehouse = self
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
        if bay in self.bay_names:
            raise Exception(
                'Warehouse Bay {} already exists in Warehouse {}'.format(
                    bay, self.name))
        ccapi.CCAPI.add_bay_to_warehouse(
            self.id, bay, bay_number=bay_number, aisle=aisle, shelf=shelf,
            warehouse_bay_type=warehouse_bay_type)
        self.reload_bays()
        return self.bay_names[bay].id

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
        self.load_json(data)

    def load_json(self, data):
        """Load data from dict."""
        self.json = data
        self.id = data.get('ID', None)
        self.name = data.get('Name', None)
        self.warehouse_id = data.get('WarehouseID', None)
        self.bay_number = data.get('BayNumber', None)
        self.aisle = data.get('Aisle', None)
        self.shelf = data.get('Shelf', None)
        self.available_stock = data.get('AvailableStock', None)
        self.warehouse_bay_type = data.get('WarehouseBayType', None)
        self.warehouse_bay_type_enum = data.get('WarehouseBayTypeEnum', None)
        self.status_id = data.get('StatusId', None)
        self.statud_id_enum = data.get('StatusIdEnum', None)
        if 'Products' in data and data['Products'] is not None:
            self.too_many_products = False
            self.products = []
            products = data['Products']
            if len(products) > 0:
                if products[0]['ManufacturerSKU'] == 'Warning':
                    self.too_many_products = True
                else:
                    self.products = [
                        BayProduct(d) for d in products
                        if d['ManufacturerSKU'] != 'Warning']

    def __repr__(self):
        return self.name

    def delete(self):
        ccapi.CCAPI.delete_bay(self.id)

    @property
    def empty(self):
        return self.too_many_products is False and len(self.products) == 0


class BayProduct:

    def __init__(self, data):
        self.load_json(data)

    def load_json(self, data):
        self.json = data
        self.image_url = data['ProductImage']
        self.id = data['ID']
        self.end_of_line = bool(data['EndOfLine'])
        self.sku = data['ManufacturerSKU']
        self.name = data['Name']

    def __repr__(self):
        return '{} - {}'.format(self.sku, self.name)
