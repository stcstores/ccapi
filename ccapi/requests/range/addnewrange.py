"""
AddNewRange request.

Creates a new product range.
"""

from ..apirequest import APIRequest


class AddNewRange(APIRequest):
    """AddNewRange request."""

    uri = 'Handlers/Range/addNewRange.ashx'

    def __new__(
            self,
            *,
            range_name,
            sku,
            end_of_line=0,
            group_all_items=0,
            pre_order=0):
        """Create AddNewRange request.

        Args:
            range_name: Name of new range
            sku: SKU for new range

        Kwargs:
            product_range_id: Placeholder range ID. Default: 0.
            end_of_line: Range is end of line. Default: 0.
            group_all_items: Default 0.
            pre_order: Default: 0.
        """
        self.range_name = range_name
        self.sku = sku
        self.end_of_line = end_of_line
        self.group_all_items = group_all_items
        self.pre_order = pre_order
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response,
            f'Error creating product range "{self.range_name}"')
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            'ProdRangeID': 0,
            'EndOfLine': int(bool(self.end_of_line)),
            'PreOrder': int(bool(self.pre_order)),
            'GroupAllItems': int(bool(self.group_all_items)),
            'RangeName': self.range_name,
            'SKUCode': self.sku,
            'BrandID': "341"
        }

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '1496918496099'}
