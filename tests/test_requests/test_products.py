"""Tests for product barcode requests."""

from ccapi.requests import products

from .test_request import TestRequest


class TestProductOperations(TestRequest):
    """Tests for the ProductOperations request."""

    request_class = products.ProductOperations

    def test_get_barcode(self):
        """Test getgeneratedsku request mode."""
        request_mode = 'getgeneratedsku'
        sku = 'VSG-H3R-G0R'
        response = {
            "Success": None,
            "Message": None,
            "RecordCount": 1,
            "Data": sku,
        }
        self.register(headers={'requestmode': request_mode}, json=response)
        response = self.mock_request(request_mode)
        self.assertEqual(response.data, sku)


class TestProductSaveBarcode(TestRequest):
    """Tests for the saveBarcode request."""

    request_class = products.SaveBarcode
    RESPONSE = '"OK"'

    def test_save_barcode(self):
        """Test the saveBarcode request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request('1321564981', '123654')
        self.assertEqual(response, self.RESPONSE)
