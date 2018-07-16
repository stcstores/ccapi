"""Tests for CCAPI's methods."""

from ccapi import CCAPI, VatRates, inventoryitems, requests

from .. import test_data, test_requests
from .test_CCAPI_class import TestCCAPI


class Test_get_sku_Method(TestCCAPI):
    """Test the get_sku method of CCAPI."""

    SKU = test_requests.TestProductOperations.SKU
    RESPONSE = test_requests.TestProductOperations.RESPONSE

    def test_get_sku(self):
        """Test the get_sku method of CCAPI."""
        self.register_request(requests.ProductOperations, json=self.RESPONSE)
        self.assertEqual(CCAPI.get_sku(), self.SKU)

    def test_get_range_sku(self):
        """Test the get_sku method of CCAPI."""
        self.register_request(requests.ProductOperations, json=self.RESPONSE)
        self.assertEqual(CCAPI.get_sku(range_sku=True), 'RNG_' + self.SKU)


class Test_create_product_Method(TestCCAPI):
    """Test the create_product method of CCAPI."""

    REQUEST_KWARGS = {
        'range_id': '4347654',
        'name': 'Product Name',
        'barcode': '12345678912',
        'sku': 'WUA-DU7-W6W',
        'description': 'Product Description',
        'vat_rate': 20,
    }
    CREATED_PRODUCT_ID = test_requests.TestAddProduct.CREATED_PRODUCT_ID
    SUCCESSFUL_RESPONSE = test_requests.TestAddProduct.SUCCESSFUL_RESPONSE
    FAILED_RESPONSE = test_requests.TestAddProduct.FAILED_RESPONSE

    def test_create_product(self):
        """Test CCAPI can add a product to a range."""
        self.register_request(
            requests.AddProduct, text=self.SUCCESSFUL_RESPONSE)
        CCAPI.create_product(
            range_id=self.REQUEST_KWARGS['range_id'],
            name=self.REQUEST_KWARGS['name'],
            barcode=self.REQUEST_KWARGS['barcode'],
            sku=self.REQUEST_KWARGS['sku'],
            description=self.REQUEST_KWARGS['description'],
            vat_rate=20)
        self.assertDataSent('ProdRangeID', self.REQUEST_KWARGS['range_id'])
        self.assertDataSent('ProdName', self.REQUEST_KWARGS['name'])
        self.assertDataSent('BarCode', self.REQUEST_KWARGS['barcode'])
        self.assertDataSent('SKUCode', self.REQUEST_KWARGS['sku'])
        self.assertDataSent(
            'ProdDescription', self.REQUEST_KWARGS['description'])
        self.assertDataSent(
            'VatRateID',
            VatRates.get_vat_rate_id_by_rate(self.REQUEST_KWARGS['vat_rate']))

    def test_create_product_without_sku(self):
        """Test create_product generates a SKU."""
        self.register_request(
            requests.AddProduct, text=self.SUCCESSFUL_RESPONSE)
        self.register_request(
            requests.ProductOperations, json=Test_get_sku_Method.RESPONSE)
        CCAPI.create_product(
            range_id=self.REQUEST_KWARGS['range_id'],
            name=self.REQUEST_KWARGS['name'],
            barcode=self.REQUEST_KWARGS['barcode'],
            sku=None,
            description=self.REQUEST_KWARGS['description'],
            vat_rate=20)
        self.assertDataSent('SKUCode', Test_get_sku_Method.SKU)

    def test_create_product_without_description(self):
        """Test create_product handles description not being passed."""
        self.register_request(
            requests.AddProduct, text=self.SUCCESSFUL_RESPONSE)
        CCAPI.create_product(
            range_id=self.REQUEST_KWARGS['range_id'],
            name=self.REQUEST_KWARGS['name'],
            barcode=self.REQUEST_KWARGS['barcode'],
            sku=self.REQUEST_KWARGS['sku'],
            description=None,
            vat_rate=20)
        self.assertDataSent('ProdDescription', self.REQUEST_KWARGS['name'])


class Test_delete_product_factory_links_Method(TestCCAPI):
    """Test the CCAPI.delete_product_factory_links method."""

    RESPONSE = test_requests.TestDeleteAllProductFactoryLink.RESPONSE
    FACTORY_ID = '11782'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.DeleteAllProductFactoryLink, text=self.RESPONSE)
        CCAPI.delete_product_factory_links(self.FACTORY_ID)

    def test_sends_correct_factory_ID(self):
        """Test the correct factory ID is sent."""
        self.assertDataSent('FactoryID', self.FACTORY_ID)


class Test_delete_image_Method(TestCCAPI):
    """Test the CCAPI.delete_image method."""

    IMAGE_ID = '28173405'
    RESPONSE = test_requests.TestDeleteImage.RESPONSE

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.DeleteImage, text=self.RESPONSE)
        CCAPI.delete_image(self.IMAGE_ID)

    def test_sends_passed_image_ID(self):
        """Test the correct image ID is sent."""
        self.assertDataSent('imgID', self.IMAGE_ID)


class Test_delete_product_facotry_link_Method(TestCCAPI):
    """Test the CCAPI.delete_product_factory_link method."""

    FACTORY_ID = '3544350'
    RESPONSE = test_requests.TestDeleteProductFactoryLink.RESPONSE

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.DeleteProductFactoryLink, text=self.RESPONSE)
        CCAPI.delete_product_factory_link(self.FACTORY_ID)

    def test_sends_passed_factory_ID(self):
        """Test the passed factory ID is sent."""
        self.assertDataSent('factoryLinkId', self.FACTORY_ID)


class Test_search_products_Method(TestCCAPI):
    """Test the CCAPI.search_products method."""

    RESPONSE = test_requests.TestDoSearch.SUCCESSFUL_RESPONSE
    SEARCH_TEXT = 'WUA-DU7-W6W'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.DoSearch, json=self.RESPONSE)
        self.products = CCAPI.search_products(self.SEARCH_TEXT)

    def test_sends_correct_product_ID(self):
        """Test sends the correct productID."""
        self.assertDataSent('text', self.SEARCH_TEXT)

    def test_returns_list(self):
        """Test returns a list instance."""
        self.assertIsInstance(self.products, list)

    def test_search_result(self):
        """Test returned list contains object with the correct attributes."""
        self.assertTrue(hasattr(self.products[0], 'id'))
        self.assertTrue(hasattr(self.products[0], 'variation_id'))
        self.assertTrue(hasattr(self.products[0], 'name'))
        self.assertTrue(hasattr(self.products[0], 'sku'))
        self.assertTrue(hasattr(self.products[0], 'thumbnail'))


class Test_get_product_factory_links_Method(TestCCAPI):
    """Test the CCAPI.get_product_factory_links method."""

    PRODUCT_ID = 6909316
    RESPONSE = [test_requests.TestFindProductFactoryLinks.RESPONSE]

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.FindProductFactoryLinks, json=self.RESPONSE)
        self.factories = CCAPI.get_product_factory_links(self.PRODUCT_ID)

    def test_sends_passed_product_ID(self):
        """Test sends the passed product ID."""
        self.assertDataSent('ProductID', self.PRODUCT_ID)

    def test_returns_FactoryLinks_instance(self):
        """Test returns FactoryLinks instance."""
        self.assertIsInstance(self.factories, inventoryitems.FactoryLinks)


class Test_get_product_Method(TestCCAPI):
    """Test the CCAPI.get_product method."""

    PRODUCT_ID = 6909316
    RESPONSE = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.FindProductSelectedOptionsOnly, json=self.RESPONSE)
        self.product = CCAPI.get_product(self.PRODUCT_ID)

    def test_get_product_sends_correct_product_ID(self):
        """Test CCAPI.get_product sends the passed product ID ."""
        self.assertIsInstance(self.product, inventoryitems.Product)

    def test_get_product_returns_a_product(self):
        """Test CCAPI.get_product returns an inventoryitems.Product."""
        self.assertDataSent('ProductID', self.PRODUCT_ID)


class Test_get_options_for_product_Method(TestCCAPI):
    """Test the CCAPI.get_options_for_product method."""

    PRODUCT_ID = 6909316
    RESPONSE = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.FindProductSelectedOptionsOnly, json=self.RESPONSE)
        self.product = CCAPI.get_options_for_product(self.PRODUCT_ID)

    def test_get_product_sends_correct_product_ID(self):
        """Test CCAPI.get_product sends the passed product ID ."""
        self.assertIsInstance(self.product, inventoryitems.ProductOptions)

    def test_get_product_returns_a_product(self):
        """Test CCAPI.get_product returns an inventoryitems.Product."""
        self.assertDataSent('ProductID', self.PRODUCT_ID)


class Test_barcode_is_in_use_Method(TestCCAPI):
    """Test the CCAPI.barcode_is_in_use method."""

    RESPONSE = test_requests.TestProductBarcodeInUse.UNUSED_RESPONSE
    BARCODE = '1321564981'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.ProductBarcodeInUse, json=self.RESPONSE)
        self.barcode_used = CCAPI.barcode_is_in_use(barcode=self.BARCODE)

    def test_passed_barcode_is_sent(self):
        """Test the correct barcode is sent."""
        self.assertDataSent('BarcodeNumber', self.BARCODE)

    def test_bool_is_returned(self):
        """Test that the method returns a boolean."""
        self.assertIsInstance(self.barcode_used, bool)


class Test_set_product_barcode_Method(TestCCAPI):
    """Test the CCAPI.set_product_barcode method."""

    BARCODE_USED_RESPONSE = test_requests.TestProductBarcodeInUse.USED_RESPONSE
    BARCODE_UNUSED_RESPONSE = (
        test_requests.TestProductBarcodeInUse.UNUSED_RESPONSE)
    RESPONSE = test_requests.TestSaveBarcode.RESPONSE
    BARCODE = '1321564981'
    PRODUCT_ID = '123654'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.ProductBarcodeInUse, json=self.BARCODE_UNUSED_RESPONSE)
        self.register_request(requests.SaveBarcode, text=self.RESPONSE)
        CCAPI.set_product_barcode(
            barcode=self.BARCODE, product_id=self.PRODUCT_ID)

    def test_passed_barcode_is_sent(self):
        """Test the correct barcode is sent."""
        self.assertDataSent('bcode', self.BARCODE)

    def test_passed_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent('prodid', self.PRODUCT_ID)

    def test_raises_for_used_barcode(self):
        """Test exception is raised if barcode is in use."""
        self.register_request(
            requests.ProductBarcodeInUse, json=self.BARCODE_USED_RESPONSE)
        with self.assertRaises(Exception):
            CCAPI.set_product_barcode(
                barcode=self.BARCODE, product_id=self.PRODUCT_ID)


class Test_set_product_description_Method(TestCCAPI):
    """Test the CCAPI.set_product_description method."""

    RESPONSE = test_requests.TestSaveDescription.RESPONSE
    PRODUCT_IDS = ['123654', '6909316']
    DESCRIPTION = 'A description of a product\n'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SaveDescription, text=self.RESPONSE)
        CCAPI.set_product_description(
            product_ids=[self.PRODUCT_IDS], description=self.DESCRIPTION)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        sent_data = self.get_last_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data['prodids']))

    def test_passed_description_is_sent(self):
        """Test that the passed description is sent."""
        self.assertDataSent('desc', self.DESCRIPTION)

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_description(
            product_ids=self.PRODUCT_IDS[0], description=self.DESCRIPTION)
        sent_data = self.get_last_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data['prodids']))


class Test_set_product_handling_time_Method(TestCCAPI):
    """Test the CCAPI.set_product_handling_time method."""

    RESPONSE = test_requests.TestSaveHandlingTime.RESPONSE
    PRODUCT_ID = '6909316'
    HANDLING_TIME = 1

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SaveHandlingTime, text=self.RESPONSE)
        CCAPI.set_product_handling_time(
            product_id=self.PRODUCT_ID, handling_time=self.HANDLING_TIME)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product ID is sent."""
        self.assertDataSent('ProductID', self.PRODUCT_ID)

    def test_passed_handling_time_is_sent(self):
        """Test that the passed handling_time is sent."""
        self.assertDataSent('handlingTime', self.HANDLING_TIME)


class Test_set_product_name_Method(TestCCAPI):
    """Test the CCAPI.set_product_name method."""

    RESPONSE = test_requests.TestSaveProductName.RESPONSE
    PRODUCT_IDS = ['123654', '6909316']
    NAME = 'Product Name'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SaveProductName, text=self.RESPONSE)
        CCAPI.set_product_name(product_ids=[self.PRODUCT_IDS], name=self.NAME)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        sent_data = self.get_last_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data['prodids']))

    def test_passed_description_is_sent(self):
        """Test that the passed name is sent."""
        self.assertDataSent('name', self.NAME)

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_name(product_ids=self.PRODUCT_IDS[0], name=self.NAME)
        sent_data = self.get_last_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data['prodids']))


class Test_set_image_order_Method(TestCCAPI):
    """Test the CCAPI.set_image_order method."""

    RESPONSE = test_requests.TestSetImageOrder.RESPONSE
    IMAGE_IDS = ['28179547', '28179563', '28179581']
    PRODUCT_ID = '6909316'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SetImageOrder, text=self.RESPONSE)
        CCAPI.set_image_order(
            product_id=self.PRODUCT_ID, image_ids=self.IMAGE_IDS)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product ID is sent."""
        self.assertDataSent('prodid', self.PRODUCT_ID)

    def test_passed_handling_time_is_sent(self):
        """Test that the passed image IDs are sent."""
        self.assertDataSent('order', '^^'.join(self.IMAGE_IDS))


class Test_set_product_option_value_Method(TestCCAPI):
    """Test the CCAPI.set_product_option_value method."""

    RESPONSE = test_requests.TestSetProductOptionValue.RESPONSE
    PRODUCT_IDS = ['123654', '6909316']
    OPTION_ID = '32131'
    OPTION_VALUE_ID = '3040649'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.SetProductOptionValue, text=self.RESPONSE)
        CCAPI.set_product_option_value(
            product_ids=self.PRODUCT_IDS,
            option_id=self.OPTION_ID,
            option_value_id=self.OPTION_VALUE_ID)

    def test_passed_product_ID_is_sent(self):
        """Test that the passed product IDs are sent."""
        sent_data = self.get_last_request_data()
        for product_id in self.PRODUCT_IDS:
            self.assertIn(product_id, str(sent_data['prodids']))

    def test_passed_option_ID_is_sent(self):
        """Test that the passed option ID is sent."""
        self.assertDataSent('OptionID', self.OPTION_ID)

    def test_passed_option_value_is_sent(self):
        """Test that the passed option value is sent."""
        self.assertDataSent('OptionValueID', self.OPTION_VALUE_ID)

    def test_passing_single_product_ID_as_string(self):
        """Test passing a single product ID as a string."""
        CCAPI.set_product_option_value(
            product_ids=self.PRODUCT_IDS[0],
            option_id=self.OPTION_ID,
            option_value_id=self.OPTION_VALUE_ID)
        sent_data = self.get_last_request_data()
        self.assertIn(self.PRODUCT_IDS[0], str(sent_data['prodids']))


class Test_set_product_scope_Method(TestCCAPI):
    """Test the CCAPI.set_product_scope method."""

    RESPONSE = test_requests.TestSetProductScope.RESPONSE

    PRODUCT_ID = '6909316'
    WEIGHT = 50
    HEIGHT = 25
    LENGTH = 75
    WIDTH = 90
    LARGE_LETTER_COMPATIBLE = False
    EXTERNAL_ID = '165481035'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(requests.SetProductScope, text=self.RESPONSE)

    def test_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent('ProductID', self.PRODUCT_ID)

    def test_weight_is_sent(self):
        """Test the passed weight is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent('Weight', self.WEIGHT)

    def test_height_is_sent(self):
        """Test the passed height is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent('Height', self.HEIGHT)

    def test_length_is_sent(self):
        """Test the passed length is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent('Length', self.LENGTH)

    def test_width_is_sent(self):
        """Test the passed width is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent('Width', self.WIDTH)

    def test_large_letter_compatible_is_sent(self):
        """Test the passed large letter compatibilty is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=self.WEIGHT,
            height=self.HEIGHT,
            length=self.LENGTH,
            width=self.WIDTH,
            large_letter_compatible=self.LARGE_LETTER_COMPATIBLE,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent(
            'LargeLetterCompatible', int(self.LARGE_LETTER_COMPATIBLE))

    def test_external_ID_is_sent(self):
        """Test the passed external ID is sent."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=50,
            height=25,
            length=75,
            width=90,
            large_letter_compatible=False,
            external_id=self.EXTERNAL_ID)
        self.assertDataSent('ExternalID', self.EXTERNAL_ID)

    def test_external_ID_None(self):
        """Test no external ID is sent when None is passed."""
        CCAPI.set_product_scope(
            product_id=self.PRODUCT_ID,
            weight=50,
            height=25,
            length=75,
            width=90,
            large_letter_compatible=False,
            external_id=None)
        self.assertDataValueIsNone('ExternalID')


class Test_set_product_base_price_Method(TestCCAPI):
    """Test the CCAPI.set_product_base_price method."""

    RESPONSE = test_requests.TestUpdateProductBasePrice.RESPONSE

    PRODUCT_ID = '6909316'
    PRICE = '6.25'

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.UpdateProductBasePrice, text=self.RESPONSE)
        CCAPI.set_product_base_price(
            product_id=self.PRODUCT_ID, price=self.PRICE)

    def test_passed_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent('prodid', self.PRODUCT_ID)

    def test_passed_price_is_sent(self):
        """Test the passed price is sent."""
        self.assertDataSent('price', self.PRICE)


class Test_update_product_stock_level_Method(TestCCAPI):
    """Test the CCAPI.update_product_stock_level method."""

    RESPONSE = test_requests.TestUpdateProductStockLevel.RESPONSE

    PRODUCT_ID = '6909316'
    NEW_STOCK_LEVEL = 5
    OLD_STOCK_LEVEL = 10

    def setUp(self):
        """Make test request."""
        super().setUp()
        self.register_request(
            requests.UpdateProductStockLevel, text=self.RESPONSE)
        CCAPI.update_product_stock_level(
            product_id=self.PRODUCT_ID,
            new_stock_level=self.NEW_STOCK_LEVEL,
            old_stock_level=self.OLD_STOCK_LEVEL)

    def test_passed_product_ID_is_sent(self):
        """Test the passed product ID is sent."""
        self.assertDataSent('ProductID', self.PRODUCT_ID)

    def test_passed_new_stock_level_is_sent(self):
        """Test the passed new stock level is sent."""
        self.assertDataSent('newStockLevel', self.NEW_STOCK_LEVEL)

    def test_passed_old_stock_level_is_sent(self):
        """Test the passed old stock level is sent."""
        self.assertDataSent('oldStockLevel', self.OLD_STOCK_LEVEL)
