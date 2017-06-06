from . ccapisession import APIRequest


class GetOptionData(APIRequest):
    uri = 'Handlers/ProductOption/getOptionData.ashx'

    def __new__(self, option_id):
        self.option_id = option_id
        return super().__new__(self)

    def process_response(self, response):
        results = response.json()
        return [GetOptionDataResult(item) for item in results]

    def get_data(self):
        return {
            'optid': self.option_id}


class GetOptionDataResult:

    def __init__(self, result):
        self.json = result
        self.id = result['ID']
        self.value = result['OptionValue']
        self.brand_id = result['BrandID']
        self.option_id = result['OptionID']
        self.value_trans = result['OptionValueTrans']
        self.sort_order = result['OptionsortOrder']
        self.selected = result['Selected']
        self.product_count = result['ProductCount']
        self.option_name = result['OptionName']

    def __repr__(self):
        return self.value
