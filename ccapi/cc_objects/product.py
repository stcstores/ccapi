"""This module contains the Product class."""

import ccapi

from .productoptions import ProductOption, ProductOptionValue
from .vatrates import VatRates
from .warehouse import WarehouseBay


class Product:
    """Product class containing data and methods for working with Products."""

    _options = None
    bays = None

    def __init__(self, data):
        """
        Create Product object.

        Args:
            data: Cloud Commerce Product JSON object.
        """
        self.json = data
        self.is_checked = data["isChecked"]
        self.is_listed = data["isListed"]
        self.supplier_sku = data["SupplierSKU"]
        self.id = data["ID"]
        self.name = data["Name"]
        self.full_name = data["FullName"]
        self.description = data["Description"]
        self.sku = data["ManufacturerSKU"]
        self.base_price = data["BasePrice"]
        if int(data["VatRateID"]) == 0:
            self.vat_rate_id = None
        else:
            self.vat_rate_id = int(data["VatRateID"])
        if self.vat_rate_id is not None:
            self.vat_rate = VatRates.get_vat_rate_by_id(self.vat_rate_id)
        else:
            self.vat_rate = None
        self.barcode = data["Barcode"]
        self.range_id = data["RangeID"]
        self.range_name = data["RangeName"]
        self.pre_order = data["PreOrder"]
        self.end_of_line = data["EndOfLine"]
        self.stock_level = data["StockLevel"]
        self.pseudo_stock_type = data["PseudoStockType"]
        self.pseudo_stock_level = data["PseudoStockLevel"]
        self.status_id = data["StatusID"]
        self.product_type = data["ProductType"]
        self.length_mm = data["LengthMM"]
        self.width_mm = data["WidthMM"]
        self.height_mm = data["HeightMM"]
        self.length_cm = data["LengthCM"]
        self.width_cm = data["WidthCM"]
        self.height_cm = data["HeightCM"]
        self.large_letter_compatible = data["LargeLetterCompatible"]
        self.external_product_id = data["ExternalProductId"]
        self.additional_shipping_label = data["AdditionalShippingLabel"]
        self.default_image_url = data["defaultImageUrl"]
        self.delivery_lead_time = data["DeliveryLeadTimeDays"]
        self.product_template_id = data["ProductTemplateId"]
        self.product_template_mode = data["ProductTemplateMode"]
        self.additional_barcodes = data["AdditionalBarcodes"]
        self.weight = data["WeightGM"]
        self.hs_code = data["HSCode"]
        if data["Locations"] is not None:
            self.bays = [WarehouseBay(bay) for bay in data["Locations"]]
        self.dimensions = data["Dimensions"]

    def __repr__(self):
        return self.full_name

    def get_sales_channels(self):
        """Get Sales Channels for this Product Range."""
        return ccapi.CCAPI.get_sales_channels_for_range(self.range_id)

    def get_sales_channel_ids(self):
        """Get IDs of Sales Channels on which this Product Range is listed."""
        return [channel.id for channel in self.get_sales_channels()]

    @property
    def options(self):
        """
        Product Options for this Product.

        ccapi.cc_objects.ProductOptions object with the Product Options
        applied to this Product.
        """
        if self._options is None:
            self._options = ccapi.CCAPI.get_options_for_product(self.id)
        return self._options

    def get_range(self):
        """Return ProductRange for Range to which this Product belongs."""
        return ccapi.CCAPI.get_range(self.range_id)

    def set_hs_code(self, hs_code):
        """Set the product's HS Code."""
        ccapi.CCAPI.set_hs_code(product_IDs=[self.id], HS_code=hs_code)
        self.hs_code = hs_code

    def set_option_value(self, option, value, create=False):
        """
        Set Value for Product Option for this product.

        Args:
            option: Option for which value will be set. Can be ProductOption or
                (str) option name.
            value: Value to set. Can be ProductOptionValue or (str) value.

        Kwargs:
            create: If True Value will be created if it does not already exist.
                Default: False.
        """
        if isinstance(option, ProductOption):
            option_id = option.id
        else:
            option = self.options[option]
            option_id = option.id
        if isinstance(value, ProductOptionValue):
            value_id = value.id
        else:
            try:
                value_id = option[value].id
            except KeyError:
                if create is True:
                    value_id = ccapi.CCAPI.create_option_value(option_id, value)
                else:
                    raise Exception("Product Option Value does not exist.")
        ccapi.CCAPI.set_product_option_value([self.id], option_id, value_id)

    def set_product_scope(
        self,
        weight=None,
        height=None,
        length=None,
        width=None,
        large_letter_compatible=None,
        external_id=None,
    ):
        """
        Set several attributes for Product.

        Sets weight, height, length, width, large letter compatibilty and
        external ID.

        Kwargs:
            weight: If not None sets Product weight in grams.
            height: If not None sets Product height in mm.
            length: If not None sets Product lenght in mm.
            width: If not None sets Product width in mm.
            large_letter_compatible: If not None sets Product large letter
                compatibility.
            external_id: If not None sets External ID of product.
        """
        if weight is not None:
            self.weight = weight
        if height is not None:
            self.height_mm = height
        if length is not None:
            self.length_mm = length
        if width is not None:
            self.width_mm = width
        if large_letter_compatible is not None:
            self.large_letter_compatible = large_letter_compatible
        if external_id is not None:
            self.external_product_id = external_id
        return ccapi.CCAPI.set_product_scope(
            product_id=self.id,
            weight=self.weight,
            height=self.height_mm,
            length=self.length_mm,
            width=self.width_mm,
            large_letter_compatible=self.large_letter_compatible,
            external_id=self.external_product_id,
        )

    def set_weight(self, weight):
        """Set weight for Product in grams."""
        self.set_product_scope(weight=weight)

    def set_dimensions(self, *, height, length, width):
        """Set height, lenght and width of Product in milimeters."""
        self.set_product_scope(height=height, length=length, width=width)

    def set_large_letter_compatible(self, compatible):
        """Set weather product is large letter compatible."""
        self.set_product_scope(large_letter_compatible=compatible)

    def set_external_id(self, external_id):
        """Set Product External ID."""
        self.set_product_scope(external_id=external_id)

    def set_base_price(self, price):
        """Set Product base price."""
        ccapi.CCAPI.set_product_base_price(product_id=self.id, price=price)

    def set_vat_rate(self, vat_rate):
        """Set VAT rate for product."""
        return ccapi.CCAPI.set_product_vat_rate(
            product_ids=[self.id], vat_rate=vat_rate
        )

    def set_handling_time(self, handling_time, update_channels=True):
        """
        Set handling time for product.

        Args:
            handling_time: New handling time.

        Kwargs:
            update_channels: If True will update handling time on channels.
                Default: True.
        """
        ccapi.CCAPI.set_product_handling_time(
            product_id=self.id,
            handling_time=handling_time,
            update_channels=update_channels,
        )

    def set_stock_level(self, new_stock_level, old_stock_level=None):
        """
        Set stock level for product.

        Args:
            new_stock_level: New stock level for product.

        Kwargs:
            old_stock_level: Stock level before update. If None
                self.stock_level will be used. Default: None.
        """
        if old_stock_level is None:
            old_stock_level = self.stock_level
        ccapi.CCAPI.update_product_stock_level(
            product_id=self.id,
            new_stock_level=new_stock_level,
            old_stock_level=old_stock_level,
        )

    def set_name(self, name):
        """Set name of Product."""
        ccapi.CCAPI.set_product_name(name=name, product_ids=[self.id])
        sales_channels = self.get_sales_channel_ids()
        ccapi.CCAPI.update_product_on_sales_channel(
            range_id=self.range_id,
            product_ids=[self.id],
            request_type="name",
            value_1=name,
            channels=sales_channels,
        )

    def set_description(self, description):
        """Set description for Product."""
        ccapi.CCAPI.set_product_description(
            product_ids=[self.id], description=description
        )

    def add_bay(self, bay):
        """Add product to Warehouse Bay."""
        if isinstance(bay, WarehouseBay):
            bay_id = bay.id
        else:
            bay_id = bay
        ccapi.CCAPI.add_warehouse_bay_to_product(self.id, bay_id)

    def remove_bay(self, bay):
        """Remove product from Warehouse Bay."""
        if isinstance(bay, WarehouseBay):
            bay_id = bay.id
        else:
            bay_id = bay
        ccapi.CCAPI.remove_warehouse_bay_from_product(self.id, bay_id)

    def get_images(self):
        """Get images for Product."""
        return ccapi.CCAPI.get_product_images(self.range_id, self.id)

    def add_image(self, image, channel_ids=[]):
        """Add image to Product."""
        return ccapi.CCAPI.upload_image(
            product_ids=[self.id], channel_ids=channel_ids, image_file=image
        )

    def set_image_order(self, image_ids=[]):
        """Set order of Product Images."""
        return ccapi.CCAPI.set_image_order(product_id=self.id, image_ids=image_ids)

    def get_factory_links(self):
        """Get factory links."""
        return ccapi.CCAPI.get_product_factory_links(self.id)

    def update_factory_link(self, factory_id, dropship=False, supplier_sku="", price=0):
        """Update or create Factory link."""
        return ccapi.CCAPI.update_product_factory_link(
            product_id=self.id,
            factory_id=factory_id,
            dropship=dropship,
            supplier_sku=supplier_sku,
            price=price,
        )
