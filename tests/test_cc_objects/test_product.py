"""Tests for the ccapi.cc_objects.Product class."""

from ccapi import CCAPI, VatRates, cc_objects, requests

from .. import test_data, test_requests
from .test_cc_objects import TestCCObjects


class TestProduct(TestCCObjects):
    """Base class for ccapi.cc_objects.Product class test."""

    RESPONSE_DATA = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT
    PRODUCT_DATA = RESPONSE_DATA["product"]
    PRODUCT_ID = PRODUCT_DATA["ID"]

    def setUp(self):
        """Get product."""
        super().setUp()
        self.register_request(
            requests.FindProductSelectedOptionsOnly, json=self.RESPONSE_DATA
        )
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
        self.assertTrue(hasattr(self.product, "json"))
        for key, value in self.PRODUCT_DATA.items():
            if key not in ["StockLevel", "FBAStockLevel"]:
                self.assertEqual(value, self.product.json[key])

    def test_is_checked(self):
        """Test the is_checked attribute."""
        self.check_attribute("is_checked", self.PRODUCT_DATA["isChecked"])

    def test_is_listed(self):
        """Test the is_listed attribute."""
        self.check_attribute("is_listed", self.PRODUCT_DATA["isListed"])

    def test_supplier_sku(self):
        """Test the is_listed attribute."""
        self.check_attribute("supplier_sku", self.PRODUCT_DATA["SupplierSKU"])

    def test_id(self):
        """Test the id attribute."""
        self.check_attribute("id", self.PRODUCT_DATA["ID"])

    def test_name(self):
        """Test the name attribute."""
        self.check_attribute("name", self.PRODUCT_DATA["Name"])

    def test_full_name(self):
        """Test the full_name attribute."""
        self.check_attribute("full_name", self.PRODUCT_DATA["FullName"])

    def test_description(self):
        """Test the description attribute."""
        self.check_attribute("description", self.PRODUCT_DATA["Description"])

    def test_sku(self):
        """Test the sku attribute."""
        self.check_attribute("sku", self.PRODUCT_DATA["ManufacturerSKU"])

    def test_base_price(self):
        """Test the base_price attribute."""
        self.check_attribute("base_price", self.PRODUCT_DATA["BasePrice"])

    def test_vat_rate_id(self):
        """Test the vat_rate_id attribute."""
        self.check_attribute("vat_rate_id", int(self.PRODUCT_DATA["VatRateID"]))

    def test_vat_rate(self):
        """Test the vat_rate attribute."""
        self.check_attribute(
            "vat_rate", VatRates.get_vat_rate_by_id(int(self.PRODUCT_DATA["VatRateID"]))
        )

    def test_barcode(self):
        """Test the barcode attribute."""
        self.check_attribute("barcode", self.PRODUCT_DATA["Barcode"])

    def test_range_id(self):
        """Test the range_id attribute."""
        self.check_attribute("range_id", self.PRODUCT_DATA["RangeID"])

    def test_range_name(self):
        """Test the range_id attribute."""
        self.check_attribute("range_name", self.PRODUCT_DATA["RangeName"])

    def test_pre_order(self):
        """Test the pre_order attribute."""
        self.check_attribute("pre_order", self.PRODUCT_DATA["PreOrder"])

    def test_end_of_line(self):
        """Test the end_of_line attribute."""
        self.check_attribute("end_of_line", self.PRODUCT_DATA["EndOfLine"])

    def test_stock_level(self):
        """Test the stock_level attribute."""
        self.check_attribute("stock_level", self.RESPONSE_DATA["StockLevel"])

    def test_pseudo_stock_type(self):
        """Test the pseudo_stock_type attribute."""
        self.check_attribute("pseudo_stock_type", self.PRODUCT_DATA["PseudoStockType"])

    def test_pseudo_stock_level(self):
        """Test the pseudo_stock_level attribute."""
        self.check_attribute(
            "pseudo_stock_level", self.PRODUCT_DATA["PseudoStockLevel"]
        )

    def test_status_id(self):
        """Test the range_id attribute."""
        self.check_attribute("status_id", self.PRODUCT_DATA["StatusID"])

    def test_product_type(self):
        """Test the product_type attribute."""
        self.check_attribute("product_type", self.PRODUCT_DATA["ProductType"])

    def test_length_mm(self):
        """Test the length_mm attribute."""
        self.check_attribute("length_mm", self.PRODUCT_DATA["LengthMM"])

    def test_width_mm(self):
        """Test the width_mm attribute."""
        self.check_attribute("width_mm", self.PRODUCT_DATA["WidthMM"])

    def test_height_mm(self):
        """Test the height_mm attribute."""
        self.check_attribute("height_mm", self.PRODUCT_DATA["HeightMM"])

    def test_length_cm(self):
        """Test the length_cm attribute."""
        self.check_attribute("length_cm", self.PRODUCT_DATA["LengthCM"])

    def test_width_cm(self):
        """Test the width_cm attribute."""
        self.check_attribute("width_cm", self.PRODUCT_DATA["WidthCM"])

    def test_height_cm(self):
        """Test the height_cm attribute."""
        self.check_attribute("height_cm", self.PRODUCT_DATA["HeightCM"])

    def test_large_letter_compatible(self):
        """Test the large_letter_compatible attribute."""
        self.check_attribute(
            "large_letter_compatible", self.PRODUCT_DATA["LargeLetterCompatible"]
        )

    def test_external_product_id(self):
        """Test the external_product_id attribute."""
        self.check_attribute(
            "external_product_id", self.PRODUCT_DATA["ExternalProductId"]
        )

    def test_additional_shipping_label(self):
        """Test the additional_shipping_label attribute."""
        self.check_attribute(
            "additional_shipping_label", self.PRODUCT_DATA["AdditionalShippingLabel"]
        )

    def test_default_image_url(self):
        """Test the default_image_url attribute."""
        self.check_attribute("default_image_url", self.PRODUCT_DATA["defaultImageUrl"])

    def test_delivery_lead_time(self):
        """Test the delivery_lead_time attribute."""
        self.check_attribute(
            "delivery_lead_time", self.PRODUCT_DATA["DeliveryLeadTimeDays"]
        )

    def test_product_template_id(self):
        """Test the product_template_id attribute."""
        self.check_attribute(
            "product_template_id", self.PRODUCT_DATA["ProductTemplateId"]
        )

    def test_product_template_mode(self):
        """Test the product_template_mode attribute."""
        self.check_attribute(
            "product_template_mode", self.PRODUCT_DATA["ProductTemplateMode"]
        )

    def test_additional_barcodes(self):
        """Test the additional_barcodes attribute."""
        self.check_attribute(
            "additional_barcodes", self.PRODUCT_DATA["AdditionalBarcodes"]
        )

    def test_weight(self):
        """Test the weight attribute."""
        self.check_attribute("weight", self.PRODUCT_DATA["WeightGM"])

    def test_bays(self):
        """Test the bays attribute."""
        self.assertTrue(hasattr(self.product, "bays"))
        self.assertIsInstance(self.product.bays, list)
        self.assertIsInstance(self.product.bays[0], cc_objects.WarehouseBay)

    def test_dimensions(self):
        """Test the dimensions attribute."""
        self.check_attribute("dimensions", self.PRODUCT_DATA["Dimensions"])


class Test_get_sales_chanels_Method(TestProduct):
    """Test the ccapi.cc_objects.Product.get_sales_channels method."""

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(
            requests.CheckRangesOnSalesChannel,
            json=test_requests.TestCheckRangesOnSalesChannel.RESPONSE,
        )
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
        """Register request URI and call method."""
        super().setUp()
        self.register_request(
            requests.CheckRangesOnSalesChannel,
            json=test_requests.TestCheckRangesOnSalesChannel.RESPONSE,
        )
        self.returned_value = self.product.get_sales_channel_ids()

    def test_returns_list(self):
        """Test the get_sales_channel_ids method returns a list."""
        self.assertIsInstance(self.returned_value, list)

    def test_returns_sales_channel_instances(self):
        """Test the get_sales_channel_ids method returns channel IDs."""
        self.assertIsInstance(self.returned_value[0], int)


class Test_options_Property(TestProduct):
    """Test the options property of ccapi.cc_objects.Product."""

    def test_product_has_option_property(self):
        """Test product.options returns an instance of ProductOptions."""
        self.assertIsInstance(self.product.options, cc_objects.ProductOptions)

    def test_product_options_are_retrieved_if_not_set(self):
        """Test that product options are downloaded if not set."""
        self.product._options = None
        last_request = self.get_sent_request()
        options = self.product.options
        self.assertNotEqual(last_request, self.get_sent_request())
        self.assertIsInstance(options, cc_objects.ProductOptions)


class Test_get_range_Method(TestProduct):
    """Test the get_range method of ccapi.cc_objects.Product."""

    # TODO


class Test_set_option_value_Method(TestProduct):
    """Test the set_option_value method of ccapi.cc_objects.Product."""

    # TODO


class Test_set_product_scope_Method(TestProduct):
    """Test the set_product_scope method of ccapi.cc_objects.Product."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    WEIGHT = 50
    HEIGHT = 25
    LENGTH = 75
    WIDTH = 90
    LARGE_LETTER_COMPATIBLE = False
    EXTERNAL_ID = "165481035"

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)
        self.product.set_product_scope(
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID,
        )

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.product.id)

    def test_weight_is_sent(self):
        """Test the passed weight is sent."""
        self.assertDataSent("Weight", self.WEIGHT)

    def test_height_is_sent(self):
        """Test the passed height is sent."""
        self.assertDataSent("Height", self.HEIGHT)

    def test_length_is_sent(self):
        """Test the passed length is sent."""
        self.assertDataSent("Length", self.LENGTH)

    def test_width_is_sent(self):
        """Test the passed width is sent."""
        self.assertDataSent("Width", self.WIDTH)

    def test_large_letter_compatible_is_sent(self):
        """Test the passed large letter compatibilty is sent."""
        self.assertDataSent("LargeLetterCompatible", int(self.LARGE_LETTER_COMPATIBLE))

    def test_external_ID_is_sent(self):
        """Test the passed external ID is sent."""
        self.assertDataSent("ExternalID", self.EXTERNAL_ID)

    def test_weight_is_set(self):
        """Test that the product.weight attribute is updated."""
        self.assertEqual(self.product.weight, self.WEIGHT)

    def test_height_is_set(self):
        """Test that the product.height attribute is updated."""
        self.assertEqual(self.product.height_mm, self.HEIGHT)

    def test_length_is_set(self):
        """Test that the product.length attribute is updated."""
        self.assertEqual(self.product.length_mm, self.LENGTH)

    def test_width_is_set(self):
        """Test that the product.width attribute is updated."""
        self.assertEqual(self.product.width_mm, self.WIDTH)

    def test_large_letter_compatible_is_set(self):
        """Test that product.large_letter_compatible attribute is updated."""
        self.assertEqual(
            self.product.large_letter_compatible, self.LARGE_LETTER_COMPATIBLE
        )

    def test_external_id_is_set(self):
        """Test that product.external_product_id attribute is updated."""
        self.assertEqual(self.product.external_product_id, self.EXTERNAL_ID)


class Test_set_weight_Method(TestProduct):
    """Test the weight method of ccapi.cc_objects.Product."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    WEIGHT = 50

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)
        self.product.set_weight(self.WEIGHT)

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.product.id)

    def test_weight_is_sent(self):
        """Test the passed weight is sent."""
        self.assertDataSent("Weight", self.WEIGHT)

    def test_height_is_sent(self):
        """Test the passed height is sent."""
        self.assertDataSent("Height", self.product.height_mm)

    def test_length_is_sent(self):
        """Test the passed length is sent."""
        self.assertDataSent("Length", self.product.length_mm)

    def test_width_is_sent(self):
        """Test the passed width is sent."""
        self.assertDataSent("Width", self.product.width_mm)

    def test_large_letter_compatible_is_sent(self):
        """Test the passed large letter compatibilty is sent."""
        self.assertDataSent(
            "LargeLetterCompatible", int(self.product.large_letter_compatible)
        )

    def test_weight_is_set(self):
        """Test that the product.weight attribute is updated."""
        self.assertEqual(self.product.weight, self.WEIGHT)


class Test_set_dimensions_Method(TestProduct):
    """Test the set_dimensions method of ccapi.cc_objects.Product."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    HEIGHT = 25
    LENGTH = 75
    WIDTH = 90

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)
        self.product.set_dimensions(
            height=self.HEIGHT, length=self.LENGTH, width=self.WIDTH
        )

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.product.id)

    def test_weight_is_sent(self):
        """Test the passed weight is sent."""
        self.assertDataSent("Weight", self.product.weight)

    def test_height_is_sent(self):
        """Test the passed height is sent."""
        self.assertDataSent("Height", self.HEIGHT)

    def test_length_is_sent(self):
        """Test the passed length is sent."""
        self.assertDataSent("Length", self.LENGTH)

    def test_width_is_sent(self):
        """Test the passed width is sent."""
        self.assertDataSent("Width", self.WIDTH)

    def test_large_letter_compatible_is_sent(self):
        """Test the passed large letter compatibilty is sent."""
        self.assertDataSent(
            "LargeLetterCompatible", int(self.product.large_letter_compatible)
        )

    def test_height_is_set(self):
        """Test that the product.height attribute is updated."""
        self.assertEqual(self.product.height_mm, self.HEIGHT)

    def test_length_is_set(self):
        """Test that the product.length attribute is updated."""
        self.assertEqual(self.product.length_mm, self.LENGTH)

    def test_width_is_set(self):
        """Test that the product.width attribute is updated."""
        self.assertEqual(self.product.width_mm, self.WIDTH)


class Test_set_large_letter_compatible_Method(TestProduct):
    """Test the set_large_letter_compatible method of cc_objects.Product."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    LARGE_LETTER_COMPATIBLE = True

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)
        self.product.set_large_letter_compatible(self.LARGE_LETTER_COMPATIBLE)

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.product.id)

    def test_weight_is_sent(self):
        """Test the passed weight is sent."""
        self.assertDataSent("Weight", self.product.weight)

    def test_height_is_sent(self):
        """Test the passed height is sent."""
        self.assertDataSent("Height", self.product.height_mm)

    def test_length_is_sent(self):
        """Test the passed length is sent."""
        self.assertDataSent("Length", self.product.length_mm)

    def test_width_is_sent(self):
        """Test the passed width is sent."""
        self.assertDataSent("Width", self.product.width_mm)

    def test_large_letter_compatible_is_sent(self):
        """Test the passed large letter compatibilty is sent."""
        self.assertDataSent("LargeLetterCompatible", int(self.LARGE_LETTER_COMPATIBLE))

    def test_large_letter_compatible_is_set(self):
        """Test that product.large_letter_compatible attribute is updated."""
        self.assertEqual(
            self.product.large_letter_compatible, self.LARGE_LETTER_COMPATIBLE
        )


class Test_set_external_id_Method(TestProduct):
    """Test the set_external_id method of cc_objects.Product."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    EXTERNAL_ID = "165481035"

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)
        self.product.set_external_id(external_id=self.EXTERNAL_ID)

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.product.id)

    def test_weight_is_sent(self):
        """Test the passed weight is sent."""
        self.assertDataSent("Weight", self.product.weight)

    def test_height_is_sent(self):
        """Test the passed height is sent."""
        self.assertDataSent("Height", self.product.height_mm)

    def test_length_is_sent(self):
        """Test the passed length is sent."""
        self.assertDataSent("Length", self.product.length_mm)

    def test_width_is_sent(self):
        """Test the passed width is sent."""
        self.assertDataSent("Width", self.product.width_mm)

    def test_large_letter_compatible_is_sent(self):
        """Test the passed large letter compatibilty is sent."""
        self.assertDataSent(
            "LargeLetterCompatible", int(self.product.large_letter_compatible)
        )

    def test_external_ID_is_sent(self):
        """Test the passed external ID is sent."""
        self.assertDataSent("ExternalID", self.EXTERNAL_ID)

    def test_external_id_is_set(self):
        """Test that product.external_product_id attribute is updated."""
        self.assertEqual(self.product.external_product_id, self.EXTERNAL_ID)


class Test_set_base_price_Method(TestProduct):
    """Test the set_base_price method of cc_objects.Product."""

    RESPONSE = "Success"

    PRICE = "6.25"

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.UpdateProductBasePrice, text=self.RESPONSE)
        self.product.set_base_price(self.PRICE)

    def test_product_id_is_sent(self):
        """Test the product's product ID is sent."""
        self.assertDataSent("ProductIDs", [self.PRODUCT_ID])

    def test_price_is_sent(self):
        """Test the new price is sent."""
        self.assertDataSent("price", self.PRICE)


class Test_set_vat_rate_Method(TestProduct):
    """Test the set_vat_rate method of cc_objects.Product."""

    RESPONSE = "Success"

    VAT_RATE = 20
    VAT_RATE_ID = VatRates.get_vat_rate_id_by_rate(VAT_RATE)

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.UpdateProductVatRate, text=self.RESPONSE)
        self.product.set_vat_rate(self.VAT_RATE)

    def test_product_ID_is_sent(self):
        """Test the product's product ID is sent."""
        self.assertDataSent("prodids", [self.product.id])

    def test_vat_rate_ID_is_sent(self):
        """Test the product's product ID is sent."""
        self.assertDataSent("vatrate", self.VAT_RATE_ID)


class Test_set_handling_time_Method(TestProduct):
    """Test the set_handling_time method of cc_objects.Product."""

    RESPONSE = test_requests.TestSaveHandlingTime.RESPONSE
    PRODUCT_ID = "6909316"
    HANDLING_TIME = 1

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SaveHandlingTime, text=self.RESPONSE)
        self.product.set_handling_time(self.HANDLING_TIME)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product ID is sent."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

    def test_passed_handling_time_is_sent(self):
        """Test that the passed handling_time is sent."""
        self.assertDataSent("handlingTime", self.HANDLING_TIME)


class Test_set_stock_level_Method(TestProduct):
    """Test the set_stock_level method."""

    NEW_STOCK_LEVEL = 5

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(
            requests.UpdateProductStockLevel,
            text=test_requests.TestUpdateProductStockLevel.RESPONSE,
        )
        self.original_stock_level = self.product.stock_level
        self.product.set_stock_level(self.NEW_STOCK_LEVEL)

    def test_product_ID_is_sent(self):
        """Test the product ID is sent."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

    def test_the_old_stock_level_is_sent(self):
        """Test that the old stock level is sent."""
        self.assertDataSent("oldStockLevel", self.original_stock_level)

    def test_the_new_stock_level_is_sent(self):
        """Test that the new stock level is sent."""
        self.assertDataSent("newStockLevel", self.NEW_STOCK_LEVEL)

    def test_the_product_stock_level_is_updated(self):
        """Test that the product's stock_level attribute is updated."""
        self.assertEqual(self.product.stock_level, self.NEW_STOCK_LEVEL)


class Test_set_name_Method(TestProduct):
    """Test the set_name method."""

    NEW_PRODUCT_NAME = "New Product Name"

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(
            requests.SaveProductName, text=test_requests.TestSaveProductName.RESPONSE
        )
        self.register_request(
            requests.UpdateProductOnSalesChannel,
            json=test_requests.TestUpdateOnSalesChannel.RESPONSE,
        )
        self.register_request(
            requests.CheckRangesOnSalesChannel,
            json=test_data.CHECK_RANGES_ON_SALES_CHANNEL_RESULT,
        )
        self.product.set_name(self.NEW_PRODUCT_NAME)
        self.SaveProductName_request = self.get_sent_request(skip=3)
        self.UpdateProductOnSalesChannel_request = self.get_sent_request(skip=1)

    def test_set_name_sends_SaveProductName_request(self):
        """Test the Product.set_name method sends a SaveProductName request."""
        self.assertRequestUsesRequestClassURI(
            requests.SaveProductName, self.SaveProductName_request
        )

    def test_set_name_sends_product_ID(self):
        """Test the Product.set_name method sends the product's ID."""
        self.assertDataSent(
            "prodids", [self.PRODUCT_ID], request=self.SaveProductName_request
        )

    def test_set_name_sends_new_product_name(self):
        """Test the Product.set_name method sends the new product name."""
        self.assertDataSent(
            "name", self.NEW_PRODUCT_NAME, request=self.SaveProductName_request
        )

    def test_set_name_sends_UpdateProductOnSalesChannel_request(self):
        """Test the method sends an UpdateProductOnSalesChannel request."""
        self.assertRequestUsesRequestClassURI(
            requests.UpdateProductOnSalesChannel,
            self.UpdateProductOnSalesChannel_request,
        )
        self.assertDataSent(
            "rangeid",
            self.product.range_id,
            request=self.UpdateProductOnSalesChannel_request,
        )
        self.assertDataSent(
            "prodids",
            [self.PRODUCT_ID],
            request=self.UpdateProductOnSalesChannel_request,
        )
        self.assertDataSent(
            "type", "name", request=self.UpdateProductOnSalesChannel_request
        )
        self.assertDataSent(
            "val1",
            self.NEW_PRODUCT_NAME,
            request=self.UpdateProductOnSalesChannel_request,
        )


class Test_set_description_Method(TestProduct):
    """Test the set_description method."""

    DESCRIPTION = "Product Description\n"

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(
            requests.SaveDescription, text=test_requests.TestSaveDescription.RESPONSE
        )
        self.product.set_description(self.DESCRIPTION)

    def test_product_ID_is_sent(self):
        """Test the product ID is sent."""
        self.assertDataSent("prodids", [self.PRODUCT_ID])

    def test_description_is_sent(self):
        """Test the description is sent."""
        self.assertDataSent("desc", self.DESCRIPTION)


class Test_add_bay_Method(TestProduct):
    """Test the add_bay method of cc_objects.Product."""

    # TODO


class Test_remove_bay_Method(TestProduct):
    """Test the remove_bay method of cc_objects.Product."""

    # TODO


class Test_get_images_Method(TestProduct):
    """Test the get_images method of cc_objects.Product."""

    # TODO


class Test_add_image_Method(TestProduct):
    """Test the add_image method of cc_objects.Product."""

    RESPONSE = test_requests.TestUploadImage.SUCCESSFUL_RESPONSE

    PRODUCT_IDS = ["123654", "6909316"]
    IMAGE = test_requests.TestUploadImage.IMAGE

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.UploadImage, json=self.RESPONSE)
        self.product.add_image(self.IMAGE)

    def test_product_ID_is_sent(self):
        """Test that the products ID is sent."""
        sent_data = self.get_sent_request_query()
        self.assertIn(str(self.product.id), str(sent_data["prodids"]))


class Test_set_image_order_Method(TestProduct):
    """Test the set_image_order method of cc_objects.Product."""

    RESPONSE = test_requests.TestSetImageOrder.RESPONSE
    IMAGE_IDS = ["28179547", "28179563", "28179581"]

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.SetImageOrder, text=self.RESPONSE)
        self.product.set_image_order(self.IMAGE_IDS)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product ID is sent."""
        self.assertDataSent("prodid", self.product.id)

    def test_passed_handling_time_is_sent(self):
        """Test that the passed image IDs are sent."""
        self.assertDataSent("order", "^^".join(self.IMAGE_IDS))


class Test_get_factory_links_Method(TestProduct):
    """Test the get_factory_links method of cc_objects.Product."""

    RESPONSE = [test_requests.TestFindProductFactoryLinks.RESPONSE]

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.FindProductFactoryLinks, json=self.RESPONSE)
        self.factories = self.product.get_factory_links()

    def test_sends_product_ID(self):
        """Test sends the product's ID."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

    def test_returns_FactoryLinks_instance(self):
        """Test returns FactoryLinks instance."""
        self.assertIsInstance(self.factories, cc_objects.FactoryLinks)


class Test_update_factory_link_Method(TestProduct):
    """Test the update_factory_link method of cc_objects.Product."""

    # TODO
