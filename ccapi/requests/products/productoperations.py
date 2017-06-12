from .. ccapisession import APIRequest


class ProductOperations(APIRequest):
    uri = 'Handlers/Products/ProductOperations.ashx'

    def __new__(self, request_mode):
        self.request_mode = request_mode
        return super().__new__(self)

    def get_headers(self):
        return {'requestmode': self.request_mode}

    def get_params(self):
        return {'d': '769'}

    def process_response(self, response):
        result = response.json()
        return ProductOperationsResult(result)


class ProductOperationsResult:
    def __init__(self, result):
        self.success = result['Success']
        self.message = result['Message']
        self.record_count = result['RecordCount']
        self.data = result['Data']
