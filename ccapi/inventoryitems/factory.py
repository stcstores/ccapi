"""Containers for Cloud Commerce factories."""

from ccapi import ccapi


class Factory:
    """Container for factories."""

    def __init__(self, data):
        """Set object attributes."""
        self.load_from_data(data)

    def load_from_data(self, data):
        """Set object attributes from API data."""
        self.id = data['ID']
        self.name = data['Name']
        self.undelivered = data['Undelivered']
        self.delivered = data['Delivered']
        self.completed = data['Completed']
        self.percent_sent = data['POSent']
        self.percent_not_sent = data['PONotSent']
        self.total = data['Total']

    def __repr__(self):
        return 'Factory: {}'.format(self.name)

    def delete(self):
        """Delete this factory."""
        return ccapi.CCAPI.delete_factory(self.id)

    def delete_product_links(self):
        """Delete all product links for this factory."""
        return ccapi.CCAPI.delete_product_factory_links(self.id)

    def update_product_link(
            self, product_id, dropship=False, supplier_sku='', price=0):
        """Update or create product link."""
        return ccapi.CCAPI.update_product_factory_link(
            product_id=product_id,
            factory_id=self.id,
            dropship=dropship,
            supplier_sku=supplier_sku,
            price=price)


class Factories:
    """Container for multiple Factory objects."""

    def __init__(self, factories):
        """Set factory list."""
        self.factories = factories
        self.names = {f.name: f for f in factories}
        self.ids = {f.id: f for f in factories}

    def __getitem__(self, key):
        return self.factories[key]

    def __iter__(self):
        for factory in self.factories:
            yield factory

    def __len__(self):
        return len(self.factories)

    def create_factory(self, name):
        """Create new factory."""
        factory = ccapi.CCAPI.create_factory(name)
        self.factories.append(factory)
        self.names[factory.name] = factory
        self.ids[factory.id] = factory


class FactoryLink:
    """Container for Factory Links."""

    def __init__(self, data):
        """Set factory link attributes from API data."""
        self.link_id = int(data['LinkID'])
        self.order_price = float(data['OrderPrice'])
        self.price_precision = float(data['PricePrecision'])
        self.product_id = int(data['ProductID'])
        self.factory_id = int(data['FactoryID'])
        self.currency_symbol = data['CurrencySymbol']
        self.factory_name = data['FactoryName']
        self.product_name = data['ProductName']
        self.manufacturer_sku = data['ManufacturerSKU']
        self.barcode_number = data['BarCodeNumber']
        self.weight = int(data['Weight'])
        self.pre_order = bool(data['PreOrder'])
        self.end_of_line = bool(data['EndOfLine'])
        self.product_range_id = int(data['ProductRangeID'])
        self.product_range_name = data['ProductRangeName']
        self.po_type = data['POType']
        self.price = float(data['Price'])
        self.supplier_sku = data['SupplierSKU']

    def __repr__(self):
        return 'Factory Link: {} - {}'.format(
            self.product_name, self.factory_name)

    def delete(self):
        """Delete this Product factory link."""
        return ccapi.CCAPI.delete_product_factory_link(self.link_id)


class FactoryLinks:
    """Container for multiple FactoryLink objects."""

    def __init__(self, factory_links):
        """Set list of factory links."""
        self.links = []
        self.factory_names = {}
        self.product_ids = {}
        self.factory_ids = {}
        for link in factory_links:
            self.add_link(link)

    def __len__(self):
        return len(self.links)

    def __getitem__(self, key):
        return self.links[key]

    def __iter__(self):
        for link in self.links:
            yield link

    def add_link(self, link):
        """Add link."""
        self.links.append(link)
        self.factory_names[link.factory_name] = link
        self.product_ids[link.product_id] = link
        self.factory_ids[link.factory_id] = link
