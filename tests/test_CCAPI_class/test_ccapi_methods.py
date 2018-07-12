"""Tests for CCAPI's methods."""

from ccapi import CCAPI, VatRates, inventoryitems, requests

from .. import test_data
from ..test_requests import test_products
from .test_CCAPI_class import TestCCAPI


class Test_get_sku_Method(TestCCAPI):
    """Test the get_sku method of CCAPI."""

    SKU = test_products.TestProductOperations.SKU
    RESPONSE = test_products.TestProductOperations.RESPONSE

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
    CREATED_PRODUCT_ID = test_products.TestAddProduct.CREATED_PRODUCT_ID
    SUCCESSFUL_RESPONSE = test_products.TestAddProduct.SUCCESSFUL_RESPONSE
    FAILED_RESPONSE = test_products.TestAddProduct.FAILED_RESPONSE

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

    RESPONSE = test_products.TestDeleteAllProductFactoryLink.RESPONSE
    FACTORY_ID = '11782'

    def test_delete_product_factory_links(self):
        """Test the CCAPI.delete_product_factory_links method."""
        self.register_request(
            requests.DeleteAllProductFactoryLink, text=self.RESPONSE)
        CCAPI.delete_product_factory_links(self.FACTORY_ID)
        self.assertDataSent('FactoryID', self.FACTORY_ID)


class Test_delete_image_Method(TestCCAPI):
    """Test the CCAPI.delete_image method."""

    IMAGE_ID = '28173405'
    RESPONSE = test_products.TestDeleteImage.RESPONSE

    def test_delete_image(self):
        """Test the CCAPI.delete_image method."""
        self.register_request(requests.DeleteImage, text=self.RESPONSE)
        CCAPI.delete_image(self.IMAGE_ID)
        self.assertDataSent('imgID', self.IMAGE_ID)


class Test_delete_product_facotry_link_Method(TestCCAPI):
    """Test the CCAPI.delete_product_factory_link method."""

    FACTORY_ID = '3544350'
    RESPONSE = test_products.TestDeleteProductFactoryLink.RESPONSE

    def test_delete_product_factory_links_method(self):
        """Test the CCAPI.delete_product_factory_link method."""
        self.register_request(
            requests.DeleteProductFactoryLink, text=self.RESPONSE)
        CCAPI.delete_product_factory_link(self.FACTORY_ID)
        self.assertDataSent('factoryLinkId', self.FACTORY_ID)


class Test_search_products_Method(TestCCAPI):
    """Test the CCAPI.search_products method."""

    RESPONSE = test_products.TestDoSearch.SUCCESSFUL_RESPONSE
    SEARCH_TEXT = 'WUA-DU7-W6W'

    def test_search_products_method(self):
        """Test the CCAPI.search_products method."""
        self.register_request(requests.DoSearch, json=self.RESPONSE)
        products = CCAPI.search_products(self.SEARCH_TEXT)
        self.assertDataSent('text', self.SEARCH_TEXT)
        self.assertIsInstance(products, list)
        self.assertTrue(hasattr(products[0], 'id'))
        self.assertTrue(hasattr(products[0], 'variation_id'))
        self.assertTrue(hasattr(products[0], 'name'))
        self.assertTrue(hasattr(products[0], 'sku'))
        self.assertTrue(hasattr(products[0], 'thumbnail'))


class Test_get_product_factory_links_Method(TestCCAPI):
    """Test the CCAPI.get_product_factory_links method."""

    PRODUCT_ID = 6909316
    RESPONSE = [test_products.TestFindProductFactoryLinks.RESPONSE]

    def test_get_factory_links_method(self):
        """Test the CCAPI.get_product_factory_links method."""
        self.register_request(
            requests.FindProductFactoryLinks, json=self.RESPONSE)
        factories = CCAPI.get_product_factory_links(self.PRODUCT_ID)
        self.assertDataSent('ProductID', self.PRODUCT_ID)
        self.assertIsInstance(factories, inventoryitems.FactoryLinks)


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
