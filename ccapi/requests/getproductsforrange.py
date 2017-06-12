from . apirequest import APIRequest
from .. inventoryitems import ProductRange


class GetProductsForRange(APIRequest):
    uri = 'Handlers/getProductsForRange.ashx'

    def __new__(self, product_id):
        self.product_id = product_id
        return super().__new__(self)

    def process_response(self, response):
        result = response.json()
        return ProductRange(result)

    def get_data(self):
        return {
            'ProdRangeID': self.product_id,
            'salesChannelID': "0"}

    def get_params(self):
        return {'d': '155'}
