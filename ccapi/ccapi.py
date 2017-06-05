from . requests import CloudCommerceAPISession
from . import requests


class CCAPI:

    def __init__(self, username, password):
        CloudCommerceAPISession.get_session(username, password)

    def search_products(self, search_text):
        return requests.DoSearch(search_text)

    def get_sku(self, range_sku=False):
        response = requests.ProductOperations('getgeneratedsku')
        sku = response.data
        if range_sku is True:
            sku = 'RNG_{}'.format(sku)
        return sku

    def get_variation_by_id(self, variation_id):
        return requests.FindProductSelectedOptionsOnly(variation_id)

    def get_product_options(self):
        return requests.GetOptions()

    def update_product_stock_level(
            self, product_id, new_stock_level, old_stock_level):
        requests.UpdateProductStockLevel(
            str(product_id), new_stock_level, old_stock_level)
