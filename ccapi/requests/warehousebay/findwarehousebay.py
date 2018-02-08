"""
FindWarehouseBay request.

Creates a new product range.
"""
from bs4 import BeautifulSoup
from ccapi.inventoryitems import WarehouseBay

from ..apirequest import APIRequest


class FindWarehouseBay(APIRequest):
    """FindWarehouseBay request."""

    uri = 'Handlers/WarehouseBay/FindWarehouseBay.ashx'

    def __new__(
            self, prog_type=None, operation=None, warehouse_id=None,
            product_id=None, warehouse_bay_id=None, products=False,
            skip_records=0, take_limit=100):
        """Create FindWarehouseBay request."""
        self.prog_type = prog_type
        self.operation = operation
        self.warehouse_id = warehouse_id
        self.product_id = product_id
        self.warehouse_bay_id = warehouse_bay_id
        self.products = products
        self.skip_records = skip_records
        self.take_limit = take_limit
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        if len(response.text) > 0:
            if self.operation is None and not self.products:
                return self.parse_bay_html(self, response.text)
            data = response.json()
            if isinstance(data, dict) and data['Data'] is None:
                return []
            if 'Data' in data and isinstance(data['Data'], list):
                return [WarehouseBay(bay) for bay in data['Data']]
            return [WarehouseBay(bay) for bay in data]

    def parse_bay_html(self, html):
        """Create WarehouseBay objects from HTML response."""
        soup = BeautifulSoup(html, 'html.parser')
        bay_divs = soup.findAll('div', {'class': 'warehouse--bay--item'})
        data = [{
            'ID': bay_div.find('div', {'class': 'ListItem'})['data-bayid'],
            'Name': bay_div.find('a', {'class': 'bay--name'}).text}
            for bay_div in bay_divs]
        return [WarehouseBay(bay) for bay in data]

    def get_data(self):
        """Get data for request."""
        data = {}
        if self.prog_type is not None:
            data['ProgType'] = self.prog_type
        if self.operation is not None:
            data['operation'] = self.operation
        if self.warehouse_id is not None:
            data['WarehouseId'] = self.warehouse_id
        if self.product_id is not None:
            data['ProductId'] = self.product_id
        if self.warehouse_bay_id is not None:
            data['warehousebayid'] = self.warehouse_bay_id
        return data

    def get_headers(self):
        if self.products is False and self.operation is None:
            return {'template': 'WarehouseBay.List'}
        if self.products is True:
            return {
                'TakeLimit': str(self.take_limit),
                'SkipRecords': str(self.skip_records)}
        return {}

    def get_params(self):
        """Get parameters for get request."""
        return {}
