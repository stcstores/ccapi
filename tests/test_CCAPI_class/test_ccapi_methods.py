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

