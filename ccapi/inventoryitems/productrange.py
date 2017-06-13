"""This module contains the ProductRange class."""

from ccapi import ccapi
from . product import Product
from . productoptions import ProductOption


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
        self.pre_order = result['PreOrder']
        self.end_of_line = result['EndOfLine']
        self.last_stock_check = result['LastStockCheck']
        self.thumb_nail = result['ThumbNail']
        self.linked = result['Linked']
        self.grouped = result['Grouped']
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

    def add_product_option(self, option):
        """
        Add Product Option to Product Range.

        Args:
            option: ProductOption object or (str) Product Option ID.
        """
        if isinstance(option, ProductOption):
            option_id = option.id
        else:
            option_id = option
        ccapi.CCAPI.add_option_to_product(self.id, option_id)
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
            option_id = option
        ccapi.CCAPI.remove_option_from_product(self.id, option_id)
        self._options = None

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
