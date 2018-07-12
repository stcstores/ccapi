"""Tests for CCAPI's methods."""

from ccapi import CCAPI, VatRates, requests

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
