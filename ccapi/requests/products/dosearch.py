from .. ccapisession import APIRequest


class DoSearch(APIRequest):
    uri = 'Handlers/Products/doSearch.ashx'

    def __new__(self, text):
        self.text = text
        return super().__new__(self)

    def process_response(self, response):
        results = response.json()
        return [DoSearchResult(item) for item in results]

    def get_data(self):
        return {
            'brandid': '341',
            'text': self.text,
            'type': 'range'
        }


class DoSearchResult:
    def __init__(self, result):
        self.id = result['ID']
        self.variation_id = result['variationID']
        self.name = result['Name']
        self.sku = result['SKU']
        self.thumbnail = result['Thumbnail']

    def __repr__(self):
        return self.name
