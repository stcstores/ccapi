"""Tests for product barcode requests."""

from ccapi.requests import productbarcode

from .test_request import TestRequest


class TestProductBarcodeInUse(TestRequest):
    """Tests for the ProductBarcodeInUse request."""

    request_class = productbarcode.ProductBarcodeInUse
    BARCODE = '13245679812'
    UNUSED_RESPONSE = {
        'Success': False,
        'Message': 'Barcode not in use',
        'RecordCount': 1,
        'Data': [],
    }
    USED_RESPONSE = {
        'Success': True,
        'Message': 'Barcode not in use',
        'RecordCount': 1,
        'Data': [],
    }

    def test_ProductBarcodeInUse_request(self):
        """Test the ProductBarcodeInUse request."""
        self.register(json=self.UNUSED_RESPONSE)
        self.mock_request(self.BARCODE)
        self.assertDataSent('BarcodeNumber', self.BARCODE)

    def test_with_unused_barcode(self):
        """Test reqeuest gives correct response for an unused barcode."""
        self.register(json=self.UNUSED_RESPONSE)
        response = self.mock_request(self.BARCODE)
        self.assertFalse(response)

    def test_with_used_barcode(self):
        """Test reqeuest gives correct response for a used barcode."""
        self.register(json=self.USED_RESPONSE)
        response = self.mock_request(self.BARCODE)
        self.assertTrue(response)
