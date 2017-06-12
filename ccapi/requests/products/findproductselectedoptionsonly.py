from .. ccapisession import APIRequest
from ccapi.inventoryitems import Product, ProductOptions, ProductOption


class FindProductSelectedOptionsOnly(APIRequest):
    uri = 'Handlers/Products/findProductSelectedOptionsOnly.ashx'

    def __new__(self, product_id, channel_id=0):
        self.product_id = product_id
        self.channel_id = channel_id
        return super().__new__(self)

    def get_data(self):
        return {'ProductID': self.product_id, 'channelID': self.channel_id}

    def process_response(self, response):
        results = response.json()
        return FindProductSelectedOptionsOnlyResult(results)


class FindProductSelectedOptionsOnlyResult:

    def __init__(self, data):
        self.stock_level = data['StockLevel']
        self.fba_stock_level = data['FBAStockLevel']
        if data['product'] is not None:
            self.product = Product(data['product'])
        self.options = ProductOptions(
            [ProductOption(option) for option in data['options']])
