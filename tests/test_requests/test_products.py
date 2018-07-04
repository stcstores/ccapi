"""Tests for product barcode requests."""

import os

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

    def test_AddProduct_request(self):
        """Test the AddProduct request."""
        self.register(text=self.SUCCESSFUL_RESPONSE)
        response = self.mock_request(**self.REQUEST_KWARGS)
        self.assertEqual(response, self.CREATED_PRODUCT_ID)
        self.assertDataSent('ProductID', '0')
        self.assertDataSent('ProdRangeID', self.REQUEST_KWARGS['range_id'])
        self.assertDataSent('ProdName', self.REQUEST_KWARGS['name'])
        self.assertDataSent('BarCode', self.REQUEST_KWARGS['barcode'])
        self.assertDataSent('SKUCode', self.REQUEST_KWARGS['sku'])
        self.assertDataSent(
            'ProdDescription', self.REQUEST_KWARGS['description'])
        self.assertDataSent('VatRateID', self.REQUEST_KWARGS['vat_rate_id'])
        self.assertDataSent('CopyDesc', '0')
        self.assertDataSent('BrandID', '341')

    def test_failed_AddProduct_request(self):
        """Test an AddProduct request with an invalid range ID."""
        self.register(text=self.FAILED_RESPONSE)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(**self.REQUEST_KWARGS)

    def test_AddProduct_raises_for_non_200(self):
        """Test AddProduct request raises for non 200 response."""
        self.register(text=self.SUCCESSFUL_RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(**self.REQUEST_KWARGS)


class TestDeleteAllProductFactoryLink(TestRequest):
    """Tests for the deleteAllProductFactoryLink request."""

    request_class = products.DeleteAllProductFactoryLink

    FACTORY_ID = '11782'
    RESPONSE = 'Success'

    def test_DeleteAllProductFactoryLink_request(self):
        """Test the DeleteAllProductFactoryLink request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(self.FACTORY_ID)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('FactoryID', self.FACTORY_ID)
        self.assertDataSent('cornerloader', 'True')

    def test_DeleteAllProductFactoryLink_request_raises_for_non_200(self):
        """Test the DeleteAllProductFactoryLink request raises for non 200."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.FACTORY_ID)


class TestDeleteImage(TestRequest):
    """Tests for the deleteImage request."""

    request_class = products.DeleteImage

    IMAGE_ID = '28173405'
    RESPONSE = 'Success'

    def test_DeleteImage_request(self):
        """Test the DeleteImage request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(self.IMAGE_ID)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('imgID', self.IMAGE_ID)

    def test_DeleteImage_raises_for_non_200(self):
        """Test AddProduct request raises for non 200 response."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.IMAGE_ID)


class TestDeleteProductFactoryLink(TestRequest):
    """Tests for the deleteProductFactoryLink request."""

    request_class = products.DeleteProductFactoryLink

    RESPONSE = 'Success'
    FACTORY_ID = '3544350'

    def test_DeleteProductFactoryLink_request(self):
        """Test deleteProductFactoryLink request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(self.FACTORY_ID)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('factoryLinkId', self.FACTORY_ID)

    def test_DeleteProductFactoryLink_raises_for_non_200(self):
        """Test DeleteProductFactoryLink raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.FACTORY_ID)


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

    def test_DoSearch_request(self):
        """Test searching for a SKU."""
        self.register(json=self.SUCCESSFUL_RESPONSE)
        response = self.mock_request(self.SKU_SEARCH_TEXT)
        self.assertEqual(response[0].id, self.RESULT_ID)
        self.assertEqual(response[0].variation_id, self.RESULT_VARIATION_ID)
        self.assertEqual(response[0].name, self.RESULT_NAME)
        self.assertEqual(response[0].sku, self.SKU_SEARCH_TEXT)
        self.assertEqual(response[0].thumbnail, self.RESULT_THUMBNAIL)
        self.assertDataSent('text', self.SKU_SEARCH_TEXT)
        self.assertDataSent('type', 'range')
        self.assertDataSent('brandid', '341')

    def test_doSearch_raises_for_non_200unmatched_search(self):
        """Test a search with no results."""
        self.register(json=self.EMPTY_RESPONSE)
        response = self.mock_request('This search will not match anything')
        self.assertEqual(response, [])

    def test_DoSearch_raises_for_non_200(self):
        """Test the doSearch request raises for non 200 responses."""
        self.register(json=self.EMPTY_RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.SKU_SEARCH_TEXT)


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

    def setUp(self):
        """Register the mock URI."""
        super().setUp()
        self.register(json=[self.RESPONSE])

    def test_FindProductFactoryLinks_request(self):
        """Test the FindProductFactoryLinks request."""
        self.mock_request(self.PRODUCT_ID)
        self.assertDataSent('ProductID', self.PRODUCT_ID)

    def test_FindProductFactoryLinks_returns_FactoryLinks(self):
        """Test the request returns an instance of FactoryLinks."""
        response = self.mock_request(self.PRODUCT_ID)
        self.assertIsInstance(response, inventoryitems.FactoryLinks)

    def test_FindProductFactoryLinks_response_contains_factory_links(self):
        """Test returned object contains instances of FactoryLink."""
        response = self.mock_request(self.PRODUCT_ID)
        self.assertIsInstance(response[0], inventoryitems.FactoryLink)

    def test_FindProductFactoryLinks_contains_factory_link_data(self):
        """Test the correct data is returned."""
        response = self.mock_request(self.PRODUCT_ID)
        self.assertEqual(response[0].product_id, self.PRODUCT_ID)
        self.assertEqual(response[0].link_id, self.LINK_ID)
        self.assertEqual(response[0].factory_name, self.FACTORY_NAME)
        self.assertEqual(response[0].factory_id, self.FACTORY_ID)
        self.assertEqual(response[0].supplier_sku, self.SUPPLIER_SKU)

    def test_FindProductFactoryLinks_links_with_no_links(self):
        """Test FindProductFactoryLinks for a product with no links."""
        self.register(json=[])
        response = self.mock_request(self.PRODUCT_ID)
        self.assertIsInstance(response, inventoryitems.FactoryLinks)
        self.assertEqual(len(response), 0)

    def test_FindProductFactoryLinks_raises_for_non_200(self):
        """Test FindProductFactoryLinks raises for non 200 response."""
        self.register(json=[self.RESPONSE], status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.PRODUCT_ID)


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

    def test_FindProductSelectedOptionsOnly_request(self):
        """Test the FindProductSelectedOptionsOnly request."""
        self.make_request()
        self.assertDataSent('ProductID', self.PRODUCT_ID)
        self.assertDataSent('channelID', '0')

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

    def test_FindProductSelectedOptionsOnly_raises_for_non_200(self):
        """Test FindProductSelectedOptionsOnlyResult raises for non 200."""
        self.register(json=self.NOT_FOUND_RESPONSE_DATA, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.PRODUCT_ID)


class TestProductOperations(TestRequest):
    """Tests for the ProductOperations request."""

    request_class = products.ProductOperations

    SKU = 'VSG-H3R-G0R'
    RESPONSE = {
        "Success": None,
        "Message": None,
        "RecordCount": 1,
        "Data": SKU,
    }

    GETGENERATEDSKU = 'getgeneratedsku'

    def test_ProductOperations_get_generated_sku(self):
        """Test getgeneratedsku request mode."""
        self.register(
            headers={'requestmode': self.GETGENERATEDSKU}, json=self.RESPONSE)
        response = self.mock_request(self.GETGENERATEDSKU)
        self.assertEqual(response.data, self.SKU)

    def test_ProductOperations_request_raises_for_non_200(self):
        """Test ProductOptions request raises for non 200 responses."""
        self.register(
            headers={'requestmode': self.GETGENERATEDSKU},
            json=self.RESPONSE,
            status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.GETGENERATEDSKU)


class TestSaveBarcode(TestRequest):
    """Tests for the saveBarcode request."""

    request_class = products.SaveBarcode
    RESPONSE = 'ok'
    BARCODE = '1321564981'
    PRODUCT_ID = '123654'

    def test_SaveBarcode_request(self):
        """Test the saveBarcode request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            barcode=self.BARCODE, product_id=self.PRODUCT_ID)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('bcode', self.BARCODE)
        self.assertDataSent('prodid', self.PRODUCT_ID)

    def test_SaveBarcode_raises_for_non_200(self):
        """Test the SaveBarcode request raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(barcode=self.BARCODE, product_id=self.PRODUCT_ID)


class TestSaveDescription(TestRequest):
    """Tests for the saveDescription Request."""

    request_class = products.SaveDescription

    RESPONSE = 'ok'
    PRODUCT_ID = '6909316'
    DESCRIPTION = 'Product Description'

    def test_SaveDescription_request(self):
        """Test SaveDescription request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            description=self.DESCRIPTION, product_ids=[self.PRODUCT_ID])
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('prodids', [self.PRODUCT_ID])
        self.assertDataSent('desc', self.DESCRIPTION)
        self.assertDataSent('channelID', '0')

    def test_SaveDescription_without_list(self):
        """Test SaveDescription request."""
        self.register(text=self.RESPONSE)
        self.mock_request(
            description=self.DESCRIPTION, product_ids=self.PRODUCT_ID)
        self.assertDataSent('prodids', [self.PRODUCT_ID])

    def test_SaveDescription_raises_for_non_200(self):
        """Test exception is raised when product ID is invalid."""
        self.register(text='ERROR', status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                description=self.DESCRIPTION, product_ids=[self.PRODUCT_ID])


class TestSaveHandlingTime(TestRequest):
    """Tests for the saveHandlingTime request."""

    request_class = products.SaveHandlingTime

    RESPONSE = 'Success'
    PRODUCT_ID = '6909316'

    def test_SaveHandlingTime_request(self):
        """Test the SaveHandlingTime request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            product_id=self.PRODUCT_ID, handling_time=1, update_channels=False)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('ProductID', self.PRODUCT_ID)
        self.assertDataSent('handlingTime', '1')
        self.assertDataSent('updateChannels', 'False')

    def test_SaveHandlingTime_raises_for_non_200(self):
        """Test SaveHandlingTime request raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_id=self.PRODUCT_ID,
                handling_time=1,
                update_channels=False)


class TestSaveProductName(TestRequest):
    """Tests for the saveProductName request."""

    request_class = products.SaveProductName
    RESPONSE = 'ok'
    PRODUCT_ID = '6909316'
    NAME = 'New Product Name'

    def test_SaveProductName_request(self):
        """Test the saveProductName request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            name=self.NAME, product_ids=[self.PRODUCT_ID])
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('prodids', [self.PRODUCT_ID])
        self.assertDataSent('name', self.NAME)
        self.assertDataSent('channelID', '0')

    def test_SaveProductName_request_with_single_product(self):
        """Test the saveProductName request."""
        self.register(text=self.RESPONSE)
        self.mock_request(name='New Product Name', product_ids=self.PRODUCT_ID)
        self.assertDataSent('prodids', [self.PRODUCT_ID])

    def test_SaveProductName_request_raises(self):
        """Test that the request raises an exception for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                name='New Product Name', product_ids=self.PRODUCT_ID)


class TestSetImageOrder(TestRequest):
    """Tests for the setImageOrder request."""

    request_class = products.SetImageOrder

    IMAGE_IDS = ['28179547', '28179563', '28179581']
    PRODUCT_ID = '6909316'
    RESPONSE = 'ok'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_SetImageOrder_request(self):
        """Test the SetImageOrder request."""
        response = self.mock_request(
            product_id=self.PRODUCT_ID, image_ids=self.IMAGE_IDS)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('order', '^^'.join(self.IMAGE_IDS))
        self.assertDataSent('prodid', self.PRODUCT_ID)

    def test_SetImageOrder_request_raises_for_non_200_response(self):
        """Test that SetImageOrder raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_id=self.PRODUCT_ID, image_ids=self.IMAGE_IDS)


class TestSetProductOptionValue(TestRequest):
    """Tests for the setProductOptionValue request."""

    request_class = products.SetProductOptionValue
    PRODUCT_ID = '6909316'
    OPTION_ID = '32131'
    OPTION_VALUE_ID = '3040649'

    RESPONSE = 'ok'

    def test_SetProductOptionValue_request(self):
        """Test the setProductOptionValue request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            product_ids=[self.PRODUCT_ID],
            option_id=self.OPTION_ID,
            option_value_id=self.OPTION_VALUE_ID)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('prodids', [self.PRODUCT_ID])
        self.assertDataSent('OptionID', self.OPTION_ID)
        self.assertDataSent('OptionValueID', self.OPTION_VALUE_ID)

    def test_SetProductOptionValue_request_with_single_product(self):
        """Test the setProductOptionValue request with a single product."""
        self.register(text=self.RESPONSE)
        self.mock_request(
            product_ids=self.PRODUCT_ID,
            option_id=self.OPTION_ID,
            option_value_id=self.OPTION_VALUE_ID)
        self.assertDataSent('prodids', [self.PRODUCT_ID])

    def test_SetProductOptionValue_raises_for_non_200(self):
        """Test setProductOptionValue raises on non 200 response."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_ids=[self.PRODUCT_ID],
                option_id=self.OPTION_ID,
                option_value_id=self.OPTION_VALUE_ID)


class TestSetProductScope(TestRequest):
    """Tests for the setProductScope request."""

    request_class = products.SetProductScope
    RESPONSE = 'true'
    PRODUCT_ID = '6909316'

    def test_SetProductScope_request(self):
        """Test the setProductScope request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            product_id=self.PRODUCT_ID,
            weight=50,
            height=25,
            length=75,
            width=90,
            large_letter_compatible=False)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('ProductID', self.PRODUCT_ID)
        self.assertDataSent('Weight', '50')
        self.assertDataSent('Height', '25')
        self.assertDataSent('Length', '75')
        self.assertDataSent('Width', '90')
        self.assertDataSent('LargeLetterCompatible', '0')

    def test_SetProductScope_raises_for_non_200(self):
        """Test setProductScope raises on non 200 response."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_id=self.PRODUCT_ID,
                weight=50,
                height=25,
                length=25,
                width=25,
                large_letter_compatible=False)


class TestUpdateOnSalesChannel(TestRequest):
    """Tests for the updateOnSalesChannel request."""

    request_class = products.UpdateProductOnSalesChannel
    RANGE_ID = '4347654'
    PRODUCT_IDS = ['6909316']
    REQUEST_TYPE = 'name'
    VALUE_1 = 'Test Name'
    VALUE_2 = 'Test Val 2'
    CHANNELS = ['1561561']
    ACT = 'Test Act'
    RESPONSE = []

    def test_UpdateProductOnSalesChannel_request(self):
        """Test the UpdateProductOnSalesChannel request."""
        self.register(json=self.RESPONSE)
        response = self.mock_request(
            request_type=self.REQUEST_TYPE,
            range_id=self.RANGE_ID,
            product_ids=self.PRODUCT_IDS,
            act=self.ACT,
            value_1=self.VALUE_1,
            value_2=self.VALUE_2,
            channels=self.CHANNELS)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('brandid', 341)
        self.assertDataSent('rangeid', self.RANGE_ID)
        self.assertDataSent('prodids', ','.join(self.PRODUCT_IDS))
        self.assertDataSent('type', self.REQUEST_TYPE)
        self.assertDataSent('act', self.ACT)
        self.assertDataSent('val1', self.VALUE_1)
        self.assertDataSent('val2', self.VALUE_2)
        self.assertDataSent('chans', ','.join(self.CHANNELS))

    def test_UpdateProductOnSalesChannel_raises_for_non_200(self):
        """Test UpdateProductOnSalesChannel raises for non 200 responses."""
        self.register(json=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                request_type=self.REQUEST_TYPE,
                range_id=self.RANGE_ID,
                product_ids=self.PRODUCT_IDS,
                act=self.ACT,
                value_1=self.VALUE_1,
                value_2=self.VALUE_2,
                channels=self.CHANNELS)


class TestUpdateProductBasePrice(TestRequest):
    """Tests for the updateProductBasePrice request."""

    request_class = products.UpdateProductBasePrice

    RESPONSE = 'Success'
    PRODUCT_ID = '6909316'

    def test_UpdateProductBasePrice_request(self):
        """Test the UpdateProductBasePrice request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(product_id=self.PRODUCT_ID, price=2.50)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('prodid', self.PRODUCT_ID)
        self.assertDataSent('price', '2.5')

    def test_UpdateProductBasePrice_raises_for_non_200(self):
        """Test the UpdateProductBasePrice raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(product_id=self.PRODUCT_ID, price=2.50)


class TestUpdateProductStockLevel(TestRequest):
    """Tests for the UpdateProductStockLevel."""

    request_class = products.UpdateProductStockLevel

    RESPONSE = 'Success'
    PRODUCT_ID = '6909316'

    def test_UpdateProductStockLevel_request(self):
        """Test UpdateProductStockLevel request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            product_id=self.PRODUCT_ID, new_stock_level=5, old_stock_level=10)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('ProductID', self.PRODUCT_ID)
        self.assertDataSent('newStockLevel', '5')
        self.assertDataSent('oldStockLevel', '10')

    def test_UpdateProductStockLevel_raises_for_non_200(self):
        """Test UpdateProductStockLevel raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_id=self.PRODUCT_ID,
                new_stock_level=5,
                old_stock_level=10)


class TestUpdateProductVatRate(TestRequest):
    """Tests for the updateProductVatRate request."""

    request_class = products.UpdateProductVatRate

    RESPONSE = 'Success'
    PRODUCT_ID = '6909316'
    VAT_RATE_ID = '5'

    def test_UpdateProductVatRate_request(self):
        """Test the UpdateProductVatRate request."""
        self.register(text=self.RESPONSE)
        response = self.mock_request(
            product_ids=[self.PRODUCT_ID], vat_rate_id=self.VAT_RATE_ID)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('prodids', [self.PRODUCT_ID])
        self.assertDataSent('vatrate', self.VAT_RATE_ID)

    def test_UpdateProductVatRate_request_with_single_product_ID(self):
        """Test the UpdateProductVatRate request with a string product_ids."""
        self.register(text=self.RESPONSE)
        self.mock_request(
            product_ids=self.PRODUCT_ID, vat_rate_id=self.VAT_RATE_ID)
        self.assertDataSent('prodids', [self.PRODUCT_ID])

    def test_UpdateProductVatRate_raises_for_non_200(self):
        """Test UpdateProductVatRate raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_ids=[self.PRODUCT_ID], vat_rate_id=self.VAT_RATE_ID)


class TestUploadImage(TestRequest):
    """Tests for the uploadImage request."""

    request_class = products.UploadImage

    PRODUCT_ID = '6909316'
    SUCCESSFUL_RESPONSE = {"result": "OK"}
    ERROR_RESPONSE = {"result": "File not found"}

    def setUp(self):
        """Get image to upload."""
        super().setUp()
        self.register(json=self.SUCCESSFUL_RESPONSE)
        self.image = open(
            os.path.join(os.path.dirname(__file__), '14602048.jpg'), 'rb')

    def test_UploadImage_request(self):
        """Test the UploadImage request."""
        response = self.mock_request(
            product_ids=[self.PRODUCT_ID], image_file=self.image)
        self.assertEqual(response, self.SUCCESSFUL_RESPONSE)
        self.assertQuerySent('prodIDs', [self.PRODUCT_ID])

    def test_UploadImage_request_with_single_product_ID(self):
        """Test the UploadImage request with a string arg for product_ids."""
        self.mock_request(product_ids=self.PRODUCT_ID, image_file=self.image)
        self.assertQuerySent('prodIDs', [self.PRODUCT_ID])

    def test_UploadImage_raises_for_invalid_response(self):
        """Test the UploadImage request raises for an error response."""
        self.register(json=self.ERROR_RESPONSE)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_ids=[self.PRODUCT_ID], image_file=self.image)

    def test_UploadImage_raises_for_non_200(self):
        """Test UploadImage raises for non 200 responses."""
        self.register(json=self.SUCCESSFUL_RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_ids=[self.PRODUCT_ID], image_file=self.image)
