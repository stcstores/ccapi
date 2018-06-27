"""Tests for product barcode requests."""

from ccapi import exceptions, inventoryitems
from ccapi.requests import products

from .. import test_data
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


class TestDeleteAllProductFactoryLink(TestRequest):
    """Tests for the deleteAllProductFactoryLink request."""

    request_class = products.DeleteAllProductFactoryLink
    # TODO


class TestDeleteImage(TestRequest):
    """Tests for the deleteImage request."""

    request_class = products.DeleteImage

    # TODO


class TestDeleteProductFactoryLink(TestRequest):
    """Tests for the deleteProductFactoryLink request."""

    request_class = products.DeleteProductFactoryLink

    RESPONSE = 'Success'

    def test_delete_product_factory_link(self):
        """Test deleteProductFactoryLink request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request('3544350')
        self.assertEqual(response, self.RESPONSE)


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


class TestFindProductFactoryLinks(TestRequest):
    """Tests for the FindProductFactoryLinks request."""

    request_class = products.FindProductFactoryLinks

    PRODUCT_ID = 6909316
    LINK_ID = 3544350
    FACTORY_ID = 9946
    FACTORY_NAME = "3P Enterprise Ltd"
    PRODUCT_RANGE_ID = 4347654
    SUPPLIER_SKU = 'SKU009'

    RESPONSE = {
        "LinkID": LINK_ID,
        "OrderPrice": 0.0,
        "PricePrecision": 0.0,
        "ProductID": PRODUCT_ID,
        "FactoryID": FACTORY_ID,
        "CurrencySymbol": "",
        "FactoryName": FACTORY_NAME,
        "ProductName": "Product Editor Test Variations Updated Title",
        "ManufacturerSKU": "WUA-DU7-W6W",
        "BarCodeNumber": None,
        "Weight": 0,
        "PreOrder": 0,
        "EndOfLine": 0,
        "ProductRangeID": 4347654,
        "ProductRangeName": "Product Editor Test Variations Updated Title",
        "POType": 0,
        "Price": 0.0,
        "SupplierSKU": SUPPLIER_SKU,
    }

    def make_request(self):
        """Test requesting product factory links."""
        self.register(json=[self.RESPONSE])
        return self.mock_request(self.PRODUCT_ID)

    def test_FindProductFactoryLinks_returns_FactoryLinks(self):
        """Test the request returns an instance of FactoryLinks."""
        response = self.make_request()
        self.assertIsInstance(response, inventoryitems.FactoryLinks)

    def test_FindProductFactoryLinks_response_contains_factory_links(self):
        """Test returned object contains instances of FactoryLink."""
        response = self.make_request()
        self.assertIsInstance(response[0], inventoryitems.FactoryLink)

    def test_FindProductFactoryLinks_contains_factory_link_data(self):
        """Test the correct data is returned."""
        response = self.make_request()
        self.assertEqual(response[0].product_id, self.PRODUCT_ID)
        self.assertEqual(response[0].link_id, self.LINK_ID)
        self.assertEqual(response[0].factory_name, self.FACTORY_NAME)
        self.assertEqual(response[0].factory_id, self.FACTORY_ID)
        self.assertEqual(response[0].supplier_sku, self.SUPPLIER_SKU)

    def test_find_product_factory_links_with_no_links(self):
        """Test FindProductFactoryLinks for a product with no links."""
        self.register(json=[])
        response = self.mock_request(self.PRODUCT_ID)
        self.assertIsInstance(response, inventoryitems.FactoryLinks)
        self.assertEqual(len(response), 0)


class TestFindProductSelectedOptionsOnly(TestRequest):
    """Tests for the findProductSelectedOptionsOnly request."""

    request_class = products.FindProductSelectedOptionsOnly

    RESPONSE_DATA = test_data.FIND_PRODUCT_SELECTED_OPTIONS_ONLY_TEST_RESLULT
    NOT_FOUND_RESPONSE_DATA = {
        "StockLevel": 0,
        "FBAStockLevel": 0,
        "FBAInTransitStockLevel": 0,
        "PurchaseOrderIncomingStock": 0,
        "PurchaseOrderBuildUpStock": 0,
        "product": None,
        "options": [],
        "AutoPurchaseOrderTypeId": 0,
        "PurchaseOrderAtStockQuantity": 0,
        "PurchaseOrderMaxStock": 0,
        "PurchaseOrderStockType": 0,
        "PurchaseOrderBoxQuantity": 0,
        "ItemsInThisMultipack": [],
        "StockBreakdown": None
    }

    PRODUCT_ID = RESPONSE_DATA['product']['ID']

    def make_request(self):
        """Test the findProductSelectedOptionsOnly request."""
        self.register(json=self.RESPONSE_DATA)
        return self.mock_request(self.PRODUCT_ID)

    def test_FindProductSelectedOptionsOnly_returns_a_product(self):
        """Test the request returns and instance of a product."""
        response = self.make_request()
        self.assertIsInstance(response.product, inventoryitems.Product)
        self.assertEqual(response.product.id, self.PRODUCT_ID)

    def test_FindProductSelectedOptionsOnly_sets_product_stock_level(self):
        """Test the request sets the returned Product's stock level."""
        response = self.make_request()
        stock_level = self.RESPONSE_DATA['StockLevel']
        self.assertEqual(response.product.stock_level, stock_level)

    def test_FindProductSelectedOptionsOnly_returns_product_options(self):
        """Test the request returns the Product's Product Options."""
        response = self.make_request()
        self.assertIsInstance(
            response.options, inventoryitems.AppliedProductOptions)
        self.assertGreater(len(response.options), 0)

    def test_FindProductSelectedOptionsOnly_with_non_existant_product(self):
        """Test handling when the product does not exist."""
        self.register(json=self.NOT_FOUND_RESPONSE_DATA)
        with self.assertRaises(exceptions.ProductNotFoundError):
            self.mock_request('999999')


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


class TestSaveDescription(TestRequest):
    """Tests for the saveDescription Request."""

    request_class = products.SaveDescription

    PRODUCT_ID = '6909316'
    RESPONSE = 'ok'

    def test_set_product_description(self):
        """Test SaveDescription request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            'Product Description', product_ids=[self.PRODUCT_ID])
        request_data = self.get_last_request_query()
        self.assertEqual(request_data['prodids'], [self.PRODUCT_ID])
        self.assertEqual(response, self.RESPONSE)

    def test_set_product_description_without_list(self):
        """Test SaveDescription request."""
        self.register(text=self.RESPONSE)
        self.mock_request('Product Description', product_ids=self.PRODUCT_ID)
        request_data = self.get_last_request_query()
        self.assertEqual(request_data['prodids'], [self.PRODUCT_ID])

    def test_failed_save_product_description_raises(self):
        """Test exception is raised when product ID is invalid."""
        self.register(text='ERROR', status_code=500)
        with self.assertRaises(exceptions.DescriptionNotSavedError):
            self.mock_request(
                'Product Description', product_ids=[self.PRODUCT_ID])


class TestSaveHandlingTime(TestRequest):
    """Tests for the saveHandlingTime request."""

    request_class = products.SaveHandlingTime
    RESPONSE = 'Success'

    def test_save_handling_time(self):
        """Test the saveHandlingTime request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(product_id='6909316', handling_time=1)
        self.assertEqual(response, self.RESPONSE)


class TestSaveProductName(TestRequest):
    """Tests for the saveProductName request."""

    request_class = products.SaveProductName
    # TODO


class TestSetImageOrder(TestRequest):
    """Tests for the setImageOrder request."""

    request_class = products.SetImageOrder
    # TODO


class TestSetProductOptionValue(TestRequest):
    """Tests for the setProductOptionValue request."""

    request_class = products.SetProductOptionValue
    # TODO


class TestSetProductScope(TestRequest):
    """Tests for the setProductScope request."""

    request_class = products.SetProductScope
    # TODO


class TestUpdateOnSalesChannel(TestRequest):
    """Tests for the updateOnSalesChannel request."""

    request_class = products.UpdateProductOnSalesChannel
    # TODO


class TestUpdateProductBasePrice(TestRequest):
    """Tests for the updateProductBasePrice request."""

    request_class = products.UpdateProductBasePrice
    # TODO


class TestUpdateProductStockLevel(TestRequest):
    """Tests for the UpdateProductStockLevel."""

    request_class = products.UpdateProductStockLevel
    # TODO


class TestUpdateProductVatRate(TestRequest):
    """Tests for the updateProductVatRate request."""

    request_class = products.UpdateProductVatRate
    # TODO


class TestUploadImage(TestRequest):
    """Tests for the uploadImage request."""

    request_class = products.UploadImage
    # TODO
