"""This module contains the main CCAPI class for ccapi."""


from . requests import CloudCommerceAPISession
from . import requests


class CCAPI:
    """
    Main class of the ccapi package.

    Provides methods for interacting with the Cloud Commerce Pro API.
    """

    def __init__(self, username, password):
        """
        Create Cloud Commerce Pro API session.

        Args:
            username: Login username.
            password: Login password.
        """
        self.create_session(username, password)

    @staticmethod
    def create_session(username, password):
        """
        Create Cloud Commerce Pro API session.

        Args:
            username: Login username.
            password: Login password.
        """
        CloudCommerceAPISession.get_session(username, password)

    @staticmethod
    def search_products(search_text):
        """
        Perform text search for products.

        Args:
            search_text: Search string.

        Returns: ccapi.requests.dosearch.DoSearchResult.

        """
        return requests.DoSearch(search_text)

    @staticmethod
    def get_sku(range_sku=False):
        """
        Generate new SKU.

        Kwargs:
            range_sku (bool) Default: False.

        Returns:
            if range_sku is True returns product range SKU. Otherwise returns
            product SKU.

        """
        response = requests.ProductOperations('getgeneratedsku')
        sku = response.data
        if range_sku is True:
            sku = 'RNG_{}'.format(sku)
        return sku

    @staticmethod
    def get_product_by_id(product_id):
        """
        Get details for Product by ID.

        Args:
            product_id: ID of Product.
        """
        response = requests.FindProductSelectedOptionsOnly(product_id)
        return response.product

    @staticmethod
    def get_options_for_product(product_id):
        """
        Get Product Options for given Product.

        Args:
            product_id: ID of product.

        Returns ccapi.inventoryitems.productoptions.ProductOptions.

        """
        response = requests.FindProductSelectedOptionsOnly(product_id)
        return response.options

    @staticmethod
    def get_options_for_range(range_id):
        """
        Get Product Options for given Product Range.

        Args:
            range_id: ID of product range.

        Returns ccapi.inventoryitems.productoptions.ProductOptions.

        """
        response = requests.GetProductData(range_id)
        return response.options

    @staticmethod
    def get_product_options():
        """
        Get all available Product Options.

        Returns ccapi.inventoryitems.productoptions.ProductOptions.

        """
        return requests.GetOptions()

    @staticmethod
    def get_option_values(option_id):
        """
        Get values for Product Option.

        Args:
            option_id: ID of Product Option.

        Returns ccapi.inventoryitems.productoptions.ProductOptions.

        """
        return requests.GetOptionData(option_id)

    @staticmethod
    def update_product_stock_level(
            product_id, new_stock_level, old_stock_level):
        """
        Change stock level for a Product.

        Args:
            product_id: ID of Product.
            new_stock_level: Updated stock level.
            old_stock_level: Original stock level.

        """
        requests.UpdateProductStockLevel(
            str(product_id), new_stock_level, old_stock_level)

    @classmethod
    def create_range(cls, range_name, sku=None):
        """
        Create new Product Range.

        Args:
            range_name: Name of new Range.

        Kwargs:
            sku: SKU of new range. If None a new SKU will be generated.
                Default: None.

        Returns: (str) ID of new range.

        """
        if sku is None:
            sku = cls.get_sku(range_sku=True)
        new_range_id = requests.AddNewRange(range_name, sku)
        return cls.get_range(new_range_id)

    @staticmethod
    def create_option_value(option_id, value):
        """
        Add new Product Option Value to Product Option.

        Args:
            option_id: ID of Product Option.
            value: New Product Option Value to add to Product Option.

        Returns: (str) ID of new Product Option Value.

        """
        return requests.AddOptionValue(option_id, value)

    @classmethod
    def get_product_option_id(cls, option_name):
        """
        Get ID of Product Option by name.

        Args:
            option_name: Name of Product Option.

        Returns: (str) Product Option ID or None.

        """
        options = cls.get_product_options()
        for option in options:
            if option.option_name == option_name:
                return option.id

    @classmethod
    def get_option_value_id(cls, option_id, value, create=False):
        """
        Get ID of Product Option Value by name for given Product Option.

        Args:
            option_id: ID of Product Option.
            value: Product Option Value to find.

        Kwargs:
            create: If True the Product Option Value will be added to the
                Product Option. Default: False.

        Returns: (str) ID of Product Option Value or None.

        """
        values = cls.get_option_values(option_id)
        for option_value in values:
            if option_value.value == value:
                return value.id
        if create is True:
            return cls.create_option_value(option_id, value)

    @staticmethod
    def add_option_to_product(product_id, option_id):
        """
        Add Product Option to Product Range.

        Args:
            product_id: ID of Range.
            option_id: ID of Product Option.
        """
        requests.AddRemProductOption(product_id, option_id, action='add')

    @staticmethod
    def remove_option_from_product(product_id, option_id):
        """
        Remove Product Option from Product Range.

        Args:
            product_id: ID of Range.
            option_id: ID of Product Option.
        """
        requests.AddRemProductOption(product_id, option_id, action='remove')

    @staticmethod
    def get_range(range_id):
        """
        Get a Product Range by ID.

        Args:
            range_id: ID of Range.

        Returns ccapi.inventoryitems.ProductRange.

        """
        return requests.GetProductsForRange(range_id)

    @classmethod
    def create_product(
            cls, range_id, name, barcode, sku=None, description=None,
            vat_rate_id=5):
        """
        Add new Product to a Product Range.

        Args:
            range_id: ID of Product Range.
            name: Name of new product.
            barcode: Barcode for new product.

        Kwargs:
            sku: SKU of new product. If None a new SKU will be generated.
                Default: None.
            description: Description of new product. If None name will be used.
                Default: None.
            vat_rate_id: ID of VAT rate for product. Default: 5.

        Returns: (str) ID of new Product.

        """
        if sku is None:
            sku = cls.get_sku(range_sku=False)
        if description is None:
            description = name
        response = requests.AddProduct(
            range_id, name, barcode, sku, description, vat_rate_id)
        return response.replace('Success^^', '')
