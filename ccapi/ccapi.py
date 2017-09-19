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
        return CloudCommerceAPISession.get_session(username, password)

    @staticmethod
    def credentials(username, password):
        """Set username and password."""
        CloudCommerceAPISession.credentials(username, password)

    @staticmethod
    def is_logged_in():
        """Check current session is valid."""
        return CloudCommerceAPISession.is_logged_in()

    @staticmethod
    def check_login():
        """Get new session if current session has expired."""
        CloudCommerceAPISession.check_login()

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
    def get_product(product_id):
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
    def get_shop_options_for_range(range_id):
        """
        Get Shop Options for given Product Range.

        Args:
            range_id: ID of product range.

        Returns ccapi.inventoryitems.productoptions.ShopOptions.

        """
        response = requests.GetProductData(range_id)
        return response.shop_options

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
        return new_range_id

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
            if option.option_name.lower() == option_name.lower().strip():
                return option.id
        return None

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
            if option_value.value.strip().lower() == value.strip().lower():
                return option_value.id
        if create is True:
            return cls.create_option_value(option_id, value)
        return None

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
        requests.AddRemProductOption(product_id, option_id, action='rem')

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

    @staticmethod
    def set_product_option_value(product_ids, option_id, value_id):
        """
        Create setProductOptionValue request.

        Args:
            product_ids: Tuple of products to which the value will be applied.
            option_id: ID of Product Option to set.
            value_id: ID of Product Option Value to set.
        """
        return requests.SetProductOptionValue(product_ids, option_id, value_id)

    @staticmethod
    def set_product_scope(
            product_id, weight, height, lenght, width, large_letter_compatible,
            external_id):
        """
        Create setProductScope request.

        Sets weight, height, length, width, large letter compatibilty and
        external ID.

        Args:
            product_id: ID of Product to update.
            weight: Product weight in grams.
            height: Product height in mm.
            length: Product lenght in mm.
            width: Product width in mm.
            large_letter_compatible: (bool) Item can be shipped as Large
                Letter.
            external_id: External ID of product.
        """
        return requests.SetProductScope(
            product_id, weight, height, lenght, width, large_letter_compatible,
            external_id)

    @staticmethod
    def set_product_base_price(product_id, price):
        """
        Set base price for product.

        Args:
            product_id: ID of Product to update.
            price: New base price for Product.
        """
        requests.UpdateProductBasePrice(product_id, price)

    @staticmethod
    def set_product_handling_time(
            product_id, handling_time, update_channels=True):
        """
        Set handling time for product.

        Args:
            product_id: ID of Product to update.
            handling_time: New handling time.

        Kwargs:
            update_channels: If True will update handling time on channels.
                Default: True.
        """
        requests.SaveHandlingTime(product_id, handling_time, update_channels)

    @staticmethod
    def get_warehouses():
        """Return Warehouses object containing all Warehouses."""
        return requests.FindWarehouse()

    @staticmethod
    def get_bays_for_warehouse(warehouse_id):
        """Return list of Warehouse Bays for Warehouse."""
        return requests.FindWarehouseBay(
            warehouse_id=warehouse_id, prog_type='normal')

    @staticmethod
    def get_bays_for_product(product_id):
        """Return list of Warehouse Bays for Product."""
        return requests.FindWarehouseBay(
            product_id=product_id, operation='productbays')

    @staticmethod
    def add_warehouse_bay_to_product(product_id, bay_id):
        """Add Warehouse Bay to Product."""
        return requests.FindWarehouseBay(
            product_id=product_id, warehouse_bay_id=bay_id,
            operation='addlocation')

    @staticmethod
    def remove_warehouse_bay_from_product(product_id, bay_id):
        """Remove Warehouse Bay from Product."""
        return requests.FindWarehouseBay(
            product_id=product_id, warehouse_bay_id=bay_id,
            operation='removelocation')

    @staticmethod
    def add_bay_to_warehouse(
            warehouse_id, bay, bay_number=0, aisle='', shelf='',
            warehouse_bay_type='Default'):
        """Add bay to warehouse."""
        return requests.SaveWarehouseBay(
            warehouse_id, bay, bay_number=bay_number, aisle=aisle, shelf=shelf,
            warehouse_bay_type=warehouse_bay_type)

    @staticmethod
    def delete_product_option_value(option_value_id):
        """Delete Product Option Value."""
        requests.DeleteOptionValue(option_value_id)

    @staticmethod
    def set_range_option_drop_down(range_id, option_id, value):
        """Set weather a Product Option is a drop down for a Product Range.

        Args:
            range_id: ID of Product Range.
            option_id: ID of Product Option.
            value: (Bool) Product Option is a drop down.
        """
        requests.SetOptionSelect(range_id, option_id, value)

    @classmethod
    def get_products(cls, *args, **kwargs):
        """
        Search for products matching criteria.

        Kwargs:
            search_text: Text to find in title or SKU.
            option_matches_id: Option Value ID to match.

        Returns: list containing ccapi.Product.

        """
        products = []
        for product_range in cls.get_ranges(*args, **kwargs):
            products += product_range.products
        return products

    @classmethod
    def get_ranges(cls, *args, **kwargs):
        """
        Search for products matching criteria.

        Kwargs:
            search_text: Text to find in title or SKU.
            option_matches_id: Option Value ID to match.

        Returns: list containing ccapi.Range.

        """
        kwargs['skip_records'] = 0
        products = []
        while True:
            data = requests.GetProducts(*args, **kwargs)
            if len(data) == 0:
                range_ids = list(set([
                    product['RangeId'] for product in products]))
                return [cls.get_range(range_id) for range_id in range_ids]
            products += data
            kwargs['skip_records'] = len(products)

    @staticmethod
    def delete_bay(bay_id):
        """Delete Warehouse Bay."""
        return requests.FindWarehouseBay(
            warehouse_bay_id=bay_id, operation='removebay')

    @classmethod
    def get_bay_id(cls, bay_name, warehouse_name, create=False):
        """Get ID for Warehouse Bay."""
        warehouses = cls.get_warehouses()
        warehouse = warehouses[warehouse_name]
        if bay_name in warehouse.bay_names:
            return warehouse[bay_name].id
        if create is True:
            bay_id = warehouse.add_bay(bay_name)
            return bay_id
        return None

    @staticmethod
    def get_print_queue():
        """Return the current contents of the Print Queue."""
        return requests.FindPrintQueue()

    @staticmethod
    def get_users(search_string=''):
        """Return system users."""
        return requests.PreEmployee(search_string=search_string)

    @staticmethod
    def delete_range(range_id):
        """Delete Product Range."""
        return requests.DeleteProductRange(range_id)

    @staticmethod
    def get_order_addresses(order_id, customer_id):
        """Get addresses for order."""
        return requests.GetOrderAddresses(order_id, customer_id)

    @staticmethod
    def get_orders_for_dispatch(*args, **kwargs):
        """Get orders for dispatch."""
        return requests.GetOrdersForDispatch(*args, **kwargs)

    @staticmethod
    def update_range_settings(
            range_id, current_name='', current_sku='',
            current_end_of_line='', current_pre_order='',
            current_group_items='', new_name='', new_sku='',
            new_end_of_line='', new_pre_order='', new_group_items='',
            channels=[]):
        """
        Update Range Settings.

        Update Name, SKU, End of Line, Pre Order and Group Items
        for Product Range.
        """
        return requests.UpdateRangeSettings(
            range_id, current_name=current_name, current_sku=current_sku,
            current_end_of_line=current_end_of_line,
            current_pre_order=current_pre_order,
            current_group_items=current_group_items, new_name=new_name,
            new_sku=new_sku, new_end_of_line=new_end_of_line,
            new_pre_order=new_pre_order, new_group_items=new_group_items,
            channels=channels)

    @staticmethod
    def update_range_on_sales_channel(*args, **kwargs):
        """Update Product Range settings on sales channel.

        Args:
            range_id: ID of Product Range.

        Kwargs:
            option_id: ID of Product Option.
            value: (Bool) Product Option is a drop down.
        """
        return requests.UpdateRangeOnSalesChannel(*args, **kwargs)

    @staticmethod
    def update_product_on_sales_channel(*args, **kwargs):
        """Update Product settings on sales channel.

        Args:
            request_type: Setting to change on channel.
            range_id: ID of Product Range to update.

        Kwargs:
            product_ids: List containing IDs of products to update.
            act: Act.
            value_1: First updated value.
            value_2: Second updated value.
            channels: List containing IDs of channels to be updated.
        """
        return requests.UpdateProductOnSalesChannel(*args, **kwargs)

    @staticmethod
    def get_sales_channels_for_range(range_id):
        """Create checkRangesOnSalesChannel request.

        Args:
            range_id: ID of Product Range.
        """
        return requests.CheckRangesOnSalesChannel(range_id)

    @staticmethod
    def set_product_description(description, product_ids):
        """Set description for Product."""
        return requests.SaveDescription(description, product_ids)

    @staticmethod
    def set_product_name(name, product_ids):
        """Set name for Product."""
        requests.SaveProductName(name, product_ids)
