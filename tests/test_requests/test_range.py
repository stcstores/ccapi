"""Tests for range requests."""

from ccapi import cc_objects, exceptions
from ccapi.requests import range

from .. import test_data
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
    RANGE_ID = '4462752'
    OPTION_ID = '32129'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_add_action(self):
        """Test the add action of the AddRemProductOption request."""
        self.mock_request(
            range_id=self.RANGE_ID, option_id=self.OPTION_ID, add=True)
        self.assertDataSent('prdid', self.RANGE_ID)
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
            range_id=self.RANGE_ID, option_id=self.OPTION_ID, remove=True)
        self.assertDataSent('prdid', self.RANGE_ID)
        self.assertDataSent('optid', self.OPTION_ID)
        self.assertDataSent('act', 'rem')

    def test_AddRemProductOption_raises_for_non_200(self):
        """Test the AddRemProductOption request raises for non 200 response."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                range_id=self.RANGE_ID, option_id=self.OPTION_ID, add=True)

    def test_add_and_remove_both_True(self):
        """Test the request with both add and remove arguments True."""
        with self.assertRaises(ValueError):
            self.mock_request(
                range_id=self.RANGE_ID,
                option_id=self.OPTION_ID,
                add=True,
                remove=True)

    def test_add_and_remove_both_False(self):
        """Test the request with both add and remove arguments False."""
        with self.assertRaises(ValueError):
            self.mock_request(
                range_id=self.RANGE_ID,
                option_id=self.OPTION_ID,
                add=False,
                remove=False)


class TestCheckRangesOnSalesChannel(TestRequest):
    """Test the CheckRangesOnSalesChannel request."""

    request_class = range.CheckRangesOnSalesChannel

    RESPONSE = test_data.CHECK_RANGES_ON_SALES_CHANNEL_RESULT
    EMPTY_RESPONSE = []
    RANGE_ID = '4462752'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(json=self.RESPONSE)

    def test_sends_range_id(self):
        """Test the CheckRangesOnSalesChannel sends the passed range ID."""
        self.mock_request(self.RANGE_ID)
        self.assertDataSent('rangeid', self.RANGE_ID)
        self.assertDataSent('brandid', 341)

    def test_returns_list(self):
        """Test the CheckRangesOnSalesChannel request returns a list."""
        response = self.mock_request(self.RANGE_ID)
        self.assertIsInstance(response, list)

    def test_returns_list_of_sales_channels(self):
        """Test the request returns a list of ccapi.cc_objects.SalesChannel."""
        response = self.mock_request(self.RANGE_ID)
        self.assertIsInstance(response[0], cc_objects.SalesChannel)

    def test_returns_empty_list_for_empty_response(self):
        """Test the request returns an empty list when no channels exist."""
        self.register(json=[])
        response = self.mock_request(self.RANGE_ID)
        self.assertEqual(response, [])

    def test_raises_for_non_200(self):
        """Test the request raises for non 200 responses."""
        self.register(json=[], status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.RANGE_ID)


class TestDeleteProductRange(TestRequest):
    """Test the DeleteProductRange request."""

    request_class = range.DeleteProductRange

    RESPONSE = 'Deleted^^0Deleted^^0'
    RANGE_ID = '4462752'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_DeleteProductRange_request(self):
        """Test the DeleteProductRangeRequest."""
        self.mock_request(self.RANGE_ID)
        self.assertDataSent('ProgType', 'DeleteProductRange')
        self.assertDataSent('BrandID', 341)
        self.assertDataSent('ProdRangeID', self.RANGE_ID)

    def test_DeleteProductRange_raises_for_non_200(self):
        """Test the DeleteProductRange request raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.RANGE_ID)


class TestSetOptionSelect(TestRequest):
    """Test the SetOptionSelect request."""

    request_class = range.SetOptionSelect

    RANGE_ID = '4355752'
    OPTION_ID = '32129'
    DROP_DOWN = True

    RESPONSE = 'ok'

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_SetOptionSelect_request(self):
        """Test the SetOptionSelect request."""
        self.mock_request(
            range_id=self.RANGE_ID,
            option_id=self.OPTION_ID,
            drop_down=self.DROP_DOWN)
        self.assertDataSent('prdid', self.RANGE_ID)
        self.assertDataSent('optid', self.OPTION_ID)
        self.assertDataSent('onoff', int(self.DROP_DOWN))

    def test_SetOptionSelect_raises_for_non_200(self):
        """Test the request raises for a non 200 response."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                range_id=self.RANGE_ID,
                option_id=self.OPTION_ID,
                drop_down=self.DROP_DOWN)


class TestUpdateOnSalesChannel(TestRequest):
    """Test the UpdateRangeOnSalesChannel request."""

    request_class = range.UpdateRangeOnSalesChannel

    RESPONSE = []

    RANGE_ID = '4355752'
    REQUEST_TYPE = 'select'
    ACT = 'update'
    VALUE = 'Test Value'
    OPTION_ID = '32129'
    CHANNEL_IDS = ['3541', '3557']

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(json=self.RESPONSE)

    def test_UpdateRangeOnSalesChannel_request(self):
        """Test the UpdateRangeOnSalesChannel requset."""
        self.mock_request(
            range_id=self.RANGE_ID,
            request_type=self.REQUEST_TYPE,
            act=self.ACT,
            value=self.VALUE,
            option_id=self.OPTION_ID,
            channel_ids=self.CHANNEL_IDS)
        self.assertDataSent('rangeid', self.RANGE_ID)
        self.assertDataSent('type', self.REQUEST_TYPE)
        self.assertDataSent('act', self.ACT)
        self.assertDataSent('val', self.VALUE)
        self.assertDataSent('optid', self.OPTION_ID)
        self.assertDataSent('chans', self.CHANNEL_IDS)
        self.assertDataSent('brandid', 341)

    def test_UpdateRangeOnSalesChannel_raises_for_non_200(self):
        """Test UpdateRangeOnSalesChannel raies for non 200 responses."""
        self.register(json=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                range_id=self.RANGE_ID,
                request_type=self.REQUEST_TYPE,
                act=self.ACT,
                value=self.VALUE,
                option_id=self.OPTION_ID,
                channel_ids=self.CHANNEL_IDS)


class TestUpdateRangeSettings(TestRequest):
    """Test the UpdateRangeSettings request."""

    request_class = range.UpdateRangeSettings

    RESPONSE = '"OK"'

    RANGE_ID = '4355752'
    CURRENT_NAME = "Test Move Department 2"
    CURRENT_SKU = "RNG_UYV-3SP-W60"
    CURRENT_END_OF_LINE = False
    CURRENT_PRE_ORDER = False
    CURRENT_GROUP_ITEMS = False
    NEW_NAME = "Test Move Department 2"
    NEW_SKU = "RNG_UYV-3SP-W60"
    NEW_END_OF_LINE = "0"
    NEW_PRE_ORDER = False
    NEW_GROUP_ITEMS = False
    CHANNELS = ['3541', '3557']

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)
        self.mock_request(
            range_id=self.RANGE_ID,
            current_name=self.CURRENT_NAME,
            current_sku=self.CURRENT_SKU,
            current_end_of_line=self.CURRENT_END_OF_LINE,
            current_pre_order=self.CURRENT_PRE_ORDER,
            current_group_items=self.CURRENT_GROUP_ITEMS,
            new_name=self.NEW_NAME,
            new_sku=self.NEW_SKU,
            new_end_of_line=self.NEW_END_OF_LINE,
            new_pre_order=self.NEW_PRE_ORDER,
            new_group_items=self.NEW_GROUP_ITEMS,
            channels=self.CHANNELS)

    def test_UpdateRangeSettings_sends_range_id(self):
        """Test the request sends the passed range ID."""
        self.assertJsonValueSent('rangeID', self.RANGE_ID)

    def test_UpdateRangeSettings_sends_current_name(self):
        """Test the request sends the passed current name."""
        self.assertJsonValueSent('currName', self.CURRENT_NAME)

    def test_UpdateRangeSettings_sends_current_sku(self):
        """Test the request sends the passed current SKU."""
        self.assertJsonValueSent('currSKU', self.CURRENT_SKU)

    def test_UpdateRangeSettings_sends_current_end_of_line(self):
        """Test the request sends the passed current end of line."""
        self.assertJsonValueSent('currEoL', int(self.CURRENT_END_OF_LINE))

    def test_UpdateRangeSettings_sends_current_pre_order(self):
        """Test the request sends the passed current pre order."""
        self.assertJsonValueSent('currPreO', int(self.CURRENT_PRE_ORDER))

    def test_UpdateRangeSettings_sends_current_group_items(self):
        """Test the request sends the passed current group items."""
        self.assertJsonValueSent('currGBy', str(int(self.CURRENT_GROUP_ITEMS)))

    def test_UpdateRangeSettings_sends_new_name(self):
        """Test the request sends the passed new name."""
        self.assertJsonValueSent('newName', self.NEW_NAME)

    def test_UpdateRangeSettings_sends_new_sku(self):
        """Test the request sends the passed new SKU."""
        self.assertJsonValueSent('newSKU', self.NEW_SKU)

    def test_UpdateRangeSettings_sends_new_end_of_line(self):
        """Test the request sends the passed new end of line."""
        self.assertJsonValueSent('newEoL', str(int(self.NEW_END_OF_LINE)))

    def test_UpdateRangeSettings_sends_new_pre_order(self):
        """Test the request sends the passed new pre order."""
        self.assertJsonValueSent('newPreO', str(int(self.NEW_PRE_ORDER)))

    def test_UpdateRangeSettings_sends_new_group_items(self):
        """Test the request sends the passed new group items."""
        self.assertJsonValueSent('newGBy', str(int(self.NEW_GROUP_ITEMS)))

    def test_UpdateRangeSettings_sends_channels(self):
        """Test the request sends the passed channels."""
        self.assertJsonValueSent('channels', self.CHANNELS)

    def test_UpdateRangeSettings_sends_brand_id(self):
        """Test the request sends the passed brand ID."""
        self.assertJsonValueSent('brandID', 341)

    def test_UpdateRangeSettings_raises_for_non_200_response(self):
        """Test UpdateRangeSettings rasies for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                range_id=self.RANGE_ID,
                current_name=self.CURRENT_NAME,
                current_sku=self.CURRENT_SKU,
                current_end_of_line=self.CURRENT_END_OF_LINE,
                current_pre_order=self.CURRENT_PRE_ORDER,
                current_group_items=self.CURRENT_GROUP_ITEMS,
                new_name=self.NEW_NAME,
                new_sku=self.NEW_SKU,
                new_end_of_line=self.NEW_END_OF_LINE,
                new_pre_order=self.NEW_PRE_ORDER,
                new_group_items=self.NEW_GROUP_ITEMS,
                channels=self.CHANNELS)
