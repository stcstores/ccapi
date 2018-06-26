"""Tests for product barcode requests."""

from ccapi.requests import products

from .test_request import TestRequest


class TestDoSearch(TestRequest):
    """Tests for doSearch requests."""

    request_class = products.DoSearch

    RESULT_ID = '4347654'
    SKU_SEARCH_TEXT = 'WUA-DU7-W6W'
    RESULT_VARIATION_ID = '6909316'
    RESULT_NAME = "Product Editor Test Variations Updated Title |  4XL"
    RESULT_THUMBNAIL = "//image.png"
    RESULT_DESCRIPTION = "<p>"

    SUCCESSFUL_RESPONSE = [
        {
            "ID": RESULT_ID,
            "variationID": RESULT_VARIATION_ID,
            "Name": RESULT_NAME,
            "SKU": SKU_SEARCH_TEXT,
            "Description": RESULT_DESCRIPTION,
            "Thumbnail": RESULT_THUMBNAIL,
        }
    ]
    EMPTY_RESPONSE = []

    def test_product_search(self):
        """Test searching for a SKU."""
        self.register(json=self.SUCCESSFUL_RESPONSE)
        response = self.mock_request(self.SKU_SEARCH_TEXT)
        self.assertEqual(response[0].id, self.RESULT_ID)
        self.assertEqual(response[0].variation_id, self.RESULT_VARIATION_ID)
        self.assertEqual(response[0].name, self.RESULT_NAME)
        self.assertEqual(response[0].sku, self.SKU_SEARCH_TEXT)
        self.assertEqual(response[0].thumbnail, self.RESULT_THUMBNAIL)

    def test_unmatched_search(self):
        """Test a search with no results."""
        self.register(json=self.EMPTY_RESPONSE)
        response = self.mock_request('This search will not match anything')
        self.assertEqual(response, [])


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
