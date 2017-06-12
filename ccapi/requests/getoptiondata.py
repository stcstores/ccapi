from . ccapisession import APIRequest
from .. inventoryitems import ProductOptionValue


class GetOptionData(APIRequest):
    uri = 'Handlers/ProductOption/getOptionData.ashx'

    def __new__(self, option_id):
        self.option_id = option_id
        return super().__new__(self)

    def process_response(self, response):
        results = response.json()
        return [ProductOptionValue(item) for item in results]

    def get_data(self):
        return {
            'optid': self.option_id}
