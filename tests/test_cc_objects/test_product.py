"""Tests for the ccapi.cc_objects.Product class."""

from ccapi import CCAPI, VatRates, cc_objects, requests

from .. import test_data, test_requests
from .test_cc_objects import TestCCObjects


class TestProduct(TestCCObjects):
    """Base class for ccapi.cc_objects.Product class test."""

    RESPONSE_DATA = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT
    PRODUCT_DATA = RESPONSE_DATA['product']
    PRODUCT_ID = PRODUCT_DATA['ID']

    def setUp(self):
        """Get product."""
        super().setUp()
        self.register_request(
            requests.FindProductSelectedOptionsOnly, json=self.RESPONSE_DATA)
        self.product = CCAPI.get_product(self.PRODUCT_ID)


class TestProductIsReturned(TestProduct):
    """Test that the product is an instance of ccapi.cc_objects.Product."""

    def test_Product_is_returned(self):
        """Test that the product is an instance of ccapi.cc_objects.Product."""
        self.assertIsInstance(self.product, cc_objects.Product)


class TestProductAttributes(TestProduct):
    """Test that an instance of Product has correct attributes."""

    def check_attribute(self, attribute, expected_value):
        """Check the product has an attribute and it has the expected value."""
        self.assertTrue(hasattr(self.product, attribute))
        self.assertEqual(getattr(self.product, attribute), expected_value)

    def test_json(self):
        """Test that the product has a json attribute."""
        self.assertTrue(hasattr(self.product, 'json'))
        for key, value in self.PRODUCT_DATA.items():
            if key not in ['StockLevel', 'FBAStockLevel']:
                self.assertEqual(value, self.product.json[key])

    def test_is_checked(self):
        """Test the is_checked attribute."""
        self.check_attribute('is_checked', self.PRODUCT_DATA['isChecked'])

    def test_is_listed(self):
        """Test the is_listed attribute."""
        self.check_attribute('is_listed', self.PRODUCT_DATA['isListed'])

    def test_supplier_sku(self):
        """Test the is_listed attribute."""
        self.check_attribute('supplier_sku', self.PRODUCT_DATA['SupplierSKU'])

    def test_id(self):
        """Test the id attribute."""
        self.check_attribute('id', self.PRODUCT_DATA['ID'])

    def test_name(self):
        """Test the name attribute."""
        self.check_attribute('name', self.PRODUCT_DATA['Name'])

    def test_full_name(self):
        """Test the full_name attribute."""
        self.check_attribute('full_name', self.PRODUCT_DATA['FullName'])

    def test_description(self):
        """Test the description attribute."""
        self.check_attribute('description', self.PRODUCT_DATA['Description'])

    def test_sku(self):
        """Test the sku attribute."""
        self.check_attribute('sku', self.PRODUCT_DATA['ManufacturerSKU'])

    def test_base_price(self):
        """Test the base_price attribute."""
        self.check_attribute('base_price', self.PRODUCT_DATA['BasePrice'])

    def test_vat_rate_id(self):
        """Test the vat_rate_id attribute."""
        self.check_attribute(
            'vat_rate_id', int(self.PRODUCT_DATA['VatRateID']))

    def test_vat_rate(self):
        """Test the vat_rate attribute."""
        self.check_attribute(
            'vat_rate',
            VatRates.get_vat_rate_by_id(int(self.PRODUCT_DATA['VatRateID'])))

    def test_barcode(self):
        """Test the barcode attribute."""
        self.check_attribute('barcode', self.PRODUCT_DATA['Barcode'])

    def test_range_id(self):
        """Test the range_id attribute."""
        self.check_attribute('range_id', self.PRODUCT_DATA['RangeID'])

    def test_range_name(self):
        """Test the range_id attribute."""
        self.check_attribute('range_name', self.PRODUCT_DATA['RangeName'])

    def test_pre_order(self):
        """Test the pre_order attribute."""
        self.check_attribute('pre_order', self.PRODUCT_DATA['PreOrder'])

    def test_end_of_line(self):
        """Test the end_of_line attribute."""
        self.check_attribute('end_of_line', self.PRODUCT_DATA['EndOfLine'])

    def test_stock_level(self):
        """Test the stock_level attribute."""
        self.check_attribute('stock_level', self.RESPONSE_DATA['StockLevel'])

    def test_pseudo_stock_type(self):
        """Test the pseudo_stock_type attribute."""
        self.check_attribute(
            'pseudo_stock_type', self.PRODUCT_DATA['PseudoStockType'])

    def test_pseudo_stock_level(self):
        """Test the pseudo_stock_level attribute."""
        self.check_attribute(
            'pseudo_stock_level', self.PRODUCT_DATA['PseudoStockLevel'])

    def test_status_id(self):
        """Test the range_id attribute."""
        self.check_attribute('status_id', self.PRODUCT_DATA['StatusID'])

    def test_product_type(self):
        """Test the product_type attribute."""
        self.check_attribute('product_type', self.PRODUCT_DATA['ProductType'])

    def test_length_mm(self):
        """Test the length_mm attribute."""
        self.check_attribute('length_mm', self.PRODUCT_DATA['LengthMM'])

    def test_width_mm(self):
        """Test the width_mm attribute."""
        self.check_attribute('width_mm', self.PRODUCT_DATA['WidthMM'])

    def test_height_mm(self):
        """Test the height_mm attribute."""
        self.check_attribute('height_mm', self.PRODUCT_DATA['HeightMM'])

    def test_length_cm(self):
        """Test the length_cm attribute."""
        self.check_attribute('length_cm', self.PRODUCT_DATA['LengthCM'])

    def test_width_cm(self):
        """Test the width_cm attribute."""
        self.check_attribute('width_cm', self.PRODUCT_DATA['WidthCM'])

    def test_height_cm(self):
        """Test the height_cm attribute."""
        self.check_attribute('height_cm', self.PRODUCT_DATA['HeightCM'])

    def test_large_letter_compatible(self):
        """Test the large_letter_compatible attribute."""
        self.check_attribute(
            'large_letter_compatible',
            self.PRODUCT_DATA['LargeLetterCompatible'])

    def test_external_product_id(self):
        """Test the external_product_id attribute."""
        self.check_attribute(
            'external_product_id', self.PRODUCT_DATA['ExternalProductId'])

    def test_additional_shipping_label(self):
        """Test the additional_shipping_label attribute."""
        self.check_attribute(
            'additional_shipping_label',
            self.PRODUCT_DATA['AdditionalShippingLabel'])

    def test_default_image_url(self):
        """Test the default_image_url attribute."""
        self.check_attribute(
            'default_image_url', self.PRODUCT_DATA['defaultImageUrl'])

    def test_delivery_lead_time(self):
        """Test the delivery_lead_time attribute."""
        self.check_attribute(
            'delivery_lead_time', self.PRODUCT_DATA['DeliveryLeadTimeDays'])

    def test_product_template_id(self):
        """Test the product_template_id attribute."""
        self.check_attribute(
            'product_template_id', self.PRODUCT_DATA['ProductTemplateId'])

    def test_product_template_mode(self):
        """Test the product_template_mode attribute."""
        self.check_attribute(
            'product_template_mode', self.PRODUCT_DATA['ProductTemplateMode'])

    def test_additional_barcodes(self):
        """Test the additional_barcodes attribute."""
        self.check_attribute(
            'additional_barcodes', self.PRODUCT_DATA['AdditionalBarcodes'])

    def test_weight(self):
        """Test the weight attribute."""
        self.check_attribute('weight', self.PRODUCT_DATA['WeightGM'])

    def test_bays(self):
        """Test the bays attribute."""
        self.assertTrue(hasattr(self.product, 'bays'))
        self.assertIsInstance(self.product.bays, list)
        self.assertIsInstance(self.product.bays[0], cc_objects.WarehouseBay)

    def test_dimensions(self):
        """Test the dimensions attribute."""
        self.check_attribute('dimensions', self.PRODUCT_DATA['Dimensions'])


class Test_set_stock_level_Method(TestProduct):
    """Test the set_stock_level method."""

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.UpdateProductStockLevel,
            text=test_requests.TestUpdateProductStockLevel.RESPONSE)

    def test_set_stock_level(self):
        """Test the Product.set_stock_level method."""
        original_stock_level = self.product.stock_level
        new_stock_level = 5
        self.product.set_stock_level(new_stock_level)
        self.assertDataSent('ProductID', self.PRODUCT_ID)
        self.assertDataSent('newStockLevel', new_stock_level)
        self.assertDataSent('oldStockLevel', original_stock_level)


class Test_set_name_Method(TestProduct):
    """Test the set_name method."""

    NEW_PRODUCT_NAME = 'New Product Name'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.SaveProductName,
            text=test_requests.TestSaveProductName.RESPONSE)
        self.register_request(
            requests.UpdateProductOnSalesChannel,
            json=test_requests.TestUpdateOnSalesChannel.RESPONSE)
        self.register_request(
            requests.CheckRangesOnSalesChannel,
            json=test_data.CHECK_RANGES_ON_SALES_CHANNEL_RESULT)
        self.product.set_name(self.NEW_PRODUCT_NAME)
        self.SaveProductName_request = self.get_sent_request(skip=3)
        self.UpdateProductOnSalesChannel_request = self.get_sent_request(
            skip=1)

    def test_set_name_sends_SaveProductName_request(self):
        """Test the Product.set_name method sends a SaveProductName request."""
        self.assertRequestUsesRequestClassURI(
            requests.SaveProductName, self.SaveProductName_request)

    def test_set_name_sends_product_ID(self):
        """Test the Product.set_name method sends the product's ID."""
        self.assertDataSent(
            'prodids', [self.PRODUCT_ID], request=self.SaveProductName_request)

    def test_set_name_sends_new_product_name(self):
        """Test the Product.set_name method sends the new product name."""
        self.assertDataSent(
            'name',
            self.NEW_PRODUCT_NAME,
            request=self.SaveProductName_request)

    def test_set_name_sends_UpdateProductOnSalesChannel_request(self):
        """Test the method sends an UpdateProductOnSalesChannel request."""
        self.assertRequestUsesRequestClassURI(
            requests.UpdateProductOnSalesChannel,
            self.UpdateProductOnSalesChannel_request)
        self.assertDataSent(
            'rangeid',
            self.product.range_id,
            request=self.UpdateProductOnSalesChannel_request)
        self.assertDataSent(
            'prodids', [self.PRODUCT_ID],
            request=self.UpdateProductOnSalesChannel_request)
        self.assertDataSent(
            'type', 'name', request=self.UpdateProductOnSalesChannel_request)
        self.assertDataSent(
            'val1',
            self.NEW_PRODUCT_NAME,
            request=self.UpdateProductOnSalesChannel_request)


class Test_set_description_Method(TestProduct):
    """Test the set_description method."""

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.SaveDescription,
            text=test_requests.TestSaveDescription.RESPONSE)

    def test_set_description(self):
        """Test the set_description method."""
        description = 'Product Description\n'
        self.product.set_description(description)
        self.assertDataSent('prodids', [self.PRODUCT_ID])
        self.assertDataSent('desc', description)


class Test_get_sales_chanels_Method(TestProduct):
    """Test the ccapi.cc_objects.Product.get_sales_channels method."""

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.CheckRangesOnSalesChannel,
            json=test_requests.TestCheckRangesOnSalesChannel.RESPONSE)
        self.returned_value = self.product.get_sales_channels()

    def test_returns_list(self):
        """Test the get_sales_channels method returns a list."""
        self.assertIsInstance(self.returned_value, list)

    def test_returns_sales_channel_instances(self):
        """Test the get_sales_channels method returns SalesChannels."""
        self.assertIsInstance(self.returned_value[0], cc_objects.SalesChannel)


class Test_get_sales_channel_ids_Method(TestProduct):
    """Test the ccapi.cc_objects.Product.get_sales_channel_ids method."""

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.CheckRangesOnSalesChannel,
            json=test_requests.TestCheckRangesOnSalesChannel.RESPONSE)
        self.returned_value = self.product.get_sales_channel_ids()

    def test_returns_list(self):
        """Test the get_sales_channel_ids method returns a list."""
        self.assertIsInstance(self.returned_value, list)

    def test_returns_sales_channel_instances(self):
        """Test the get_sales_channel_ids method returns channel IDs."""
        self.assertIsInstance(self.returned_value[0], int)
