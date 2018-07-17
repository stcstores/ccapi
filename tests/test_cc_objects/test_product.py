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
