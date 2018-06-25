"""Tests for product barcode requests."""

from ccapi.requests import productbarcode

from .test_request import TestRequest


class TestProductBarcodeInUse(TestRequest):
    """Tests for the ProductBarcodeInUse request."""

    request_class = productbarcode.ProductBarcodeInUse
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

    def test_with_unused_barcode(self):
        """Test reqeuest gives correct response for an unused barcode."""
        self.register(json=self.UNUSED_RESPONSE)
        response = self.mock_request('13245679812')
        self.assertFalse(response)

    def test_with_used_barcode(self):
        """Test reqeuest gives correct response for a used barcode."""
        self.register(json=self.USED_RESPONSE)
        response = self.mock_request('13245679812')
        self.assertTrue(response)
