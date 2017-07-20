"""
GetProductsForRange request.

Advanced Product search.
"""

import json
from .. apirequest import APIRequest


class GetProducts(APIRequest):
    """GetProductsForRange request."""

    uri = '/Handlers/ProductManager/GetProducts.ashx'

    def __new__(
            self, search_text='-', master_category_id=0, search_type=0,
            main_products=True, clones=True, only_in_stock=False,
            listing_status=0, product_id=0, product_range_id=0,
            channel_identifier='', name='', price_from=0, price_to=0,
            product_type=-1, sort_by='', skip_records=0, take_records=100,
            take_exact_match=False, channel_type=-1, channel_id=0,
            sort_desc=False, id_list=None, option_matches_id=0,
            multi_listings=True):
        """Create GetProductsForRange request.

        Kwargs:
            search_text: Text to find in title or SKU.
            option_matches_id: Option Value ID to match.
        """
        if search_text.strip() == '':
            search_text = '-'
        self.search_text = search_text
        self.master_category_id = master_category_id
        self.search_type = search_type
        self.main_products = main_products
        self.clones = clones
        self.only_in_stock = only_in_stock
        self.listing_status = listing_status
        self.product_id = product_id
        self.product_range_id = product_range_id
        self.channel_identifier = channel_identifier
        self.name = name
        self.price_from = price_from
        self.price_to = price_to
        self.product_type = product_type
        self.sort_by = sort_by
        self.skip_records = skip_records
        self.take_records = take_records
        self.take_exact_match = take_exact_match
        self.channel_type = channel_type
        self.channel_id = channel_id
        self.sort_desc = sort_desc
        self.id_list = id_list
        self.option_matches_id = option_matches_id
        if self.option_matches_id is None:
            self.option_matches_id = 0
        self.multi_listings = multi_listings
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        search_options = {
            "MasterCategoryId": self.master_category_id,
            "SearchType": self.search_type,
            "SKU": self.search_text,
            "MainProducts": self.main_products,
            "Clones": self.clones,
            "OnlyInStock": self.only_in_stock,
            "listingStatus": self.listing_status,
            "ProductId": self.product_id,
            "ProductRangeId": self.product_range_id,
            "ChannelIdentifier": self.channel_identifier,
            "Name": self.name,
            "PriceFrom": self.price_from,
            "PriceTo": self.price_to,
            "ProductType": self.product_type,
            "SortBy": self.sort_by,
            "SkipRecords": self.skip_records,
            "TakeRecords": self.take_records,
            "TakeExactMatch": self.take_exact_match,
            "ChannelType": self.channel_type,
            "ChannelId": self.channel_id,
            "SortDesc": self.sort_desc,
            "idList": self.id_list,
            "OptionMatchesId": self.option_matches_id,
            "MultiListings": self.multi_listings
        }
        data = {'SearchOptions': json.dumps(search_options)}
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '57'}

    def process_response(self, response):
        """Handle request response."""
        data = response.json()['Data']
        if data is None:
            return []
        return data
