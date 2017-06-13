"""This module contains the Product class."""

from ccapi import ccapi
from . location import Location
from . productoptions import ProductOption, ProductOptionValue


class Product:
    """Product class containing data and methods for working with Products."""

    _options = None
    locations = None

    def __init__(self, data):
        """
        Create Product object.

        Args:
            data: Cloud Commerce Product JSON object.
        """
        self.is_checked = data['isChecked']
        self.is_listed = data['isListed']
        self.supplier_sku = data['SupplierSKU']
        self.id = data['ID']
        self.name = data['Name']
        self.full_name = data['FullName']
        self.description = data['Description']
        self.manufacturer_sku = data['ManufacturerSKU']
        self.base_price = data['BasePrice']
        self.vat_rate_id = data['VatRateID']
        self.vat_rate = data['VatRate']
        self.barcode = data['Barcode']
        self.range_id = data['RangeID']
        self.range_name = data['RangeName']
        self.pre_order = data['PreOrder']
        self.end_of_line = data['EndOfLine']
        self.stock_level = data['StockLevel']
        self.pseudo_stock_type = data['PseudoStockType']
        self.pseudo_stock_level = data['PseudoStockLevel']
        self.status_id = data['StatusID']
        self.product_type = data['ProductType']
        self.length_mm = data['LengthMM']
        self.width_mm = data['WidthMM']
        self.height_mm = data['HeightMM']
        self.length_cm = data['LengthCM']
        self.width_cm = data['WidthCM']
        self.height_cm = data['HeightCM']
        self.large_letter_compatible = data['LargeLetterCompatible']
        self.external_product_id = data['ExternalProductId']
        self.additional_shipping_label = data['AdditionalShippingLabel']
        self.default_image_url = data['defaultImageUrl']
        self.delivery_lead_time = data['DeliveryLeadTimeDays']
        self.product_template_id = data['ProductTemplateId']
        self.product_template_mode = data['ProductTemplateMode']
        self.additional_barcodes = data['AdditionalBarcodes']
        if data['Locations'] is not None:
            self.locations = [
                Location(location) for location in data['Locations']]
        self.dimensions = data['Dimensions']

    @property
    def options(self):
        """
        Product Options for this Product.

        ccapi.inventoryitems.ProductOptions object with the Product Options
        applied to this Product.
        """
        if self._options is None:
            self._options = ccapi.CCAPI.get_options_for_product(self.id)
        return self._options

    def get_range(self):
        """Return ProductRange for Range to which this Product belongs."""
        return ccapi.CCAPI.get_ragne(self.range_id)

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
                value = option[value]
            except KeyError:
                if create is True:
                    value = option.add_value(value)
                else:
                    raise
            value_id = value.id
        ccapi.CCAPI.set_product_option_value((self.id, ), option_id, value_id)
