from . ccapisession import APIRequest


class UpdateProductStockLevel(APIRequest):
    uri = 'Handlers/Products/UpdateProductStockLevel.ashx'

    def __new__(self, product_id, new_stock_level, old_stock_level):
        self.product_id = product_id
        self.new_stock_level = new_stock_level
        self.old_stock_level = old_stock_level
        return super().__new__(self)

    def get_data(self):
        return {
            'AccountID': '4419651',
            'ProductID': self.product_id,
            'newStockLevel': self.new_stock_level,
            'oldStockLevel': self.old_stock_level
        }
