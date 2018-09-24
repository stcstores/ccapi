"""Tests for product barcode requests."""

import ccapi

from .test_request import TestRequest


class TestProductBarcodeInUse(TestRequest):
    """Tests for the ProductBarcodeInUse request."""

    request_class = ccapi.requests.productbarcode.ProductBarcodeInUse
    BARCODE = "13245679812"
    UNUSED_RESPONSE = {
        "Success": False,
        "Message": "Barcode not in use",
        "RecordCount": 1,
        "Data": [],
    }
    USED_RESPONSE = {
        "Success": True,
        "Message": "Barcode not in use",
        "RecordCount": 1,
        "Data": [],
    }

    def test_ProductBarcodeInUse_request(self):
        """Test the ProductBarcodeInUse request."""
        self.register(json=self.UNUSED_RESPONSE)
        self.mock_request(self.BARCODE)
        self.assertDataSent("BarcodeNumber", self.BARCODE)

    def test_with_unused_barcode(self):
        """Test reqeuest gives correct response for an unused barcode."""
        self.register(json=self.UNUSED_RESPONSE)
        response = self.mock_request(self.BARCODE)
        self.assertFalse(response)

    def test_with_used_barcode(self):
        """Test request gives correct response for a used barcode."""
        self.register(json=self.USED_RESPONSE)
        response = self.mock_request(self.BARCODE)
        self.assertTrue(response)

    def test_raises_for_non_200(self):
        """Test request raises for non 200 response codes."""
        self.register(json=self.USED_RESPONSE, status_code=500)
        with self.assertRaises(ccapi.exceptions.CloudCommerceResponseError):
            self.mock_request(self.BARCODE)
