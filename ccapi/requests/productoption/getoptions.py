from .. ccapisession import APIRequest
from ccapi.inventoryitems import ProductOption


class GetOptions(APIRequest):
    uri = 'Handlers/ProductOption/getOptions.ashx'

    def process_response(self, response):
        results = response.json()
        return [ProductOption(item) for item in results]

    def get_data(self):
        return {
            'brandID': "341",
            'strOptionTypes': "1,+2,+6"}
