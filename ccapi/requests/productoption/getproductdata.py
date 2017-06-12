"""GetProductData request.

Gets product options assigned to given range.
"""

from .. apirequest import APIRequest
from ccapi.inventoryitems import ProductOptions, ProductOption


class GetProductData(APIRequest):
    """Wrapper for GetProductData request."""

    uri = 'Handlers/ProductOption/getProductData.ashx'

    def __new__(self, range_id, channel_id=0):
        """Create GetProductData request.

        Args:
            range_id: ID of range
        """
        self.range_id = range_id
        self.channel_id = channel_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {
            'RangeID': self.range_id,
            'channelID': self.channel_id,
            'brandID': '341'}

    def process_response(self, response):
        """Handle request response."""
        results = response.json()
        return GetProductDataResult(results)


class GetProductDataResult:
    """Wrapper for response from GetProductData request."""

    def __init__(self, data):
        """Load data from GetProductData request."""
        self.name = data['Name']
        self.group_by = data['GroupBy']
        self.sales_channel_type = data['SalesChannelType']
        self.shop_options = [
            ShopOptions(option) for option in data['ShopOptions']]
        self.options = ProductOptions(
            [ProductDataOption(option) for option in data['ProductOptions']])


class ProductDataOption(ProductOption):
    """Product Option beloning to range."""

    def __init__(self, data):
        """Load data from GetProductData request."""
        self.id = data['OptionID']
        self.option_name = data['OptionName']
        self.option_type = data['OptionType']
        self.is_web_shop_group_by = data['IsWebShopGroupBy']
        self.is_web_shop_select = data['IsWebShopSelect']
        self.is_web_shop_filter = data['IsWebShopFilter']
        self.is_ebay_option = data['IsEbayOption']
        self.is_ebay_image_option = data['IsEbayImageOption']
        self.is_amazon_option = data['IsAmazonOption']
        self.is_amazon_select = data['IsAmazonSelect']
        self.hidden = data['Hidden']
        self.pre_select_on_create_range = data['PreSelectOnCreateRange']


class ShopOptions:
    """Shop option for range."""

    def __init__(self, data):
        """Load data from GetProductData request."""
        self.id = data['OptionID']
        self.name = data['OptionName']
        self.type = data['OptionType']
        self.is_master = data['IsMaster']
        self.is_used_by_product = data['IsUsedByProduct']
        self.hidden = data['Hidden']
        self.pre_select_on_create_range = data['PreSelectOnCreateRange']
