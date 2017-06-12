from . ccapisession import APIRequest


class AddRemProductOption(APIRequest):
    uri = '/Handlers/Range/addRemProductOption.ashx'

    def __new__(self, product_id, option_id, action='add'):
        self.product_id = product_id
        self.product_id = product_id
        self.option_id = option_id
        self.action = action
        return super().__new__(self)

    def get_data(self):
        if self.action == 'add':
            return {
                'prdid': self.product_id,
                'optid': self.option_id,
                'act': 'add',
                'ebyopt': "0",
                'ebyimg': "0",
                'amaopt': "0",
                'amaimg': "0",
                'shpfil': "0",
                'shpgrp': "0",
                'shpsel': "0",
            }
        if self.action == 'rem':
            return {
                'prdid': self.product_id,
                'optid': self.option_id,
                'act': 'rem',
            }
        raise Exception('action must be "add" or "rem"')

    def process_response(self, response):
        pass
