"""Tests for product barcode requests."""

from ccapi import exceptions, inventoryitems
from ccapi.requests import products

from .test_request import TestRequest


class TestAddProduct(TestRequest):
    """Tests for the AddProduct request."""

    request_class = products.AddProduct

    REQUEST_KWARGS = {
        'range_id': '4347654',
        'name': 'Product Name',
        'barcode': '12345678912',
        'sku': 'WUA-DU7-W6W',
        'description': 'Product Description',
        'vat_rate_id': 20,
    }

    CREATED_PRODUCT_ID = '7286732'
    SUCCESSFUL_RESPONSE = 'Success^^{}'.format(CREATED_PRODUCT_ID)
    FAILED_RESPONSE = 'SubmitFailed^^0^^Insert'

    def test_add_product(self):
        """Test the AddProduct request."""
        self.register(text=self.SUCCESSFUL_RESPONSE)
        response = self.mock_request(**self.REQUEST_KWARGS)
        self.assertEqual(response, self.CREATED_PRODUCT_ID)

    def test_failed_add_product(self):
        """Test an AddProduct request with an invalid range ID."""
        self.register(text=self.FAILED_RESPONSE)
        with self.assertRaises(exceptions.ProductNotCreatedError):
            self.mock_request(**self.REQUEST_KWARGS)


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


class TestDeleteProductFactoryLink(TestRequest):
    """Tests for the deleteProductFactoryLink request."""

    request_class = products.DeleteProductFactoryLink

    RESPONSE = 'Success'

    def test_delete_product_factory_link(self):
        """Test deleteProductFactoryLink request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request('3544350')
        self.assertEqual(response, self.RESPONSE)


class TestFindProductFactoryLinks(TestRequest):
    """Tests for the FindProductFactoryLinks request."""

    request_class = products.FindProductFactoryLinks

    PRODUCT_ID = 6909316
    LINK_ID = 3544350
    ORDER_PRICE = 0.0
    PRICE_PRECISION = 0.0
    FACTORY_ID = 9946
    FACTORY_NAME = "3P Enterprise Ltd"
    PRODUCT_NAME = "Product Editor Test Variations Updated Title"
    PRODUCT_RANGE_ID = 4347654
    PRODUCT_RANGE_NAME = "Product Editor Test Variations Updated Title"
    PRICE = 0.0
    SUPPLIER_SKU = 'SKU009'

    RESPONSE = {
        "LinkID": LINK_ID,
        "OrderPrice": 0.0,
        "PricePrecision": 0.0,
        "ProductID": PRODUCT_ID,
        "FactoryID": FACTORY_ID,
        "CurrencySymbol": "",
        "FactoryName": FACTORY_NAME,
        "ProductName": PRODUCT_NAME,
        "ManufacturerSKU": "WUA-DU7-W6W",
        "BarCodeNumber": None,
        "Weight": 0,
        "PreOrder": 0,
        "EndOfLine": 0,
        "ProductRangeID": PRODUCT_RANGE_ID,
        "ProductRangeName": PRODUCT_RANGE_NAME,
        "POType": 0,
        "Price": 0.0,
        "SupplierSKU": SUPPLIER_SKU,
    }

    def test_find_product_factory_links(self):
        """Test requesting product factory links."""
        self.register(json=[self.RESPONSE])
        response = self.mock_request(self.PRODUCT_ID)
        self.assertIsInstance(response, inventoryitems.FactoryLinks)
        self.assertIsInstance(response[0], inventoryitems.FactoryLink)
        self.assertEqual(response[0].product_id, self.PRODUCT_ID)
        self.assertEqual(response[0].link_id, self.LINK_ID)
        self.assertEqual(response[0].order_price, self.ORDER_PRICE)
        self.assertEqual(response[0].price_precision, self.PRICE_PRECISION)
        self.assertEqual(response[0].factory_name, self.FACTORY_NAME)
        self.assertEqual(response[0].factory_id, self.FACTORY_ID)
        self.assertEqual(response[0].product_name, self.PRODUCT_NAME)
        self.assertEqual(response[0].product_range_id, self.PRODUCT_RANGE_ID)
        self.assertEqual(
            response[0].product_range_name, self.PRODUCT_RANGE_NAME)
        self.assertEqual(response[0].price, self.PRICE)
        self.assertEqual(response[0].supplier_sku, self.SUPPLIER_SKU)

    def test_find_product_factory_links_with_no_links(self):
        """Test FindProductFactoryLinks for a product with n o links."""
        self.register(json=[])
        response = self.mock_request(self.PRODUCT_ID)
        self.assertIsInstance(response, inventoryitems.FactoryLinks)
        self.assertEqual(len(response), 0)


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
