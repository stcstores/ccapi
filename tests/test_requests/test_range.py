"""Tests for range requests."""

from ccapi import exceptions
from ccapi.requests import range

from .test_request import TestRequest


class TestAddNewRange(TestRequest):
    """Tests for the AddNewRange request."""

    request_class = range.AddNewRange

    RESPONSE = '4940634'
    RANGE_NAME = 'New Product Range'
    SKU = 'WUA-DU7-W6W'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_AddNewRange_request(self):
        """Test the AddNewRange request."""
        response = self.mock_request(range_name=self.RANGE_NAME, sku=self.SKU)
        self.assertEqual(response, self.RESPONSE)
        self.assertDataSent('ProdRangeID', 0)
        self.assertDataSent('EndOfLine', 0)
        self.assertDataSent('PreOrder', 0)
        self.assertDataSent('GroupAllItems', 0)
        self.assertDataSent('RangeName', self.RANGE_NAME)
        self.assertDataSent('SKUCode', self.SKU)
        self.assertDataSent('BrandID', '341')

    def test_end_of_line_argument(self):
        """Test the AddNewRange request with the end_of_line argument."""
        self.mock_request(
            range_name=self.RANGE_NAME, sku=self.SKU, end_of_line=True)
        self.assertDataSent('EndOfLine', 1)
        self.mock_request(
            range_name=self.RANGE_NAME, sku=self.SKU, end_of_line=False)
        self.assertDataSent('EndOfLine', 0)

    def test_pre_order_agument(self):
        """Test the AddNewRange request with the pre_order argument."""
        self.mock_request(
            range_name=self.RANGE_NAME, sku=self.SKU, pre_order=True)
        self.assertDataSent('PreOrder', 1)
        self.mock_request(
            range_name=self.RANGE_NAME, sku=self.SKU, pre_order=False)
        self.assertDataSent('PreOrder', 0)

    def test_group_all_items_agument(self):
        """Test the AddNewRange request with the group_all_items argument."""
        self.mock_request(
            range_name=self.RANGE_NAME, sku=self.SKU, group_all_items=True)
        self.assertDataSent('GroupAllItems', 1)
        self.mock_request(
            range_name=self.RANGE_NAME, sku=self.SKU, group_all_items=False)
        self.assertDataSent('GroupAllItems', 0)

    def test_AddNewRange_raises_for_non_200(self):
        """Test the AddNewRange request raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(range_name=self.RANGE_NAME, sku=self.SKU)


class TestAddRemProductOption(TestRequest):
    """Test the AddRemProductOption request."""

    request_class = range.AddRemProductOption

    RESPONSE = ''
    PRODUCT_ID = '4462752'
    OPTION_ID = '32129'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_add_action(self):
        """Test the add action of the AddRemProductOption request."""
        self.mock_request(
            product_id=self.PRODUCT_ID, option_id=self.OPTION_ID, add=True)
        self.assertDataSent('prdid', self.PRODUCT_ID)
        self.assertDataSent('optid', self.OPTION_ID)
        self.assertDataSent('act', 'add')
        self.assertDataSent('ebyopt', 0)
        self.assertDataSent('ebyimg', 0)
        self.assertDataSent('amaopt', 0)
        self.assertDataSent('amaimg', 0)
        self.assertDataSent('shpfil', 0)
        self.assertDataSent('shpgrp', 0)
        self.assertDataSent('shpsel', 0)

    def test_rem_action(self):
        """Test the rem action of the AddRemProductOption request."""
        self.mock_request(
            product_id=self.PRODUCT_ID, option_id=self.OPTION_ID, remove=True)
        self.assertDataSent('prdid', self.PRODUCT_ID)
        self.assertDataSent('optid', self.OPTION_ID)
        self.assertDataSent('act', 'rem')

    def test_AddRemProductOption_raises_for_non_200(self):
        """Test the AddRemProductOption request raises for non 200 response."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                product_id=self.PRODUCT_ID, option_id=self.OPTION_ID, add=True)

    def test_add_and_remove_both_True(self):
        """Test the request with both add and remove arguments True."""
        with self.assertRaises(ValueError):
            self.mock_request(
                product_id=self.PRODUCT_ID,
                option_id=self.OPTION_ID,
                add=True,
                remove=True)

    def test_add_and_remove_both_False(self):
        """Test the request with both add and remove arguments False."""
        with self.assertRaises(ValueError):
            self.mock_request(
                product_id=self.PRODUCT_ID,
                option_id=self.OPTION_ID,
                add=False,
                remove=False)


class TestCheckRangesOnSalesChannel(TestRequest):
    """Test the CheckRangesOnSalesChannel request."""

    request_class = range.CheckRangesOnSalesChannel

    # TODO


class TestDeleteProductRange(TestRequest):
    """Test the DeleteProductRange request."""

    request_class = range.DeleteProductRange

    # TODO


class TestSetOptionSelect(TestRequest):
    """Test the SetOptionSelect request."""

    request_class = range.SetOptionSelect

    # TODO


class TestUpdateOnSalesChannel(TestRequest):
    """Test the UpdateRangeOnSalesChannel request."""

    request_class = range.UpdateRangeOnSalesChannel

    # TODO


class TestUpdateRangeSettings(TestRequest):
    """Test the UpdateRangeSettings request."""

    request_class = range.UpdateRangeSettings

    # TODO
