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

    # TODO


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
