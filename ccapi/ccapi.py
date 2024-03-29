"""This module contains the main CCAPI class for ccapi."""

import datetime

from . import requests
from .cc_objects import ProductExportUpdateResponse, VatRates
from .requests import CloudCommerceAPISession


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
    def create_session(domain=None, username=None, password=None):
        """
        Create Cloud Commerce Pro API session.

        Args:
            username: Login username.
            password: Login password.

        """
        return CloudCommerceAPISession.get_session(
            domain=domain, username=username, password=password
        )

    @staticmethod
    def is_logged_in():
        """Check current session is valid."""
        return CloudCommerceAPISession.check_login()

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
        request_class = requests.products.DoSearch
        return request_class(search_text, search_type=request_class.RANGE)

    @staticmethod
    def search_product_name(search_text, channel_id=None):
        """
        Perform text search for products based on product name.

        Args:
            search_text: Search string.
            channel_id: The ID of the sales channel on which to search.

        Returns: ccapi.requests.dosearch.DoSearchResult.

        """
        request_class = requests.products.DoSearch
        return request_class(
            search_text, channel_id=channel_id, search_type=request_class.PRODUCT_NAME
        )

    @staticmethod
    def search_product_SKU(search_text, channel_id=None):
        """
        Perform text search for products based on product SKU.

        Args:
            search_text: Search string.
            channel_id: The ID of the sales channel on which to search.

        Returns: ccapi.requests.dosearch.DoSearchResult.

        """
        request_class = requests.products.DoSearch
        return request_class(
            search_text, channel_id=channel_id, search_type=request_class.SKU
        )

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
        response = requests.products.ProductOperations("getgeneratedsku")
        sku = response.data
        if range_sku is True:
            sku = "RNG_{}".format(sku)
        return sku

    @staticmethod
    def get_product(product_id):
        """
        Get details for Product by ID.

        Args:
            product_id: ID of Product.

        """
        response = requests.products.FindProductSelectedOptionsOnly(product_id)
        return response.product

    @staticmethod
    def get_options_for_product(product_id):
        """
        Get Product Options for given Product.

        Args:
            product_id: ID of product.

        Returns ccapi.cc_objects.productoptions.ProductOptions.

        """
        response = requests.products.FindProductSelectedOptionsOnly(product_id)
        return response.options

    @staticmethod
    def get_product_range_options(range_id):
        """Get product options and shop options for Product Range."""
        response = requests.productoption.GetProductData(range_id)
        return response

    @staticmethod
    def get_options_for_range(range_id):
        """
        Get Product Options for given Product Range.

        Args:
            range_id: ID of product range.

        Returns ccapi.cc_objects.productoptions.ProductOptions.

        """
        response = requests.productoption.GetProductData(range_id)
        return response.options

    @staticmethod
    def get_shop_options_for_range(range_id):
        """
        Get Shop Options for given Product Range.

        Args:
            range_id: ID of product range.

        Returns ccapi.cc_objects.productoptions.ShopOptions.

        """
        response = requests.productoption.GetProductData(range_id)
        return response.shop_options

    @staticmethod
    def get_product_options():
        """
        Get all available Product Options.

        Returns ccapi.cc_objects.productoptions.ProductOptions.

        """
        return requests.productoption.GetOptions()

    @staticmethod
    def get_option_values(option_id):
        """
        Get values for Product Option.

        Args:
            option_id: ID of Product Option.

        Returns ccapi.cc_objects.productoptions.ProductOptions.

        """
        return requests.productoption.GetOptionData(option_id)

    @staticmethod
    def update_product_stock_level(*, product_id, new_stock_level, old_stock_level):
        """
        Change stock level for a Product.

        Args:
            product_id: ID of Product.
            new_stock_level: Updated stock level.
            old_stock_level: Original stock level.

        """
        requests.products.UpdateProductStockLevel(
            product_id=product_id,
            new_stock_level=new_stock_level,
            old_stock_level=old_stock_level,
        )

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
        new_range_id = requests.range.AddNewRange(range_name=range_name, sku=sku)
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
        return requests.productoption.AddOptionValue(option_id, value)

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
    def add_option_to_product(*, range_id, option_id):
        """
        Add Product Option to Product Range.

        Args:
            product_id: ID of Range.
            option_id: ID of Product Option.

        """
        requests.range.AddRemProductOption(
            range_id=range_id, option_id=option_id, add=True
        )

    @staticmethod
    def remove_option_from_product(*, range_id, option_id):
        """
        Remove Product Option from Product Range.

        Args:
            range_id: ID of Range.
            option_id: ID of Product Option.

        """
        requests.range.AddRemProductOption(
            range_id=range_id, option_id=option_id, remove=True
        )

    @staticmethod
    def get_range(range_id):
        """
        Get a Product Range by ID.

        Args:
            range_id: ID of Range.

        Returns ccapi.cc_objects.ProductRange.

        """
        return requests.handlers.GetProductsForRange(range_id)

    @classmethod
    def create_product(
        cls,
        *,
        range_id,
        name,
        barcode,
        sku=None,
        description=None,
        vat_rate=20,
        vat_rate_id=None,
    ):
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
            vat_rate: VAT percentage. This will be ignored if vat_rate_id is not None.
                Default: 20.
            vat_rate_id: The Cloud Commerce ID of the product's VAT rate. If None, the
                vat_rate kwarg will be used instead. Default: None.

        Returns: (str) ID of new Product.

        """
        if sku is None:
            sku = cls.get_sku(range_sku=False)
        if description is None:
            description = name
        if vat_rate_id is None:
            vat_rate_id = VatRates.get_vat_rate_id_by_rate(vat_rate)
        return requests.products.AddProduct(
            range_id=range_id,
            name=name,
            barcode=barcode,
            sku=sku,
            description=description,
            vat_rate_id=vat_rate_id,
        )

    @staticmethod
    def set_product_option_value(*, product_ids, option_id, option_value_id):
        """
        Create setProductOptionValue request.

        Args:
            product_ids: Tuple of products to which the value will be applied.
            option_id: ID of Product Option to set.
            option_value_id: ID of Product Option Value to set.

        """
        return requests.products.SetProductOptionValue(
            product_ids=product_ids,
            option_id=option_id,
            option_value_id=option_value_id,
        )

    @staticmethod
    def set_product_scope(
        *,
        product_id,
        weight,
        height,
        length,
        width,
        large_letter_compatible,
        external_id=None,
    ):
        """
        Set the scope of a product.

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
        return requests.products.SetProductScope(
            product_id=product_id,
            weight=weight,
            height=height,
            length=length,
            width=width,
            large_letter_compatible=large_letter_compatible,
            external_id=external_id,
        )

    @staticmethod
    def set_product_base_price(*, product_id, price):
        """
        Set base price for product.

        Args:
            product_id: ID of Product to update.
            price: New base price for Product.

        """
        requests.products.UpdateProductBasePrice(product_id=product_id, price=price)

    @staticmethod
    def set_product_handling_time(*, product_id, handling_time, update_channels=True):
        """
        Set handling time for product.

        Args:
            product_id: ID of Product to update.
            handling_time: New handling time.

        Kwargs:
            update_channels: If True will update handling time on channels.
                Default: True.

        """
        requests.products.SaveHandlingTime(
            product_id=product_id,
            handling_time=handling_time,
            update_channels=update_channels,
        )

    @staticmethod
    def get_warehouses():
        """Return Warehouses object containing all Warehouses."""
        return requests.warehouse.FindWarehouse()

    @staticmethod
    def get_bays_for_warehouse(warehouse_id):
        """Return list of Warehouse Bays for Warehouse."""
        skip_records = 0
        bays = []
        ids = []
        take_limit = 100
        skip_records = 0
        request = 1
        while True:
            data = requests.warehousebay.FindWarehouseBay(
                warehouse_id=warehouse_id,
                prog_type="normal",
                skip_records=skip_records,
                take_limit=take_limit,
            )
            if len(data) == 0:
                return bays
            for bay in data:
                if bay.id not in ids:
                    ids.append(bay.id)
                    bays.append(bay)
            request += 1
            skip_records += take_limit

    @staticmethod
    def get_bays_for_product(product_id):
        """Return list of Warehouse Bays for Product."""
        return requests.warehousebay.FindWarehouseBay(
            product_id=product_id, operation="productbays"
        )

    @staticmethod
    def add_warehouse_bay_to_product(product_id, bay_id):
        """Add Warehouse Bay to Product."""
        return requests.warehousebay.FindWarehouseBay(
            product_id=product_id, warehouse_bay_id=bay_id, operation="addlocation"
        )

    @staticmethod
    def remove_warehouse_bay_from_product(product_id, bay_id):
        """Remove Warehouse Bay from Product."""
        return requests.warehousebay.FindWarehouseBay(
            product_id=product_id, warehouse_bay_id=bay_id, operation="removelocation"
        )

    @classmethod
    def add_bay_to_warehouse(
        cls,
        warehouse_id,
        bay_name,
        bay_number=0,
        aisle="",
        shelf="",
        warehouse_bay_type="Default",
    ):
        """Add bay to warehouse."""
        requests.warehousebay.SaveWarehouseBay(
            warehouse_id,
            bay_name,
            bay_number=bay_number,
            aisle=aisle,
            shelf=shelf,
            warehouse_bay_type=warehouse_bay_type,
        )
        bays = cls.get_bays_for_warehouse(warehouse_id)
        for bay in bays:
            if bay.name == bay_name:
                return bay.id

    @staticmethod
    def delete_product_option_value(option_value_id):
        """Delete Product Option Value."""
        requests.productoption.DeleteOptionValue(option_value_id)

    @staticmethod
    def set_range_option_drop_down(*, range_id, option_id, drop_down):
        """Set weather a Product Option is a drop down for a Product Range.

        Args:
            range_id: ID of Product Range.
            option_id: ID of Product Option.
            drop_down: (Bool) Set Product Option as a drop down or not.

        """
        requests.range.SetOptionSelect(
            range_id=range_id, option_id=option_id, drop_down=drop_down
        )

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
        kwargs["skip_records"] = 0
        range_ids = []
        while True:
            response = requests.productmanager.GetProducts(*args, **kwargs)
            for product in response:
                range_id = product["RangeId"]
                if range_id not in range_ids:
                    range_ids.append(range_id)
            if len(response) > 0:
                kwargs["skip_records"] += len(response)
                continue
            return [cls.get_range(range_id) for range_id in range_ids]

    @staticmethod
    def delete_bay(bay_id):
        """Delete Warehouse Bay."""
        return requests.warehousebay.FindWarehouseBay(
            warehouse_bay_id=bay_id, operation="removebay"
        )

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
        return requests.printqueue.FindPrintQueue()

    @staticmethod
    def get_users(search_string=""):
        """Return system users."""
        return requests.handlers.PreEmployee(search_string=search_string)

    @staticmethod
    def delete_range(range_id):
        """Delete Product Range."""
        return requests.range.DeleteProductRange(range_id)

    @staticmethod
    def get_order_addresses(order_id, customer_id):
        """Get addresses for order."""
        return requests.orderdetails.GetOrderAddresses(order_id, customer_id)

    @staticmethod
    def get_orders_for_dispatch(*args, **kwargs):
        """Get orders for dispatch."""
        kwargs["skip_records"] = 0
        kwargs["take_limit"] = 200
        orders = []
        while True:
            new_orders = requests.orderhandlers.GetOrdersForDispatch(*args, **kwargs)
            new_orders = [
                o for o in new_orders if o.order_id not in (o.order_id for o in orders)
            ]
            orders += new_orders
            if len(new_orders) > 0:
                kwargs["skip_records"] += kwargs["take_limit"]
            else:
                return orders

    @staticmethod
    def update_range_settings(
        range_id,
        current_name="",
        current_sku="",
        current_end_of_line="",
        current_pre_order="",
        current_group_items="",
        new_name="",
        new_sku="",
        new_end_of_line="",
        new_pre_order="",
        new_group_items="",
        channels=[],
    ):
        """
        Update Range Settings.

        Update Name, SKU, End of Line, Pre Order and Group Items
        for Product Range.
        """
        return requests.range.UpdateRangeSettings(
            range_id=range_id,
            current_name=current_name,
            current_sku=current_sku,
            current_end_of_line=current_end_of_line,
            current_pre_order=current_pre_order,
            current_group_items=current_group_items,
            new_name=new_name,
            new_sku=new_sku,
            new_end_of_line=new_end_of_line,
            new_pre_order=new_pre_order,
            new_group_items=new_group_items,
            channels=channels,
        )

    @staticmethod
    def update_range_on_sales_channel(
        *, range_id, request_type, act, value, option_id, channel_ids=[]
    ):
        """Update Product Range settings on sales channel.

        Args:
            range_id: ID of Product Range.

        Kwargs:
            option_id: ID of Product Option.
            value: (Bool) Product Option is a drop down.

        """
        return requests.range.UpdateRangeOnSalesChannel(
            range_id=range_id,
            request_type=request_type,
            act=act,
            value=value,
            option_id=option_id,
            channel_ids=channel_ids,
        )

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
        return requests.products.UpdateProductOnSalesChannel(*args, **kwargs)

    @staticmethod
    def get_sales_channels_for_range(range_id):
        """Return a list of sales channels for the given Product Range.

        Args:
            range_id: ID of Product Range.

        """
        return requests.range.CheckRangesOnSalesChannel(range_id)

    @staticmethod
    def set_product_description(*, description, product_ids):
        """Set description for Product."""
        return requests.products.SaveDescription(
            description=description, product_ids=product_ids
        )

    @staticmethod
    def set_product_name(*, name, product_ids):
        """Set name for Product."""
        requests.products.SaveProductName(name=name, product_ids=product_ids)

    @staticmethod
    def set_product_vat_rate(*, product_ids, vat_rate):
        """Set VAT rate for products."""
        vat_rate_id = VatRates.get_vat_rate_id_by_rate(vat_rate)
        return requests.products.UpdateProductVatRate(
            product_ids=product_ids, vat_rate_id=vat_rate_id
        )

    @staticmethod
    def set_product_vat_rate_by_id(*, product_ids, vat_rate_id):
        """Set VAT rate for products."""
        return requests.products.UpdateProductVatRate(
            product_ids=product_ids, vat_rate_id=vat_rate_id
        )

    @staticmethod
    def get_product_images(range_id, product_id):
        """Get images for product.

        Args:
            range_id: ID of Product Range.
            product_id: ID of Product.

        """
        return requests.handlers.GetImages(range_id=range_id, product_id=product_id)

    @staticmethod
    def delete_image(image_id):
        """Delete a product image.

        Args:
            image_id: ID of Product Image to delete.

        """
        image_id = str(image_id).replace("bimage", "")
        return requests.products.DeleteImage(image_id)

    @staticmethod
    def upload_image(*, product_ids, channel_ids=[], image_file=None):
        """Add an image to a product or products.

        Kwargs:
            product_ids: IDs of products to add image to.
            channel_ids: IDs of channels to add image to.
            image_file: File object containing the image to upload.

        """
        return requests.products.UploadImage(
            product_ids=product_ids, channel_ids=channel_ids, image_file=image_file
        )

    @staticmethod
    def set_image_order(*, product_id=None, image_ids=[]):
        """Set the order of a product's images.

        Kwargs:
            product_id: ID of Product for which Images will be ordered.
            image_order: List containing IDs of images in updated order.
        """
        image_order = [str(image_id).replace("bimage", "") for image_id in image_ids]
        return requests.products.SetImageOrder(
            product_id=product_id, image_ids=image_order
        )

    @staticmethod
    def get_courier_rules():
        """Return shipping rules."""
        return requests.configuration.ShippingRules()

    @staticmethod
    def get_dispatch_methods_for_order(order_id, analyse=True):
        """Return dispatch methods for an order."""
        return requests.orderhandlers.GetDispatchMethodsForOrder(
            order_id, analyse=analyse
        )

    @staticmethod
    def get_factories():
        """Return a list of existing Factories."""
        return requests.factory.FindFactories()

    @classmethod
    def create_factory(cls, name):
        """Create new Factory."""
        new_factory_id = requests.factory.Factory(
            name=name, factory_id=0, prog_type=requests.Factory.UPDATE_FACTORY
        )
        factories = cls.get_factories()
        return factories.ids[new_factory_id]

    @staticmethod
    def delete_product_factory_links(factory_id):
        """Remove product links from factory."""
        return requests.products.DeleteAllProductFactoryLink(factory_id)

    @staticmethod
    def delete_factory(factory_id):
        """Delete Factory."""
        return requests.factory.Factory(
            prog_type=requests.Factory.DELETE_FACTORY, factory_id=factory_id
        )

    @staticmethod
    def get_product_factory_links(product_id):
        """Get factory links for product."""
        return requests.products.FindProductFactoryLinks(product_id)

    @staticmethod
    def update_product_factory_link(
        product_id=None, factory_id=None, dropship=False, supplier_sku="", price=0
    ):
        """Create or update Product Factory Link."""
        return requests.factory.UpdProductFactoryLink(
            product_id=product_id,
            factory_id=factory_id,
            dropship=dropship,
            supplier_sku=supplier_sku,
            price=price,
        )

    @staticmethod
    def delete_product_factory_link(factory_link_id):
        """Delete Product Factory link."""
        return requests.products.DeleteProductFactoryLink(factory_link_id)

    @staticmethod
    def add_customer(*args, **kwargs):
        """
        Add a customer to Cloud Commerce.

        Kwargs:
            customer_name (Required) (str): The new customer's name.
            address_1 (Required) (str): The first line of the customer's address.
            country (Required) (str): The country of the customer's address.
            selling_channel_id (Required) (str): The ID of the selling channel used by
                the customer.
            account_name (str or None): The name of the customer's accound.
                Default: None.
            address_2 (str or None): The second line of the customer's address.
                Default: None.
            agent_id (int): The ID of the agent creating the customer.
                Use 0 to not specify an agent. Default: 0.
            company_fax (str or None): The customer's company fax number.
                Default: None.
            company_mobile (str or None): The customer's company mobile number.
                Default: None.
            company_telephone (str or None): The customer's company telephone number.
                Default: None.
            contact_email (str or None): The customer's contact email address.
                Default: None.
            contact_fax (str or None): The customer's contact fax number.
                Default: None.
            contact_name (str or None): The customer's contact name. Default: None.
            contact_phone (str or None): The customer's contact phone number.
                Default: None.
            contact_mobile (str or None): The customer's contact phone number.
                Default: None.
            county (str or None): The county or region of the customer's address.
                Default: None.
            customer_type (int): The ID of the type of the customer. Default: 8.
            eu_vat (bool): True if the customer is charged EU VAT. Default: True.
            post_code (str or None): The customer's postal or zip code. Default: None.
            payment_terms (int): ID of the payment terms for the customer. A list of
                payment term IDs can be found by calling CCAPI.get_payment_terms().
                Default: 1 (Full Payment Before Dispatch).
            town (str or None): The town in the customer's address. Default: None.
            trade_name (str or None): The customer's trading name. If None customer_name
                will be used. Default: None.
            vat_number (str or None): The customer's VAT number. Default: None.
            special_instructions (str or None): Special instructions for the customer.
                Default: None.
            credit_limit (int): The customer's credit limit. Default 0.

            Returns:
                (str) The ID of the newly created customer.

        """
        return requests.handlers.AddCustomer(*args, **kwargs)

    @staticmethod
    def get_payment_terms():
        """
        Return payment term options.

        Returns dict: {payment term name: payment term ID}
        """
        response = requests.program_type_requests.GetPaymentTerms()
        response_list = response.split("^^")[2:]
        payment_terms = {}
        while len(response_list) > 0:
            payment_term_ID = response_list.pop()
            payment_term_name = response_list.pop()
            payment_terms[payment_term_name] = payment_term_ID
        return payment_terms

    @staticmethod
    def create_order(
        *,
        customer_id,
        items,
        delivery_address_id,
        billing_address_id,
        delivery_date=None,
        season_id=None,
        channel_id=None,
        order_id=None,
        order_note=None,
        send_email=None,
        carriage_net=None,
        carriage_vat=None,
        total_net=None,
        total_vat=None,
        total_gross=None,
        discount_net=None,
        shipping_rule_id=None,
    ):
        """
        Add a customer order to Cloud Commerce.

        Kwargs:
            customer_id (int): The ID of the customer making the order.
            items (list[ccapi.requests.handlers.createorder.NewOrderItem]): List of
                NewOrderItem instances for each item ordered.
            delivery_address_id (int): ID of the address to deliver to.
            billing_address_id (int): ID of the customer's billing address for this
                order.
            delivery_date (datetime.datetime or None): The date by which the order
                should be delivered. If None is passed, the current date will be used.
                Default: None
            channel_id (int): The ID of the channel on which the order was placed.
                (Not required)
            order_note (str): Add a note to the order.
            send_email (bool): Use True to send confirmation email, otherwise
                no email will be sent.
            carriage_net (float): The net value of the carriage cost.
            carriage_vat (float): The VAT charged on carriage.
            total_net (float): The total net value of the order.
            total_vat (float): The VAT charged on the order.
            total_gross (float): The total gross value of the order.
            discount_net (float): The discount applied to the order. (Default: 0)
            shipping_rule_id (int or None): ID of the shipping rule to be used for the
                order. Use None to not specify a shipping rule. (Default: None)
        """
        kwargs = {key: value for key, value in locals().items() if value is not None}
        if "delivery_date" not in kwargs:
            kwargs["delivery_date"] = datetime.datetime.now()
        kwargs["free_of_charge"] = sum([item.total_gross for item in items]) == 0
        return requests.handlers.CreateOrder(**kwargs)

    @staticmethod
    def create_payment(
        *,
        customer_id,
        invoice_id,
        amount,
        transaction_type_id=None,
        bank_nominal_code=None,
        transaction_date=None,
        bank_account_id=None,
        proforma_id=None,
        gateway_id=None,
        currency_code_id=None,
        exchange_rate=None,
        login_id=None,
    ):
        """
        Create a payment for an order.

        Kwargs:
            customer_id (int) (required): The ID of the customer that originated the
                payment.
            invoice_id (int) (required): The ID of the invoice being paid.
            amount (float) (required): The amount paid.
            transaction_type_id (int or None): The ID of the transaction type. Default: None.
            transaction_date (datetime.datetime or None): The date of the transaction.
                If None, the current date will be used.
            bank_account_id (int or None): The ID of the customer's bank account. 0 is used
                when no bank account is to be indicated. Default: None.
            proforma_id (int or None): The ID of the transaction proforma. "0" is used
                when no proforma is to be indicated. Default: None.
            gateway_id: 0 is used when no gateway ID is to be indicated. Default: 0.
            currency_code_id (int or None): The ID of the currency used for the
                transaction. Default: 1 (GBP).
            currency_code (int or None): Three letter code for the currency of the
                transaction. Not required. Default: None.
            exchange_rate (int or None): The rate of exchange between the transaction currency
                and GBP. Default: None.
            login_id (int or None): Not required. Default: None
        """
        kwargs = {key: value for key, value in locals().items() if value is not None}
        return requests.handlers.CreatePayment(**kwargs)

    @staticmethod
    def add_address(
        customer_id,
        address_type,
        company_name=None,
        first_name=None,
        last_name=None,
        address_1=None,
        address_2=None,
        post_code=None,
        town=None,
        region=None,
        country=None,
        telephone_number=None,
        fax_number=None,
        mobile_number=None,
        email=None,
    ):
        """
        Add an address for a customer and return it's ID.

        Kwargs:
            customer_id (int): The customer ID of the customer to which the address
                belongs. (Required)
            address_type (str): The type of the address. Available options
                are "Admin", "Delivery" and "Billing". Optionally use
                UpdateCustomerAddress.ADMIN, UpdateCustomerAddress.DELIVERY or
                UpdateCustomerAddress.BILLING. (Required)
            company_name (str or None): The addresee's company name. Use an empty
                string if this is not applicable. Default: None.
            first_name (str or None): The addresee's first name. Default: None.
            last_name (str or None): The addresee's last name. Default: None.
            address_1 (str or None): The first line of the address. Default: None.
            address_2 (str or None): The second line of the address. Default: None.
            post_code (str or None): The postal or zip code of the address.
                Default: None.
            town (str or None): The adress's town. Default: None.
            region (str or None): The county, region or province of the address.
                Default: None.
            country (str or None): The country the address is in. Default: None.
            telephone_number (str or None): A contact telephone number for the address.
                Default: None.
            fax_number (str or None): A contact fax number for the address.
            Default: None.
            mobile_number (str or None): A contact mobile phone number for the address.
                Default: None.

        Returns:
            (str) ID of the created address.

        """
        kwargs = {key: value for key, value in locals().items() if value is not None}
        response = requests.program_type_requests.customer.UpdateCustomerAddress(
            **kwargs
        )
        return response.split("^^")[2]

    @staticmethod
    def update_address(
        customer_id,
        address_id,
        address_type,
        company_name=None,
        first_name=None,
        last_name=None,
        address_1=None,
        address_2=None,
        post_code=None,
        town=None,
        region=None,
        country=None,
        telephone_number=None,
        fax_number=None,
        mobile_number=None,
        email=None,
    ):
        """
        Add an address for a customer and return it's ID.

        Kwargs:
            customer_id (int): The customer ID of the customer to which the address
                belongs. (Required)
            address_id (str): The ID of the address to be updated. (Required)
            address_type (str): The type of the address. Available options
                are "Admin", "Delivery" and "Billing". Optionally use
                UpdateCustomerAddress.ADMIN, UpdateCustomerAddress.DELIVERY or
                UpdateCustomerAddress.BILLING. (Required)
            company_name (str or None): The addresee's company name. Use an empty string if
                this is not applicable. Default: None.
            first_name (str or None): The addresee's first name. Default: None.
            last_name (str or None): The addresee's last name. Default: None.
            address_1 (str or None): The first line of the address. Default: None.
            address_2 (str or None): The second line of the address. Default: None.
            post_code (str or None): The postal or zip code of the address.
                Default: None.
            town (str or None): The adress's town. Default: None.
            region (str or None): The county, region or province of the address.
                Default: None.
            country (str or None): The country the address is in. Default: None.
            telephone_number (str or None): A contact telephone number for the address.
                Default: None.
            fax_number (str or None): A contact fax number for the address.
            Default: None.
            mobile_number (str or None): A contact mobile phone number for the address.
                Default: None.

        Returns:
            (str) ID of the created address.

        """
        kwargs = {key: value for key, value in locals().items() if value is not None}
        requests.program_type_requests.customer.UpdateCustomerAddress(**kwargs)

    @staticmethod
    def barcode_is_in_use(barcode):
        """Return True if barcode is in use, otherwise False."""
        return requests.productbarcode.ProductBarcodeInUse(barcode)

    @classmethod
    def set_product_barcode(cls, *, barcode, product_id):
        """Set a product's barcode."""
        if cls.barcode_is_in_use(barcode) is False:
            return requests.products.SaveBarcode(barcode=barcode, product_id=product_id)
        raise Exception('Barcode "{}" is already in use'.format(barcode))

    @staticmethod
    def customer_logs(customer_id):
        """Return the logs for a customer's orders."""
        return requests.customers.GetLogs(customer_id)

    @staticmethod
    def get_product_exports():
        """Return product export information."""
        export_data = requests.exports.GetProductExportUpdate()
        return ProductExportUpdateResponse(**export_data)

    @staticmethod
    def export_products(copy_images=False):
        """
        Trigger a product export.

        Args:
            copy_images (bool): Include images in export.

        Returns:
            True if successfull.

        """
        return requests.exports.RequestProductExport(copy_images=copy_images)

    @staticmethod
    def save_product_export_file(export_file_name, path):
        """
        Save a product export file.

        Args:
            export_file_name (str): The name of the file to retrieve.
            path (pathlib.Path): The path at which the export will be saved. If the path
                is a directory export_file_name will be used as a filename.

        """
        response = requests.exports.ViewFile(export_file_name)
        path = path.absolute()
        if path.is_dir():
            filename = export_file_name + ".xlsx"
            path = path / filename
        with open(str(path), "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)

    @staticmethod
    def insert_payment(
        *, customer_id, amount, invoice_id, channel_id, payment_date=None
    ):
        """Add a payment to a customer invoice.

        Kwargs:
            customer_ID (int): The ID of the customer to apply the payment to.
            login_ID (int): The ID of the user creating the payment.
            amount (float): The amount paid.
            bank_account_ID (int): The ID of the bank account into which the payment was
                made.
            invoice_ID (int): The ID of the invoice that has been paid.
            channel_ID (int): The ID of the channel from which the invoice was created.
            payment_date (optional datetime.datetime) The date of the payment.
        """
        return requests.handlers.CustomerAccounts(
            prog_type=requests.handlers.CustomerAccounts.INSERT_PAYMENT,
            customer_id=customer_id,
            amount=amount,
            invoice_id=invoice_id,
            channel_id=channel_id,
            payment_date=payment_date,
        )

    @staticmethod
    def set_multipack(product_ID):
        """Set a product as a multipack item."""
        return requests.products.SetProductType(
            product_id=product_ID, type=requests.products.SetProductType.MULTIPACK
        )

    @staticmethod
    def set_multipack_items(*items, multipack_product_id):
        """
        Set multipack items for a multipack product.

        Args:
            multipack_product_id (str): Product ID of the multipack item to be added too.
            *items (tuple): Tuple(multipack item ID, quantity, item_price) for each item
                in the multipack.

        """
        return requests.program_type_requests.SaveSimplePackage(
            multipack_product_id, *items
        )

    @staticmethod
    def get_multipack_info(multipack_product_ID):
        """Return multipack information for a multipack product."""
        response = requests.products.FindProductSelectedOptionsOnly(
            multipack_product_ID
        )
        return response.multipack_info

    @staticmethod
    def set_hs_code(*, product_IDs, HS_code):
        """Set the HS code for a list of products."""
        return requests.products.ProductOperations(
            requests.products.ProductOperations.UPDATE_HS_CODE,
            product_IDs=product_IDs,
            HS_code=HS_code,
        )

    @staticmethod
    def recent_orders_for_customer(customer_ID):
        """Return recent orders for a customer."""
        return requests.orderhandlers.GetRecentOrdersByCustomerID(customer_ID)

    @staticmethod
    def find_hs_code(search_term):
        """Return a list of HS Codes matching the search term."""
        return requests.handlers.CommonDataSource(search_term)

    @staticmethod
    def delete_product_export(*, export_ID, export_name):
        """Delete a product export."""
        return requests.DeleteRequest(export_ID=export_ID, export_name=export_name)

    @staticmethod
    def set_country_of_origin(*, product_id, country_id):
        """Set a product's country of origin."""
        return requests.products.UpdateCountryOfOrigin(
            product_id=product_id, country_id=country_id
        )

    @staticmethod
    def get_pending_stock(product_id):
        """Return the pending stock level for a product."""
        return requests.products.GetPendingStock(product_id)

    @staticmethod
    def get_product_channel_links(product_id):
        """Return information about product channel linking."""
        return requests.sales_channels.GetProductChannelLinks(product_id)

    @staticmethod
    def get_stock_control_check(range_id):
        """Return a stock check report for a product range."""
        return requests.reports.StockControlCheck(range_id=range_id)
