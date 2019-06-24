"""Tests for CCAPI's methods."""

import datetime
import json
import shutil
import tempfile
from pathlib import Path

from ccapi import CCAPI, NewOrderItem, VatRates, cc_objects, requests

from .. import test_data, test_requests
from .test_CCAPI_class import TestCCAPIMethod


class Test_get_sku_Method(TestCCAPIMethod):
    """Test the get_sku method of CCAPI."""

    SKU = test_requests.TestProductOperations.SKU
    RESPONSE = test_requests.TestProductOperations.RESPONSE

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.ProductOperations, json=self.RESPONSE)

    def test_get_sku(self):
        """Test the get_sku method of CCAPI."""
        sku = CCAPI.get_sku()
        self.assertEqual(sku, self.SKU)

    def test_get_range_sku(self):
        """Test the get_sku method of CCAPI."""
        range_sku = CCAPI.get_sku(range_sku=True)
        self.assertEqual(range_sku, "RNG_" + self.SKU)


class Test_create_product_Method(TestCCAPIMethod):
    """Test the create_product method of CCAPI."""

    RANGE_ID = "4347654"
    NAME = "Product Name"
    BARCODE = "12345678912"
    SKU = "WUA-DU7-W6W"
    DESCRIPTION = "Product Description"
    VAT_RATE = 20

    CREATED_PRODUCT_ID = test_requests.TestAddProduct.CREATED_PRODUCT_ID
    RESPONSE = test_requests.TestAddProduct.SUCCESSFUL_RESPONSE

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.AddProduct, text=self.RESPONSE)


class Test_create_product_MethodPassingSKU(Test_create_product_Method):
    """Test the create_product method when an SKU is passed."""

    def setUp(self):
        """Make request."""
        super().setUp()
        CCAPI.create_product(
            range_id=self.RANGE_ID,
            name=self.NAME,
            barcode=self.BARCODE,
            sku=self.SKU,
            description=self.DESCRIPTION,
            vat_rate=self.VAT_RATE,
        )

    def test_sends_product_ID(self):
        """Test a product ID is sent."""
        self.assertDataSent("ProdRangeID", self.RANGE_ID)

    def test_sends_product_name(self):
        """Test a product name is sent."""
        self.assertDataSent("ProdName", self.NAME)

    def test_sends_barcode(self):
        """Test a barcode is sent."""
        self.assertDataSent("BarCode", self.BARCODE)

    def test_sends_SKU(self):
        """Test a SKU is sent."""
        self.assertDataSent("SKUCode", self.SKU)

    def test_sends_description(self):
        """Test a description is sent."""
        self.assertDataSent("ProdDescription", self.DESCRIPTION)

    def test_sends_VAT_rate_ID(self):
        """Test a VAT rate ID is sent."""
        self.assertDataSent(
            "VatRateID", VatRates.get_vat_rate_id_by_rate(self.VAT_RATE)
        )


class Test_create_product_MethodWithoutPassingSKU(Test_create_product_Method):
    """Test the create_product method without passing a SKU."""

    def setUp(self):
        """Register URI and make request."""
        super().setUp()
        self.register_request(
            requests.ProductOperations, json=Test_get_sku_Method.RESPONSE
        )
        CCAPI.create_product(
            range_id=self.RANGE_ID,
            name=self.NAME,
            barcode=self.BARCODE,
            sku=None,
            description=self.DESCRIPTION,
            vat_rate=self.VAT_RATE,
        )

    def test_sends_request_for_new_SKU(self):
        """Test a request is sent for a new SKU if none is provided."""
        self.assertRequestUsesRequestClassURI(
            requests.ProductOperations, request=self.get_sent_request(skip=2)
        )

    def test_sends_generated_SKU(self):
        """Test create_product sends the new SKU."""
        self.assertDataSent("SKUCode", Test_get_sku_Method.SKU)


class Test_create_product_MethodWithoutPassingADescription(Test_create_product_Method):
    """Test the create_product method without passing a description."""

    def setUp(self):
        """Make request."""
        super().setUp()
        CCAPI.create_product(
            range_id=self.RANGE_ID,
            name=self.NAME,
            barcode=self.BARCODE,
            sku=self.SKU,
            description=None,
            vat_rate=self.VAT_RATE,
        )

    def test_create_product_without_description(self):
        """Test create_product handles description not being passed."""
        self.assertDataSent("ProdDescription", self.NAME)


class Test_delete_product_factory_links_Method(TestCCAPIMethod):
    """Test the CCAPI.delete_product_factory_links method."""

    RESPONSE = test_requests.TestDeleteAllProductFactoryLink.RESPONSE
    FACTORY_ID = "11782"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.DeleteAllProductFactoryLink, text=self.RESPONSE)
        CCAPI.delete_product_factory_links(self.FACTORY_ID)

    def test_sends_correct_factory_ID(self):
        """Test the correct factory ID is sent."""
        self.assertDataSent("FactoryID", self.FACTORY_ID)


class Test_delete_image_Method(TestCCAPIMethod):
    """Test the CCAPI.delete_image method."""

    IMAGE_ID = "28173405"
    RESPONSE = test_requests.TestDeleteImage.RESPONSE

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.DeleteImage, text=self.RESPONSE)
        CCAPI.delete_image(self.IMAGE_ID)

    def test_sends_passed_image_ID(self):
        """Test the correct image ID is sent."""
        self.assertDataSent("imgID", self.IMAGE_ID)


class Test_delete_product_factory_link_Method(TestCCAPIMethod):
    """Test the CCAPI.delete_product_factory_link method."""

    FACTORY_ID = "3544350"
    RESPONSE = test_requests.TestDeleteProductFactoryLink.RESPONSE

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.DeleteProductFactoryLink, text=self.RESPONSE)
        CCAPI.delete_product_factory_link(self.FACTORY_ID)

    def test_sends_passed_factory_ID(self):
        """Test the passed factory ID is sent."""
        self.assertDataSent("factoryLinkIds", self.FACTORY_ID)


class Test_search_products_Method(TestCCAPIMethod):
    """Test the CCAPI.search_products method."""

    RESPONSE = test_requests.TestDoSearch.SUCCESSFUL_RESPONSE
    SEARCH_TEXT = "WUA-DU7-W6W"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.DoSearch, json=self.RESPONSE)
        self.products = CCAPI.search_products(self.SEARCH_TEXT)

    def test_sends_correct_product_ID(self):
        """Test sends the correct productID."""
        self.assertDataSent("text", self.SEARCH_TEXT)

    def test_returns_list(self):
        """Test returns a list instance."""
        self.assertIsInstance(self.products, list)

    def test_search_result(self):
        """Test returned list contains object with the correct attributes."""
        self.assertTrue(hasattr(self.products[0], "id"))
        self.assertTrue(hasattr(self.products[0], "variation_id"))
        self.assertTrue(hasattr(self.products[0], "name"))
        self.assertTrue(hasattr(self.products[0], "sku"))
        self.assertTrue(hasattr(self.products[0], "thumbnail"))


class Test_get_product_factory_links_Method(TestCCAPIMethod):
    """Test the CCAPI.get_product_factory_links method."""

    PRODUCT_ID = 6_909_316
    RESPONSE = [test_requests.TestFindProductFactoryLinks.RESPONSE]

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.FindProductFactoryLinks, json=self.RESPONSE)
        self.factories = CCAPI.get_product_factory_links(self.PRODUCT_ID)

    def test_sends_passed_product_ID(self):
        """Test sends the passed product ID."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

    def test_returns_FactoryLinks_instance(self):
        """Test returns FactoryLinks instance."""
        self.assertIsInstance(self.factories, cc_objects.FactoryLinks)


class Test_get_product_Method(TestCCAPIMethod):
    """Test the CCAPI.get_product method."""

    PRODUCT_ID = 6_909_316
    RESPONSE = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.FindProductSelectedOptionsOnly, json=self.RESPONSE
        )
        self.product = CCAPI.get_product(self.PRODUCT_ID)

    def test_get_product_sends_correct_product_ID(self):
        """Test CCAPI.get_product sends the passed product ID ."""
        self.assertIsInstance(self.product, cc_objects.Product)

    def test_get_product_returns_a_product(self):
        """Test CCAPI.get_product returns an cc_objects.Product."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)


class Test_get_options_for_product_Method(TestCCAPIMethod):
    """Test the CCAPI.get_options_for_product method."""

    PRODUCT_ID = 6_909_316
    RESPONSE = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.FindProductSelectedOptionsOnly, json=self.RESPONSE
        )
        self.product = CCAPI.get_options_for_product(self.PRODUCT_ID)

    def test_get_product_sends_correct_product_ID(self):
        """Test CCAPI.get_product sends the passed product ID ."""
        self.assertIsInstance(self.product, cc_objects.ProductOptions)

    def test_get_product_returns_a_product(self):
        """Test CCAPI.get_product returns an cc_objects.Product."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)


class Test_barcode_is_in_use_Method(TestCCAPIMethod):
    """Test the CCAPI.barcode_is_in_use method."""

    RESPONSE = test_requests.TestProductBarcodeInUse.UNUSED_RESPONSE
    BARCODE = "1321564981"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.ProductBarcodeInUse, json=self.RESPONSE)
        self.barcode_used = CCAPI.barcode_is_in_use(barcode=self.BARCODE)

    def test_passed_barcode_is_sent(self):
        """Test the correct barcode is sent."""
        self.assertDataSent("BarcodeNumber", self.BARCODE)

    def test_bool_is_returned(self):
        """Test that the method returns a boolean."""
        self.assertIsInstance(self.barcode_used, bool)


class Test_set_product_barcode_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_barcode method."""

    BARCODE_USED_RESPONSE = test_requests.TestProductBarcodeInUse.USED_RESPONSE
    BARCODE_UNUSED_RESPONSE = test_requests.TestProductBarcodeInUse.UNUSED_RESPONSE
    RESPONSE = test_requests.TestSaveBarcode.RESPONSE
    BARCODE = "1321564981"
    PRODUCT_ID = "123654"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.ProductBarcodeInUse, json=self.BARCODE_UNUSED_RESPONSE
        )
        self.register_request(requests.SaveBarcode, text=self.RESPONSE)
        CCAPI.set_product_barcode(barcode=self.BARCODE, product_id=self.PRODUCT_ID)

    def test_uses_ProductBarcodeInUse_request(self):
        """Test set_product_barcode uses the ProductBarcodeInUse request."""
        self.assertRequestUsesRequestClassURI(
            requests.ProductBarcodeInUse, self.get_sent_request(skip=2)
        )

    def test_passed_barcode_is_sent(self):
        """Test the correct barcode is sent."""
        self.assertDataSent("bcode", self.BARCODE)

    def test_passed_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("prodid", self.PRODUCT_ID)

    def test_raises_for_used_barcode(self):
        """Test exception is raised if barcode is in use."""
        self.register_request(
            requests.ProductBarcodeInUse, json=self.BARCODE_USED_RESPONSE
        )
        with self.assertRaises(Exception):
            CCAPI.set_product_barcode(barcode=self.BARCODE, product_id=self.PRODUCT_ID)


class Test_set_product_description_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_description method."""

    RESPONSE = test_requests.TestSaveDescription.RESPONSE
    PRODUCT_IDS = ["123654", "6909316"]
    DESCRIPTION = "A description of a product\n"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SaveDescription, text=self.RESPONSE)
        CCAPI.set_product_description(
            product_ids=[self.PRODUCT_IDS], description=self.DESCRIPTION
        )

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        sent_data = self.get_sent_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data["prodids"]))

    def test_passed_description_is_sent(self):
        """Test that the passed description is sent."""
        self.assertDataSent("desc", self.DESCRIPTION)

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_description(
            product_ids=self.PRODUCT_IDS[0], description=self.DESCRIPTION
        )
        sent_data = self.get_sent_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data["prodids"]))


class Test_set_product_handling_time_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_handling_time method."""

    RESPONSE = test_requests.TestSaveHandlingTime.RESPONSE
    PRODUCT_ID = "6909316"
    HANDLING_TIME = 1

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SaveHandlingTime, text=self.RESPONSE)
        CCAPI.set_product_handling_time(
            product_id=self.PRODUCT_ID, handling_time=self.HANDLING_TIME
        )

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product ID is sent."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

    def test_passed_handling_time_is_sent(self):
        """Test that the passed handling_time is sent."""
        self.assertDataSent("handlingTime", self.HANDLING_TIME)


class Test_set_product_name_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_name method."""

    RESPONSE = test_requests.TestSaveProductName.RESPONSE
    PRODUCT_IDS = ["123654", "6909316"]
    NAME = "Product Name"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SaveProductName, text=self.RESPONSE)
        CCAPI.set_product_name(product_ids=[self.PRODUCT_IDS], name=self.NAME)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        sent_data = self.get_sent_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data["prodids"]))

    def test_passed_description_is_sent(self):
        """Test that the passed name is sent."""
        self.assertDataSent("name", self.NAME)

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_name(product_ids=self.PRODUCT_IDS[0], name=self.NAME)
        sent_data = self.get_sent_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data["prodids"]))


class Test_set_image_order_Method(TestCCAPIMethod):
    """Test the CCAPI.set_image_order method."""

    RESPONSE = test_requests.TestSetImageOrder.RESPONSE
    IMAGE_IDS = ["28179547", "28179563", "28179581"]
    PRODUCT_ID = "6909316"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SetImageOrder, text=self.RESPONSE)
        CCAPI.set_image_order(product_id=self.PRODUCT_ID, image_ids=self.IMAGE_IDS)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product ID is sent."""
        self.assertDataSent("prodid", self.PRODUCT_ID)

    def test_passed_handling_time_is_sent(self):
        """Test that the passed image IDs are sent."""
        self.assertDataSent("order", "^^".join(self.IMAGE_IDS))


class Test_set_product_option_value_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_option_value method."""

    RESPONSE = test_requests.TestSetProductOptionValue.RESPONSE
    PRODUCT_IDS = ["123654", "6909316"]
    OPTION_ID = "32131"
    OPTION_VALUE_ID = "3040649"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SetProductOptionValue, text=self.RESPONSE)
        CCAPI.set_product_option_value(
            product_ids=self.PRODUCT_IDS,
            option_id=self.OPTION_ID,
            option_value_id=self.OPTION_VALUE_ID,
        )

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        sent_data = self.get_sent_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data["prodids"]))

    def test_passed_option_ID_is_sent(self):
        """Test that the passed option ID is sent."""
        self.assertDataSent("OptionID", self.OPTION_ID)

    def test_passed_option_value_is_sent(self):
        """Test that the passed option value is sent."""
        self.assertDataSent("OptionValueID", self.OPTION_VALUE_ID)

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_option_value(
            product_ids=self.PRODUCT_IDS[0],
            option_id=self.OPTION_ID,
            option_value_id=self.OPTION_VALUE_ID,
        )
        sent_data = self.get_sent_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data["prodids"]))


class Test_set_product_scope_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_scope method."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    PRODUCT_ID = "6909316"
    WEIGHT = 50
    HEIGHT = 25
    LENGTH = 75
    WIDTH = 90
    LARGE_LETTER_COMPATIBLE = False
    EXTERNAL_ID = "165481035"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID,
        )

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

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

    def test_external_ID_None(self):
        """Test no external ID is sent when None is passed."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=None,
        )
        self.assertDataValueIsNone("ExternalID")


class Test_set_product_base_price_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_base_price method."""

    RESPONSE = test_requests.TestUpdateProductBasePrice.RESPONSE

    PRODUCT_ID = "6909316"
    PRICE = "6.25"

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.UpdateProductBasePrice, text=self.RESPONSE)
        CCAPI.set_product_base_price(product_id=self.PRODUCT_ID, price=self.PRICE)

    def test_passed_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductIDs", [self.PRODUCT_ID])

    def test_passed_price_is_sent(self):
        """Test the passed price is sent."""
        self.assertDataSent("price", self.PRICE)


class Test_update_product_stock_level_Method(TestCCAPIMethod):
    """Test the CCAPI.update_product_stock_level method."""

    RESPONSE = test_requests.TestUpdateProductStockLevel.RESPONSE

    PRODUCT_ID = "6909316"
    NEW_STOCK_LEVEL = 5
    OLD_STOCK_LEVEL = 10

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.UpdateProductStockLevel, text=self.RESPONSE)
        CCAPI.update_product_stock_level(
            product_id=self.PRODUCT_ID,
            new_stock_level=self.NEW_STOCK_LEVEL,
            old_stock_level=self.OLD_STOCK_LEVEL,
        )

    def test_passed_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent("ProductID", self.PRODUCT_ID)

    def test_passed_new_stock_level_is_sent(self):
        """Test the passed new stock level is sent."""
        self.assertDataSent("newStockLevel", self.NEW_STOCK_LEVEL)

    def test_passed_old_stock_level_is_sent(self):
        """Test the passed old stock level is sent."""
        self.assertDataSent("oldStockLevel", self.OLD_STOCK_LEVEL)


class Test_set_product_vat_rate_Method(TestCCAPIMethod):
    """Test the CCAPI.set_product_vat_rate method."""

    RESPONSE = test_requests.TestUpdateProductVatRate.RESPONSE

    PRODUCT_IDS = ["123654", "6909316"]

    VAT_RATE = 20
    VAT_RATE_ID = VatRates.get_vat_rate_id_by_rate(VAT_RATE)

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.UpdateProductVatRate, text=self.RESPONSE)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        CCAPI.set_product_vat_rate(product_ids=self.PRODUCT_IDS, vat_rate=self.VAT_RATE)
        sent_data = self.get_sent_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data["prodids"]))

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_vat_rate(
            product_ids=self.PRODUCT_IDS[0], vat_rate=self.VAT_RATE
        )
        sent_data = self.get_sent_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data["prodids"]))

    def test_vat_rate_ID_is_sent(self):
        """Test the correct VAT rate ID is sent."""
        CCAPI.set_product_vat_rate(product_ids=self.PRODUCT_IDS, vat_rate=self.VAT_RATE)
        self.assertDataSent("vatrate", self.VAT_RATE_ID)


class Test_upload_image_Method(TestCCAPIMethod):
    """Test the CCAPI.upload_image method."""

    RESPONSE = test_requests.TestUploadImage.SUCCESSFUL_RESPONSE

    PRODUCT_IDS = ["123654", "6909316"]
    IMAGE = test_requests.TestUploadImage.IMAGE

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.UploadImage, json=self.RESPONSE)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        CCAPI.upload_image(product_ids=self.PRODUCT_IDS, image_file=self.IMAGE)
        sent_data = self.get_sent_request_query()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data["prodids"]))

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.upload_image(product_ids=self.PRODUCT_IDS, image_file=self.IMAGE)
        sent_data = self.get_sent_request_query()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data["prodids"]))


class Test_create_range_Method(TestCCAPIMethod):
    """Test the CCAPI.create_range method."""

    RANGE_ID = "4940634"
    GET_SKU_RESPONSE = test_requests.TestProductOperations.RESPONSE

    RANGE_NAME = "New Product Range"
    SKU = "JF8-98D-3KD"

    def setUp(self):
        """Register request URIs."""
        super().setUp()
        self.register_request(requests.AddNewRange, text=self.RANGE_ID)
        self.register_request(requests.ProductOperations, json=self.GET_SKU_RESPONSE)

    def test_create_range_returns_a_range_ID(self):
        """Test the CCAPI.create_range method returns a range ID."""
        response = CCAPI.create_range(self.RANGE_NAME, self.SKU)
        self.assertEqual(response, self.RANGE_ID)

    def test_create_range_sends_range_name(self):
        """Test the CCAPI.create_range method sends a range name."""
        CCAPI.create_range(self.RANGE_NAME, self.SKU)
        self.assertDataSent("RangeName", self.RANGE_NAME)

    def test_create_range_sends_SKU(self):
        """Test the CCAPI.create_range method sends a SKU."""
        CCAPI.create_range(self.RANGE_NAME, self.SKU)
        self.assertDataSent("SKUCode", self.SKU)

    def test_gets_generated_SKU(self):
        """Test a request is made for a new SKU."""
        CCAPI.create_range(self.RANGE_NAME)
        self.assertRequestUsesRequestClassURI(
            requests.ProductOperations, self.get_sent_request(skip=2)
        )

    def test_generated_SKU_is_used(self):
        """Test that the generated SKU is sent."""
        CCAPI.create_range(self.RANGE_NAME)
        self.assertDataSent("SKUCode", "RNG_" + self.GET_SKU_RESPONSE["Data"])


class Test_add_option_to_product_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.add_option_to_product method."""

    RESPONSE = test_requests.TestAddRemProductOption.RESPONSE

    RANGE_ID = "4940634"
    OPTION_ID = "32131"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.AddRemProductOption, text=self.RESPONSE)
        CCAPI.add_option_to_product(range_id=self.RANGE_ID, option_id=self.OPTION_ID)

    def test_add_option_to_product_sends_range_ID(self):
        """Test the CCAPI.add_option_to_product method sends a Range ID."""
        self.assertDataSent("prdid", self.RANGE_ID)

    def test_add_option_to_product_sends_option_ID(self):
        """Test the CCAPI.add_option_to_product method sends an option ID."""
        self.assertDataSent("optid", self.OPTION_ID)

    def test_add_option_to_product_sends_act(self):
        """Test the CCAPI.add_option_to_product method sends a correct act."""
        self.assertDataSent("act", "add")


class Test_remove_option_from_product_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.remove_option_from_product method."""

    RESPONSE = test_requests.TestAddRemProductOption.RESPONSE

    RANGE_ID = "4940634"
    OPTION_ID = "32131"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.AddRemProductOption, text=self.RESPONSE)
        CCAPI.remove_option_from_product(
            range_id=self.RANGE_ID, option_id=self.OPTION_ID
        )

    def test_remove_option_from_product_sends_range_ID(self):
        """Test the remove_option_from_product method sends a Range ID."""
        self.assertDataSent("prdid", self.RANGE_ID)

    def test_remove_option_from_product_sends_option_ID(self):
        """Test the remove_option_from_product method sends an option ID."""
        self.assertDataSent("optid", self.OPTION_ID)

    def test_remove_option_from_product_sends_act(self):
        """Test the remove_option_from_product method sends a correct act."""
        self.assertDataSent("act", "rem")


class Test_get_sales_channels_for_range_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.get_sales_channels_for_range method."""

    RESPONSE = test_data.CHECK_RANGES_ON_SALES_CHANNEL_RESULT

    RANGE_ID = "4940634"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.CheckRangesOnSalesChannel, json=self.RESPONSE)

    def test_get_sales_channels_for_range_sends_range_id(self):
        """Test the method uses the correct request class."""
        CCAPI.get_sales_channels_for_range(self.RANGE_ID)
        self.assertDataSent("rangeid", self.RANGE_ID)

    def test_get_sales_channel_for_range_returns_list(self):
        """Test the method returns a list."""
        response = CCAPI.get_sales_channels_for_range(self.RANGE_ID)
        self.assertIsInstance(response, list)

    def test_get_sales_channel_for_range_returns_sales_channels(self):
        """Test the method returns a list."""
        response = CCAPI.get_sales_channels_for_range(self.RANGE_ID)
        self.assertIsInstance(response[0], cc_objects.SalesChannel)


class Test_delete_range_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.delete_range method."""

    RESPONSE = test_requests.TestDeleteProductRange.RESPONSE

    RANGE_ID = "4940634"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.DeleteProductRange, text=self.RESPONSE)
        CCAPI.delete_range(self.RANGE_ID)

    def test_delete_range_sends_range_id(self):
        """Test the delete_range method sends the passed range ID."""
        self.assertDataSent("ProdRangeID", self.RANGE_ID)


class Test_set_range_option_drop_down_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.set_range_option_drop_down method."""

    RESPONSE = test_requests.TestSetOptionSelect.RESPONSE

    RANGE_ID = "4355752"
    OPTION_ID = "32129"
    DROP_DOWN = True

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.SetOptionSelect, text=self.RESPONSE)
        CCAPI.set_range_option_drop_down(
            range_id=self.RANGE_ID, option_id=self.OPTION_ID, drop_down=self.DROP_DOWN
        )

    def test_sends_range_ID(self):
        """Test the set_range_option_drop_down method sends a range ID."""
        self.assertDataSent("prdid", self.RANGE_ID)

    def test_sends_option_ID(self):
        """Test the set_range_option_drop_down method sends an option ID."""
        self.assertDataSent("optid", self.OPTION_ID)

    def test_sends_drop_down_status(self):
        """Test the method sends a drop down status."""
        self.assertDataSent("onoff", int(self.DROP_DOWN))


class Test_update_range_on_sales_channel_Method(TestCCAPIMethod):
    """Test the update_range_on_sales_channel method."""

    RESPONSE = []

    RANGE_ID = "4355752"
    REQUEST_TYPE = "select"
    ACT = "update"
    VALUE = "Test Value"
    OPTION_ID = "32129"
    CHANNEL_IDS = ["3541", "3557"]

    def setUp(self):
        """Register request URI and call method."""
        super().setUp()
        self.register_request(requests.UpdateRangeOnSalesChannel, json=self.RESPONSE)
        CCAPI.update_range_on_sales_channel(
            range_id=self.RANGE_ID,
            request_type=self.REQUEST_TYPE,
            act=self.ACT,
            value=self.VALUE,
            option_id=self.OPTION_ID,
            channel_ids=self.CHANNEL_IDS,
        )

    def test_update_range_on_sales_channel_method_sends_range_ID(self):
        """Test the update_range_on_sales_channel method sends a range ID."""
        self.assertDataSent("rangeid", self.RANGE_ID)

    def test_update_range_on_sales_channel_method_sends_request_type(self):
        """Test update_range_on_sales_channel method sends a request type."""
        self.assertDataSent("type", self.REQUEST_TYPE)

    def test_update_range_on_sales_channel_method_sends_act(self):
        """Test the update_range_on_sales_channel method sends an act."""
        self.assertDataSent("act", self.ACT)

    def test_update_range_on_sales_channel_method_sends_value(self):
        """Test the update_range_on_sales_channel method sends a value."""
        self.assertDataSent("val", self.VALUE)

    def test_update_range_on_sales_channel_method_sends_option_ID(self):
        """Test the update_range_on_sales_channel method sends an option ID."""
        self.assertDataSent("optid", self.OPTION_ID)

    def test_update_range_on_sales_channel_method_sends_channel_IDs(self):
        """Test the update_range_on_sales_channel method sends channel IDs."""
        self.assertDataSent("chans", self.CHANNEL_IDS)

    def test_update_range_on_sales_channel_method_sends_brand_ID(self):
        """Test the update_range_on_sales_channel method sends a brand ID."""
        self.assertDataSent("brandid", 341)


class Testupdate_range_settings_method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.update_range_settings method."""

    RESPONSE = '"OK"'

    RANGE_ID = "4355752"
    CURRENT_NAME = "Test Move Department 2"
    CURRENT_SKU = "RNG_UYV-3SP-W60"
    CURRENT_END_OF_LINE = False
    CURRENT_PRE_ORDER = False
    CURRENT_GROUP_ITEMS = False
    NEW_NAME = "Test Move Department 2"
    NEW_SKU = "RNG_UYV-3SP-W60"
    NEW_END_OF_LINE = "0"
    NEW_PRE_ORDER = False
    NEW_GROUP_ITEMS = False
    CHANNELS = ["3541", "3557"]

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.UpdateRangeSettings, text=self.RESPONSE)
        CCAPI.update_range_settings(
            range_id=self.RANGE_ID,
            current_name=self.CURRENT_NAME,
            current_sku=self.CURRENT_SKU,
            current_end_of_line=self.CURRENT_END_OF_LINE,
            current_pre_order=self.CURRENT_PRE_ORDER,
            current_group_items=self.CURRENT_GROUP_ITEMS,
            new_name=self.NEW_NAME,
            new_sku=self.NEW_SKU,
            new_end_of_line=self.NEW_END_OF_LINE,
            new_pre_order=self.NEW_PRE_ORDER,
            new_group_items=self.NEW_GROUP_ITEMS,
            channels=self.CHANNELS,
        )

    def test_update_range_settings_sends_range_id(self):
        """Test the method sends the passed range ID."""
        self.assertJsonValueSent("rangeID", self.RANGE_ID)

    def test_update_range_settings_sends_current_name(self):
        """Test the method sends the passed current name."""
        self.assertJsonValueSent("currName", self.CURRENT_NAME)

    def test_update_range_settings_sends_current_sku(self):
        """Test the method sends the passed current SKU."""
        self.assertJsonValueSent("currSKU", self.CURRENT_SKU)

    def test_update_range_settings_sends_current_end_of_line(self):
        """Test the method sends the passed current end of line."""
        self.assertJsonValueSent("currEoL", int(self.CURRENT_END_OF_LINE))

    def test_update_range_settings_sends_current_pre_order(self):
        """Test the method sends the passed current pre order."""
        self.assertJsonValueSent("currPreO", int(self.CURRENT_PRE_ORDER))

    def test_update_range_settings_sends_current_group_items(self):
        """Test the method sends the passed current group items."""
        self.assertJsonValueSent("currGBy", str(int(self.CURRENT_GROUP_ITEMS)))

    def test_update_range_settings_sends_new_name(self):
        """Test the method sends the passed new name."""
        self.assertJsonValueSent("newName", self.NEW_NAME)

    def test_update_range_settings_sends_new_sku(self):
        """Test the method sends the passed new SKU."""
        self.assertJsonValueSent("newSKU", self.NEW_SKU)

    def test_update_range_settings_sends_new_end_of_line(self):
        """Test the method sends the passed new end of line."""
        self.assertJsonValueSent("newEoL", str(int(self.NEW_END_OF_LINE)))

    def test_update_range_settings_sends_new_pre_order(self):
        """Test the method sends the passed new pre order."""
        self.assertJsonValueSent("newPreO", str(int(self.NEW_PRE_ORDER)))

    def test_update_range_settings_sends_new_group_items(self):
        """Test the method sends the passed new group items."""
        self.assertJsonValueSent("newGBy", str(int(self.NEW_GROUP_ITEMS)))

    def test_update_range_settings_sends_channels(self):
        """Test the method sends the passed channels."""
        self.assertJsonValueSent("channels", self.CHANNELS)

    def test_update_range_settings_sends_brand_id(self):
        """Test the method sends the passed brand ID."""
        self.assertJsonValueSent("brandID", 341)


class Test_add_customer_Method(TestCCAPIMethod):
    """Test the ccapi.add_customer_method."""

    CUSTOMER_ID = test_requests.test_handlers.TestAddCustomer.CUSTOMER_ID
    RESPONSE = test_requests.test_handlers.TestAddCustomer.RESPONSE

    ACCOUNT_NAME = "Account 001"
    ADDRESS_1 = "1 Way Street"
    ADDRESS_2 = "Villageton"
    AGENT_ID = 3
    COMPANY_FAX = "02135 465135"
    COMPANY_MOBILE = "09135 453 901"
    COMPANY_TELEPHONE = "132485 63156"
    CONTACT_EMAIL = "contact@nowhere.com"
    CONTACT_FAX = "15441 8464 6541"
    CONTACT_MOBILE = "09874 751 665"
    CONTACT_NAME = "Contact Test Customer"
    CONTACT_PHONE = "01324 164861"
    COUNTRY = "United Kingdom"
    COUNTY = "Townshire"
    CUSTOMER_NAME = "Test Customer"
    CUSTOMER_TYPE = 6
    EU_VAT = False
    POST_CODE = "ES23 5LN"
    PAYMENT_TERMS = 3
    SELLING_CHANNEL_ID = "3541"
    SPECIAL_INSTRUCTIONS_NOTE = "Leave packages in Porch."
    TOWN = "Townsville"
    TRADE_NAME = "Shop Co."
    VAT_NUMBER = "8759453"
    CREDIT_LIMIT = 7

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.handlers.AddCustomer, text=self.RESPONSE)
        self.returned_value = CCAPI.add_customer(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            address_2=self.ADDRESS_2,
            town=self.TOWN,
            post_code=self.POST_CODE,
            account_name=self.ACCOUNT_NAME,
            agent_id=self.AGENT_ID,
            company_fax=self.COMPANY_FAX,
            company_mobile=self.COMPANY_MOBILE,
            company_telephone=self.COMPANY_TELEPHONE,
            contact_email=self.CONTACT_EMAIL,
            contact_fax=self.CONTACT_FAX,
            contact_name=self.CONTACT_NAME,
            contact_phone=self.CONTACT_PHONE,
            contact_mobile=self.CONTACT_MOBILE,
            county=self.COUNTY,
            customer_type=self.CUSTOMER_TYPE,
            eu_vat=self.EU_VAT,
            payment_terms=self.PAYMENT_TERMS,
            trade_name=self.TRADE_NAME,
            vat_number=self.VAT_NUMBER,
            special_instructions=self.SPECIAL_INSTRUCTIONS_NOTE,
            credit_limit=self.CREDIT_LIMIT,
        )

    def test_add_customer_returns_customer_ID(self):
        """Test the add_customer method of CCAPI returns a customer ID."""
        self.assertEqual(self.returned_value, self.CUSTOMER_ID)

    def test_add_customer_sends_account_name(self):
        """Test the add_customer method sends an account name."""
        self.assertDataSent("AcctName", self.ACCOUNT_NAME)

    def test_add_customer_sends_address_1(self):
        """Test the add_customer method sends the first line of the address."""
        self.assertDataSent("addr1", self.ADDRESS_1)

    def test_add_customer_sends_address_2(self):
        """Test the add_customer method sends the second line of the address."""
        self.assertDataSent("addr2", self.ADDRESS_2)

    def test_add_customer_sends_agent_ID(self):
        """Test the add_customer method sends the agent ID."""
        self.assertDataSent("agentID", self.AGENT_ID)

    def test_add_customer_sends_company_fax(self):
        """Test the add_customer method sends the company fax."""
        self.assertDataSent("compFax", self.COMPANY_FAX)

    def test_add_customer_sends_company_mobile(self):
        """Test the add_customer method sends the company mobile."""
        self.assertDataSent("compMob", self.COMPANY_MOBILE)

    def test_add_customer_sends_company_telephone(self):
        """Test the add_customer method sends the company telephone."""
        self.assertDataSent("compTel", self.COMPANY_TELEPHONE)

    def test_add_customer_sends_contact_email(self):
        """Test the add_customer method sends the contact email."""
        self.assertDataSent("contEmail", self.CONTACT_EMAIL)

    def test_add_customer_sends_contact_fax(self):
        """Test the add_customer method sends the contact fax."""
        self.assertDataSent("contFax", self.CONTACT_FAX)

    def test_add_customer_sends_contact_mobile(self):
        """Test the add_customer method sends the contact mobile."""
        self.assertDataSent("contMob", self.CONTACT_MOBILE)

    def test_add_customer_sends_contact_name(self):
        """Test the add_customer method sends the contact name."""
        self.assertDataSent("contName", self.CONTACT_NAME)

    def test_add_customer_sends_contact_phone(self):
        """Test the add_customer method sends the contact phone."""
        self.assertDataSent("contPhone", self.CONTACT_PHONE)

    def test_add_customer_sends_country(self):
        """Test the add_customer method sends the country."""
        self.assertDataSent("country", self.COUNTRY)

    def test_add_customer_sends_county(self):
        """Test the add_customer method sends the county."""
        self.assertDataSent("county", self.COUNTY)

    def test_add_customer_sends_customer_name(self):
        """Test the add_customer method sends the customer name."""
        self.assertDataSent("CustName", self.CUSTOMER_NAME)

    def test_add_customer_sends_customer_type(self):
        """Test the add_customer method sends the customer type."""
        self.assertDataSent("CustType", self.CUSTOMER_TYPE)

    def test_add_customer_sends_EU_VAT(self):
        """Test the add_customer method sends the EU VAT."""
        self.assertDataSent("EUVAT", int(bool(self.EU_VAT)))

    def test_add_customer_sends_post_code(self):
        """Test the add_customer method sends the post code."""
        self.assertDataSent("pcode", self.POST_CODE)

    def test_add_customer_sends_payment_terms(self):
        """Test the add_customer method sends the payment terms."""
        self.assertDataSent("pterms", self.PAYMENT_TERMS)

    def test_add_customer_sends_selling_channel_ID(self):
        """Test the add_customer method sends the selling channel ID."""
        self.assertDataSent("scID", self.SELLING_CHANNEL_ID)

    def test_add_customer_sends_special_instruction_note(self):
        """Test the add_customer method sends the special instruction note."""
        self.assertDataSent("SpecInstrNote", self.SPECIAL_INSTRUCTIONS_NOTE)

    def test_add_customer_sends_town(self):
        """Test the add_customer method sends the town."""
        self.assertDataSent("town", self.TOWN)

    def test_add_customer_sends_trade_name(self):
        """Test the add_customer method sends the trade name."""
        self.assertDataSent("TradName", self.TRADE_NAME)

    def test_add_customer_sends_VAT_number(self):
        """Test the add_customer method sends the VAT number."""
        self.assertDataSent("VATNo", self.VAT_NUMBER)

    def test_add_customer_sends_credit_limit(self):
        """Test the add_customer method sends the credit_limit."""
        self.assertDataSent("CreditLimit", self.CREDIT_LIMIT)


class Test_get_payment_terms_Method(TestCCAPIMethod):
    """Test the CCAPI.get_payment_terms method."""

    RESPONSE = test_requests.test_program_type_requests.TestGetPaymentTerms.RESPONSE

    PAYMENT_TERMS = {
        "4": "Full Payment With 10% Early Payment Discount",
        "1": "Full Payment Before Dispatch",
        "7": "Direct debit",
        "39": "Cash On Delivery",
        "9": "7 Days Credit",
        "3": "60 Days Credit",
        "5": "50% Upfront Balance in 30 Days",
        "6": "30% Deposit - Balance on Delivery",
        "8": "30 Days Credit",
        "2": "28 Days Credit",
        "10": "14 Days Credit",
    }

    PROGRAM_TYPE = "GetPaymentTerms"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.program_type_requests.Customer, text=self.RESPONSE
        )
        self.returned_value = CCAPI.get_payment_terms()

    def test_get_payment_terms_sends_program_type(self):
        """Test the get_payment_terms method sends the correct program type."""
        self.assertDataSent("ProgType", self.PROGRAM_TYPE)

    def test_get_payment_terms_method_returns_payment_terms(self):
        """Test the method returns parsed payment terms."""
        self.assertEqual(self.returned_value, self.PAYMENT_TERMS)


class Test_create_payment_Method(TestCCAPIMethod):
    """Test the CCAPI.create_payment method."""

    RESPONSE = test_requests.test_accounts.TestCreatePayment.RESPONSE

    CUSTOMER_ID = "18495409"
    INVOICE_ID = "17249270"
    AMOUNT = 17.99
    LOGIN_ID = "1321483154"
    TRANSACTION_TYPE_ID = "12"
    BANK_ACCOUNT_ID = "13248121"
    PROFORMA_ID = "4513032413"
    GATEWAY_ID = "1651138443"
    CURRENCY_CODE_ID = "12"
    EXCHANGE_RATE = "1.25"
    TRANSACTION_DATE = datetime.datetime(day=1, month=1, year=1970)

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.accounts.CreatePayment, text=self.RESPONSE)
        CCAPI.create_payment(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            login_id=self.LOGIN_ID,
            transaction_type_id=self.TRANSACTION_TYPE_ID,
            bank_account_id=self.BANK_ACCOUNT_ID,
            proforma_id=self.PROFORMA_ID,
            gateway_id=self.GATEWAY_ID,
            currency_code_id=self.CURRENCY_CODE_ID,
            exchange_rate=self.EXCHANGE_RATE,
            transaction_date=self.TRANSACTION_DATE,
        )

    def test_create_payment_sends_customer_ID(self):
        """Test the create_payment method sends a customer ID."""
        self.assertDataSent(
            requests.accounts.CreatePayment.CUSTOMER_ID, self.CUSTOMER_ID
        )

    def test_create_payment_sends_invoice_ID(self):
        """Test the create_payment method sends an invoice ID."""
        self.assertDataSent(requests.accounts.CreatePayment.INVOICE_ID, self.INVOICE_ID)

    def test_create_payment_sends_amount(self):
        """Test the create_payment method sends an amount."""
        self.assertDataSent(requests.accounts.CreatePayment.AMOUNT, self.AMOUNT)

    def test_create_payment_sends_login_ID(self):
        """Test the create_payment method sends a login ID."""
        self.assertDataSent(requests.accounts.CreatePayment.LOGIN_ID, self.LOGIN_ID)

    def test_create_payment_sends_transaction_type_ID(self):
        """Test the create_payment method sends a transaction_type ID."""
        self.assertDataSent(
            requests.accounts.CreatePayment.TRANSACTION_TYPE_ID,
            self.TRANSACTION_TYPE_ID,
        )

    def test_create_payment_sends_bank_account_ID(self):
        """Test the create_payment method sends a bank account ID."""
        self.assertDataSent(
            requests.accounts.CreatePayment.BANK_ACCOUNT_ID, self.BANK_ACCOUNT_ID
        )

    def test_create_payment_sends_proforma_account_ID(self):
        """Test the create_payment method sends a bank proforma ID."""
        self.assertDataSent(
            requests.accounts.CreatePayment.PROFORMA_ID, self.PROFORMA_ID
        )

    def test_create_payment_sends_gateway_ID(self):
        """Test the create_payment method sends a gateway ID."""
        self.assertDataSent(requests.accounts.CreatePayment.GATEWAY_ID, self.GATEWAY_ID)

    def test_create_payment_sends_currency_code_ID(self):
        """Test the create_payment method sends a currency code ID."""
        self.assertDataSent(
            requests.accounts.CreatePayment.CURRENCY_CODE_ID, self.CURRENCY_CODE_ID
        )

    def test_create_payment_sends_exchange_rate(self):
        """Test the create_payment method sends an exchange rate."""
        self.assertDataSent(
            requests.accounts.CreatePayment.EXCHANGE_RATE, self.EXCHANGE_RATE
        )

    def test_create_payment_sends_transaction_type(self):
        """Test the create_payment method sends an transaction date."""
        self.assertDataSent(
            requests.accounts.CreatePayment.TRANSACTION_DATE,
            self.TRANSACTION_DATE.strftime("%d/%m/%Y"),
        )


class Test_add_address_Method(TestCCAPIMethod):
    """Test the CCAPI.add_address method."""

    NEW_ADDRESS_ID = (
        test_requests.test_program_type_requests.TestUpdateCustomerAddress.NEW_ADDRESS_ID
    )
    RESPONSE = (
        test_requests.test_program_type_requests.TestUpdateCustomerAddress.RESPONSE
    )

    CUSTOMER_ID = 18_748_142
    ADDRESS_TYPE = (
        requests.program_type_requests.customer.UpdateCustomerAddress.DELIVERY
    )
    COMPANY_NAME = "Joe's Blogs"
    FIRST_NAME = "Joe"
    LAST_NAME = "Blog"
    ADDRESS_1 = "1 The Street"
    ADDRESS_2 = "Churchford"
    POST_CODE = "L17 THX"
    TOWN = "Towningsville"
    REGION = "Southwestshire"
    COUNTRY = "United Kingdom"
    TELEPHONE_NUMBER = "04845 16815"
    FAX_NUMBER = "04813 541864"
    MOBILE_NUMBER = "07954 415 638"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.program_type_requests.customer.UpdateCustomerAddress,
            text=self.RESPONSE,
        )
        self.response = CCAPI.add_address(
            customer_id=self.CUSTOMER_ID,
            address_type=self.ADDRESS_TYPE,
            company_name=self.COMPANY_NAME,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            address_1=self.ADDRESS_1,
            address_2=self.ADDRESS_2,
            post_code=self.POST_CODE,
            town=self.TOWN,
            region=self.REGION,
            country=self.COUNTRY,
            telephone_number=self.TELEPHONE_NUMBER,
            fax_number=self.FAX_NUMBER,
            mobile_number=self.MOBILE_NUMBER,
        )

    def test_add_address_returns_address_ID(self):
        """Test the CCAPI.add_address method returns the new address ID."""
        self.assertEqual(self.response, self.NEW_ADDRESS_ID)

    def test_add_address_sends_customer_ID(self):
        """Test the CCAPI.add_address method sends a customer ID."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.CUSTOMER_ID,
            self.CUSTOMER_ID,
        )

    def test_add_address_sends_address_type(self):
        """Test the CCAPI.add_address method sends an address type."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_TYPE,
            self.ADDRESS_TYPE,
        )

    def test_add_address_sends_company_name(self):
        """Test the CCAPI.add_address method sends a company name."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.COMPANY_NAME,
            self.COMPANY_NAME,
        )

    def test_add_address_sends_first_name(self):
        """Test the CCAPI.add_address method sends a first name."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.FIRST_NAME,
            self.FIRST_NAME,
        )

    def test_add_address_sends_last_name(self):
        """Test the CCAPI.add_address method sends a last name."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.LAST_NAME,
            self.LAST_NAME,
        )

    def test_add_address_sends_address_1(self):
        """Test the CCAPI.add_address method sends a first address line."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_1,
            self.ADDRESS_1,
        )

    def test_add_address_sends_address_2(self):
        """Test the CCAPI.add_address method sends a second address line."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_2,
            self.ADDRESS_2,
        )

    def test_add_address_sends_post_code(self):
        """Test the CCAPI.add_address method sends a post code."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.POST_CODE,
            self.POST_CODE,
        )

    def test_add_address_sends_town(self):
        """Test the CCAPI.add_address method sends a town."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.TOWN,
            self.TOWN,
        )

    def test_add_address_sends_region(self):
        """Test the CCAPI.add_address method sends a region."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.REGION,
            self.REGION,
        )

    def test_add_address_sends_country(self):
        """Test the CCAPI.add_address method sends a country."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.COUNTRY,
            self.COUNTRY,
        )

    def test_add_address_sends_telephone_number(self):
        """Test the CCAPI.add_address method sends a telephone number."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.TELEPHONE_NUMBER,
            self.TELEPHONE_NUMBER,
        )

    def test_add_address_sends_fax_number(self):
        """Test the CCAPI.add_address method sends a fax number."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.FAX_NUMBER,
            self.FAX_NUMBER,
        )

    def test_add_address_sends_mobile_number(self):
        """Test the CCAPI.add_address method sends a mobile number."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.MOBILE_NUMBER,
            self.MOBILE_NUMBER,
        )


class Test_update_address_Method(TestCCAPIMethod):
    """Test the CCAPI.update_address method."""

    NEW_ADDRESS_ID = (
        test_requests.test_program_type_requests.TestUpdateCustomerAddress.NEW_ADDRESS_ID
    )
    RESPONSE = (
        test_requests.test_program_type_requests.TestUpdateCustomerAddress.RESPONSE
    )

    CUSTOMER_ID = 18_748_142
    ADDRESS_ID = 98_748_152
    ADDRESS_TYPE = (
        requests.program_type_requests.customer.UpdateCustomerAddress.DELIVERY
    )
    COMPANY_NAME = "Joe's Blogs"
    FIRST_NAME = "Joe"
    LAST_NAME = "Blog"
    ADDRESS_1 = "1 The Street"
    ADDRESS_2 = "Churchford"
    POST_CODE = "L17 THX"
    TOWN = "Towningsville"
    REGION = "Southwestshire"
    COUNTRY = "United Kingdom"
    TELEPHONE_NUMBER = "04845 16815"
    FAX_NUMBER = "04813 541864"
    MOBILE_NUMBER = "07954 415 638"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.program_type_requests.customer.UpdateCustomerAddress,
            text=self.RESPONSE,
        )
        self.response = CCAPI.update_address(
            customer_id=self.CUSTOMER_ID,
            address_id=self.ADDRESS_ID,
            address_type=self.ADDRESS_TYPE,
            company_name=self.COMPANY_NAME,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            address_1=self.ADDRESS_1,
            address_2=self.ADDRESS_2,
            post_code=self.POST_CODE,
            town=self.TOWN,
            region=self.REGION,
            country=self.COUNTRY,
            telephone_number=self.TELEPHONE_NUMBER,
            fax_number=self.FAX_NUMBER,
            mobile_number=self.MOBILE_NUMBER,
        )

    def test_update_address_returns_address_ID(self):
        """Test the CCAPI.update_address method returns the new address ID."""
        self.assertIsNone(self.response)

    def test_update_address_sends_customer_ID(self):
        """Test the CCAPI.update_address method sends a customer ID."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.CUSTOMER_ID,
            self.CUSTOMER_ID,
        )

    def test_update_address_sends_address_ID(self):
        """Test the CCAPI.update_address method sends an address ID."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_ID,
            self.ADDRESS_ID,
        )

    def test_update_address_sends_address_type(self):
        """Test the CCAPI.update_address method sends an address type."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_TYPE,
            self.ADDRESS_TYPE,
        )

    def test_update_address_sends_company_name(self):
        """Test the CCAPI.update_address method sends a company name."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.COMPANY_NAME,
            self.COMPANY_NAME,
        )

    def test_update_address_sends_first_name(self):
        """Test the CCAPI.update_address method sends a first name."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.FIRST_NAME,
            self.FIRST_NAME,
        )

    def test_update_address_sends_last_name(self):
        """Test the CCAPI.update_address method sends a last name."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.LAST_NAME,
            self.LAST_NAME,
        )

    def test_update_address_sends_address_1(self):
        """Test the CCAPI.update_address method sends a first address line."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_1,
            self.ADDRESS_1,
        )

    def test_update_address_sends_address_2(self):
        """Test the CCAPI.update_address method sends a second address line."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.ADDRESS_2,
            self.ADDRESS_2,
        )

    def test_update_address_sends_post_code(self):
        """Test the CCAPI.update_address method sends a post code."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.POST_CODE,
            self.POST_CODE,
        )

    def test_update_address_sends_town(self):
        """Test the CCAPI.update_address method sends a town."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.TOWN,
            self.TOWN,
        )

    def test_update_address_sends_region(self):
        """Test the CCAPI.update_address method sends a region."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.REGION,
            self.REGION,
        )

    def test_update_address_sends_country(self):
        """Test the CCAPI.update_address method sends a country."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.COUNTRY,
            self.COUNTRY,
        )

    def test_update_address_sends_telephone_number(self):
        """Test the CCAPI.update_address method sends a telephone number."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.TELEPHONE_NUMBER,
            self.TELEPHONE_NUMBER,
        )

    def test_update_address_sends_fax_number(self):
        """Test the CCAPI.update_address method sends a fax number."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.FAX_NUMBER,
            self.FAX_NUMBER,
        )

    def test_update_address_sends_mobile_number(self):
        """Test the CCAPI.update_address method sends a mobile number."""
        self.assertDataSent(
            requests.program_type_requests.customer.UpdateCustomerAddress.MOBILE_NUMBER,
            self.MOBILE_NUMBER,
        )


class Test_create_order_Method(TestCCAPIMethod):
    """Test the CCAPI.creat_order method."""

    RESPONSE = test_requests.test_handlers.TestCreateOrderRequest.RESPONSE

    ITEMS = [
        NewOrderItem(
            product_id=4_176_861,
            item_net=12.5,
            item_gross=15,
            total_net=12.5,
            total_gross=15,
        ),
        NewOrderItem(
            product_id=3_176_869,
            item_net=13.12,
            item_gross=19,
            total_net=22.5,
            total_gross=18,
        ),
    ]

    CUSTOMER_ID = 18_495_409
    DELIVERY_ADDRESS_ID = 134_864_315
    BILLING_ADDRESS_ID = 786_315_135
    DELIVERY_DATE = datetime.datetime.now()
    LOGIN_ID = 134_876_131
    SEASON_ID = 5
    CHANNEL_ID = 3151
    ORDER_NOTE = "Order Note text"
    SEND_EMAIL = True
    CARRIAGE_NET = 3.65
    CARRIAGE_VAT = 15.87
    TOTAL_NET = 15.84
    TOTAL_VAT = 12.80
    TOTAL_GROSS = 2.90
    DISCOUNT_NET = 1.50
    FREE_OF_CHARGE = True
    SHIPPING_RULE_ID = 487_315
    REFERENCE = "reference value"
    PREP = "prep value"
    POSTAGE_OVERRIDE = "postage override value"
    ORDER_ID = 154_313_143

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.handlers.createorder.CreateOrder, json=self.RESPONSE
        )

    def test_returns_CreateOrder_response(self):
        """Test the method returns an instance of CreateOrderResponse."""
        response = CCAPI.create_order(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
        )
        self.assertIsInstance(
            response, requests.handlers.createorder.CreateOrderResponse
        )

    def test_sends_parameters(self):
        """Test all passed parameters are sent to Cloud Commerce."""
        CCAPI.create_order(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            season_id=self.SEASON_ID,
            channel_id=self.CHANNEL_ID,
            order_note=self.ORDER_NOTE,
            send_email=self.SEND_EMAIL,
            carriage_net=self.CARRIAGE_NET,
            carriage_vat=self.CARRIAGE_VAT,
            total_net=self.TOTAL_NET,
            total_vat=self.TOTAL_VAT,
            total_gross=self.TOTAL_GROSS,
            discount_net=self.DISCOUNT_NET,
            shipping_rule_id=self.SHIPPING_RULE_ID,
        )
        """Test the method sends all passed parameters to Cloud Commerce."""
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.CUSTOMER_ID, self.CUSTOMER_ID
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.ITEMS,
            json.dumps([i.to_dict() for i in self.ITEMS]),
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.DELIVERY_ADDRESS_ID,
            self.DELIVERY_ADDRESS_ID,
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.BILLING_ADDRESS_ID,
            self.BILLING_ADDRESS_ID,
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.DELIVERY_DATE,
            self.DELIVERY_DATE.strftime("%d/%m/%Y"),
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.CHANNEL_ID, self.CHANNEL_ID
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.ORDER_NOTE, self.ORDER_NOTE
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.SEND_EMAIL, int(self.SEND_EMAIL)
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.CARRIAGE_NET, self.CARRIAGE_NET
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.CARRIAGE_VAT, self.CARRIAGE_VAT
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.TOTAL_NET, self.TOTAL_NET
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.TOTAL_VAT, self.TOTAL_VAT
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.TOTAL_GROSS, self.TOTAL_GROSS
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.DISCOUNT_NET, self.DISCOUNT_NET
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.SHIPPING_RULE_ID,
            self.SHIPPING_RULE_ID,
        )

    def test_sends_free_of_charge_for_free_orders(self):
        """Test that free of charge is sent as True if the order is free."""
        items = [
            NewOrderItem(
                product_id=4_176_861,
                item_net=0,
                item_gross=0,
                total_net=0,
                total_gross=0,
            ),
            NewOrderItem(
                product_id=3_176_869,
                item_net=0,
                item_gross=0,
                total_net=0,
                total_gross=0,
            ),
        ]
        CCAPI.create_order(
            items=items,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.FREE_OF_CHARGE, "true"
        )

    def test_sends_free_of_charge_for_non_free_orders(self):
        """Test that free of charge is sent as True if the order is not free."""
        items = [
            NewOrderItem(
                product_id=4_176_861,
                item_net=0,
                item_gross=0,
                total_net=0,
                total_gross=5,
            ),
            NewOrderItem(
                product_id=3_176_869,
                item_net=0,
                item_gross=0,
                total_net=0,
                total_gross=5,
            ),
        ]
        CCAPI.create_order(
            items=items,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.FREE_OF_CHARGE, "false"
        )

    def test_delivery_date_defaults_to_current_date(self):
        """Test that the current date is sent if None is passed for delivery_date."""
        CCAPI.create_order(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=None,
        )
        self.assertDataSent(
            requests.handlers.createorder.CreateOrder.DELIVERY_DATE,
            datetime.datetime.now().strftime("%d/%m/%Y"),
        )


class Test_customer_logs_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.customer_logs method."""

    RESPONSE = test_requests.test_customers.TestGetLogs.RESPONSE
    CUSTOMER_ID = "367033441"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.customers.GetLogs, json=self.RESPONSE)

    def test_customer_logs_return_a_list(self):
        """Test the ccapi.CCAPI.customer_logs method returns a list of logs."""
        returned_value = CCAPI.customer_logs(self.CUSTOMER_ID)
        self.assertIsInstance(returned_value, list)
        self.assertIsInstance(returned_value[0], requests.customers.getlogs.CustomerLog)


class Test_get_product_exports_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.get_product_exports method."""

    RESPONSE = test_data.GET_PRODUCT_EXPORT_UPDATE_RESPONSE

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(
            requests.exports.GetProductExportUpdate, json=self.RESPONSE
        )

    def test_get_product_exports_returns_ProductExportUpdateResponse(self):
        """Test the method returns an instance of ProductExportUpdateResponse."""
        returned_value = CCAPI.get_product_exports()
        self.assertIsInstance(returned_value, cc_objects.ProductExportUpdateResponse)


class Test_export_products_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.export_products method."""

    RESPONSE = test_requests.test_exports.TestRequestProductExport.RESPONSE

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.exports.RequestProductExport, text=self.RESPONSE)

    def test_request_product_export_returns_True(self):
        """Test export_products returns True after a successfull request."""
        returned_value = CCAPI.export_products()
        self.assertTrue(returned_value)

    def test_copy_images_parameter(self):
        """Test the copy_images parameter of export_products."""
        CCAPI.export_products(copy_images=False)
        self.assertDataSent(requests.exports.RequestProductExport.COPY, 0)


class Test_save_product_export_file_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.export_products method."""

    RESPONSE = test_requests.test_exports.TestViewFile.RESPONSE
    FILE_NAME = "ProductExport9999"

    def setUp(self):
        """Create a temporary directory for saving export files."""
        super().setUp()
        self.target_dir = Path(tempfile.mkdtemp())
        self.register_request(requests.exports.ViewFile, content=self.RESPONSE)

    def tearDown(self):
        """Remove temporary directory."""
        shutil.rmtree(self.target_dir)
        super().tearDown()

    def test_save_export_file(self):
        """Test the method saves an downloaded export file."""
        save_name = "test_file.xlsx"
        save_path = self.target_dir / save_name
        CCAPI.save_product_export_file(self.FILE_NAME, save_path)
        with open(str(save_path), "rb") as f:
            saved_content = f.read()
        self.assertEqual(saved_content, self.RESPONSE)

    def test_default_file_name(self):
        """Test that the export name is used as a file name if none is provided."""
        CCAPI.save_product_export_file(self.FILE_NAME, self.target_dir)
        with open(str(self.target_dir / self.FILE_NAME) + ".xlsx", "rb") as f:
            saved_content = f.read()
        self.assertEqual(saved_content, self.RESPONSE)


class Test_get_range_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.get_range method."""

    RESPONSE = test_data.GET_PRODUCTS_FOR_RANGE_RESPONSE
    RANGE_ID = 3_537_227

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.handlers.GetProductsForRange, json=self.RESPONSE)

    def test_range_id_is_sent(self):
        """Test that the provided range ID is sent."""
        CCAPI.get_range(self.RANGE_ID)
        self.assertDataSent(
            requests.handlers.GetProductsForRange.PRODUCT_RANGE_ID, self.RANGE_ID
        )

    def test_returns_a_product_range(self):
        """Test that the method returns an instance of cc_objects.ProductRange."""
        returned_value = CCAPI.get_range(self.RANGE_ID)
        self.assertIsInstance(returned_value, cc_objects.ProductRange)


class Test_insert_payment_Method(TestCCAPIMethod):
    """Test the ccapi.CCAPI.get_range method."""

    RESPONSE = test_requests.test_handlers.TestCustomerAccountsInsertPayment.RESPONSE

    CUSTOMER_ID = "29796764"
    LOGIN_ID = "15186"
    AMOUNT = 9.99
    PAYMENT_DATE = datetime.datetime(year=2019, month=2, day=14)
    BANK_ACCOUNT_ID = 822
    INVOICE_ID = "4156168445"
    CHANNEL_ID = "3157"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register_request(requests.handlers.CustomerAccounts, json=self.RESPONSE)

    def test_date_is_sent(self):
        """Test that the provided range ID is sent."""
        CCAPI.insert_payment(
            customer_ID=self.CUSTOMER_ID,
            login_ID=self.LOGIN_ID,
            amount=self.AMOUNT,
            bank_account_ID=self.BANK_ACCOUNT_ID,
            invoice_ID=self.INVOICE_ID,
            channel_ID=self.CHANNEL_ID,
            payment_date=self.PAYMENT_DATE,
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.PROG_TYPE,
            requests.handlers.CustomerAccounts.INSERT_PAYMENT,
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.CUSTOMER_ID, int(self.CUSTOMER_ID)
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.LOGIN_ID, int(self.LOGIN_ID)
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.CURRENCY, float(self.AMOUNT)
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.BANK_ACCOUNT_ID,
            int(self.BANK_ACCOUNT_ID),
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.INVOICE_ID, int(self.INVOICE_ID)
        )
        self.assertDataSent(
            requests.handlers.CustomerAccounts.CHANNEL_ID, int(self.CHANNEL_ID)
        )

    def test_returns_a_product_range(self):
        """Test that the method returns an instance of cc_objects.ProductRange."""
        returned_value = CCAPI.insert_payment(
            customer_ID=self.CUSTOMER_ID,
            login_ID=self.LOGIN_ID,
            amount=self.AMOUNT,
            bank_account_ID=self.BANK_ACCOUNT_ID,
            invoice_ID=self.INVOICE_ID,
            channel_ID=self.CHANNEL_ID,
            payment_date=self.PAYMENT_DATE,
        )
        self.assertTrue(returned_value)
