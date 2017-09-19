"""This module contains the ProductRange class."""

from ccapi import ccapi
from . product import Product
from . productoptions import ProductOptions, ProductOption


class ProductRange:
    """Class containing data and methods for working with ProductRanges."""

    _options = None

    def __init__(self, result):
        """
        Create Product Range object.

        Args:
            result: Cloud Commerce Product Range JSON object.
        """
        self.json = result
        self.id = result['ID']
        self.name = result['Name']
        self.sku = result['ManufacturerSKU']
        self.products = [Product(data) for data in result['Products']]
        self.child_id = result['ChildID']
        self.brand_id = result['BrandID']
        self.brand_company_name = result['BrandCompanyName']
        self.brand_trading_name = result['BrandTradingName']
        self.neck_shape = result['NeckShape']
        self.pre_order = bool(result['PreOrder'])
        self.end_of_line = bool(result['EndOfLine'])
        self.last_stock_check = result['LastStockCheck']
        self.thumb_nail = result['ThumbNail']
        self.linked = result['Linked']
        self.grouped = bool(result['Grouped'])
        self.on_sales_channel = result['OnSalesChannel']
        self.season_id = result['SeasonID']
        self.season_name = result['SeasonName']
        self.status_id = result['StatusID']
        self.edit_url = result['EditUrl']
        self.base_url = result['BaseUrl']
        self.product_ids = result['ProductIDs']
        self.shop_id = result['ShopID']
        self.item_count = result['ItemCount']
        self.listing_errors = result['ListingErrors']
        self.listings_pending = result['ListingsPending']
        self.listed_count = result['ListedCount']
        self.multi_listings_count = result['MultiListingsCount']
        self.single_listings_count = result['SingleListingsCount']
        self.pseudo_stock_level_type = result['PseudoStockLevelType']
        self.cdiscout_listings = result['cdiscountListings']

    def __repr__(self):
        return self.name

    def get_sales_channels(self):
        """Get Sales Channels for this Product Range."""
        return ccapi.CCAPI.get_sales_channels_for_range(self.id)

    def get_sales_channel_ids(self):
        """Get IDs of Sales Channels on which this Product Range is listed."""
        return [channel.id for channel in self.get_sales_channels()]

    def add_product_option(self, option, drop_down=False):
        """
        Add Product Option to Product Range.

        Args:
            option: ProductOption object or (str) Product Option ID.

        Kwargs:
            drop_down: If True option will be set as a drop down.
            Default: False.
        """
        if isinstance(option, ProductOption):
            option_id = option.id
        else:
            option_id = ProductOptions[option].id
        ccapi.CCAPI.add_option_to_product(self.id, option_id)
        if drop_down is True:
            self.set_option_drop_down(option_id, True)
        self._options = None

    def remove_product_option(self, option):
        """
        Remove Product Option from Product Range.

        Args:
            option: ProductOption object or (str) Product Option ID.
        """
        if isinstance(option, ProductOption):
            option_id = option.id
        else:
            option_id = self.options[option].id
        ccapi.CCAPI.remove_option_from_product(self.id, option_id)
        self._options = None

    def set_option_drop_down(self, option, value, update_channels=False):
        """Set weather a Product Option is a drop down for this Product Range.

        Args:
            option: ProductOption or ID of Product Option.
            value: (Bool) Product Option is a drop down.
        """
        if isinstance(option, ProductOption):
            option_id = option.id
        else:
            option_id = option
        ccapi.CCAPI.set_range_option_drop_down(self.id, option_id, value)
        if update_channels is True:
            channel_ids = self.get_sales_channel_ids()
            ccapi.CCAPI.update_range_on_sales_channel(
                self.id, request_type='select', act='update', value=value,
                option_id=option_id, channel_ids=channel_ids)

    @property
    def options(self):
        """
        Product Options for this Product Range.

        ccapi.inventoryitems.ProductOptions object with the Product Options
        applied to this Product Range.
        """
        if self._options is None:
            self._options = ccapi.CCAPI.get_options_for_range(self.id)
        return self._options

    def add_product(
            self, name, barcode, sku=None, description=None, vat_rate_id=5):
        """
        Add new Product to this Product Range.

        Args:
            name: Name of new product.
            barcode: Barcode for new product.

        Kwargs:
            sku: SKU of new product. If None a new SKU will be generated.
                Default: None.
            description: Description of new product. If None name will be used.
                Default: None.
            vat_rate_id: ID of VAT rate for product. Default: 5.

        Returns: (ccapi.inventoryitems.Product) New Product.

        """
        product_id = ccapi.CCAPI.create_product(
            self.id, name, barcode, sku=sku, description=description,
            vat_rate_id=vat_rate_id)
        return ccapi.CCAPI.get_product(product_id)

    def delete(self):
        """Delete this Product Range."""
        ccapi.CCAPI.delete_range(self.id)

    def update_range_settings(
            self, name=None, sku=None, end_of_line=None, pre_order=None,
            grouped=None, channels=[]):
        """
        Update Range Settings.

        Update Name, SKU, End of Line, Pre Order and Group Items
        for Product Range.
        """
        if name is None:
            name = self.name
        else:
            self.name = name
        if sku is None:
            sku = self.sku
        else:
            self.sku = sku
        if end_of_line is None:
            end_of_line = self.end_of_line
        if pre_order is None:
            pre_order = self.pre_order
        if grouped is None:
            grouped = self.grouped
        ccapi.CCAPI.update_range_settings(
            self.id,
            current_name=self.name,
            current_sku=self.sku,
            current_end_of_line=self.end_of_line,
            current_pre_order=self.pre_order,
            current_group_items=self.grouped,
            new_name=name,
            new_sku=sku,
            new_end_of_line=end_of_line,
            new_pre_order=pre_order,
            new_group_items=grouped,
            channels=channels)
        self.name = name
        self.sku = sku
        self.end_of_line = end_of_line
        self.pre_order = pre_order
        self.grouped = grouped

    def set_name(self, name):
        """Set Name of Product Range."""
        self.update_range_settings(name=name)

    def set_sku(self, sku):
        """Set SKU for Product Range."""
        self.update_range_settings(sku=sku)

    def set_end_of_line(self, end_of_line):
        """Set End Of Line status for Product Range."""
        self.update_range_settings(end_of_line=end_of_line)

    def set_grouped(self, grouped):
        """Set Grouped status for Product Range."""
        self.update_range_settings(grouped=grouped)

    def set_description(self, description, update_channels=False):
        product_ids = [p.id for p in self.products]
        ccapi.CCAPI.set_product_description(description, product_ids)
        if update_channels is True:
            ccapi.CCAPI.update_product_on_sales_channel(
                'desc', self.id, product_ids=[p.id for p in self.products],
                value_1=description,
                channels=[c.id for c in self.get_sales_channels()])
