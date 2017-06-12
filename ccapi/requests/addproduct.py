from . ccapisession import APIRequest


class AddProduct(APIRequest):
    uri = 'Handlers/Products/AddProduct.ashx'

    def __new__(
            self, range_id, name, barcode, sku, description, vat_rate_id):
        self.range_id = range_id
        self.name = name
        self.barcode = barcode
        self.sku = sku
        self.description = description
        self.vat_rate_id = vat_rate_id
        return super().__new__(self)

    def process_response(self, response):
        return response.text

    def get_data(self):
        return {
            'ProductID': "0",
            'ProdRangeID': self.range_id,
            'ProdName': self.name,
            'BarCode': self.barcode,
            'SKUCode': self.sku,
            'ProdDescription': self.description,
            'VatRateID': self.vat_rate_id,
            'CopyDesc': "0",
            'BrandID': "341"}

    def get_params(self):
        return {'d': '1496918496099'}
