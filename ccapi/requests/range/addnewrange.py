from .. ccapisession import APIRequest


class AddNewRange(APIRequest):
    uri = 'Handlers/Range/addNewRange.ashx'

    def __new__(
            self, range_name, sku, product_range_id=0, end_of_line=0,
            group_all_items=0, pre_order=0):
        self.range_name = range_name
        self.sku = sku
        self.product_range_id = product_range_id
        self.end_of_line = end_of_line
        self.group_all_items = group_all_items
        self.pre_order = pre_order
        return super().__new__(self)

    def process_response(self, response):
        return response.text

    def get_data(self):
        return {
            'ProdRangeID': self.product_range_id,
            'EndOfLine': self.end_of_line,
            'PreOrder': self.pre_order,
            'GroupAllItems': self.group_all_items,
            'RangeName': self.range_name,
            'SKUCode': self.sku,
            'BrandID': "341"}

    def get_params(self):
        return {'d': '1496918496099'}
