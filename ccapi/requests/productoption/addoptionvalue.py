from .. ccapisession import APIRequest


class AddOptionValue(APIRequest):
    uri = 'Handlers/ProductOption/addOptionValue.ashx'

    def __new__(self, option_id, value):
        self.option_id = option_id
        self.value = value
        return super().__new__(self)

    def process_response(self, response):
        return response.text

    def get_data(self):
        return {
            'optid': self.option_id,
            'val': self.value,
            'brandID': '341'}


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
