from . requests import CloudCommerceAPISession
from . import requests


class CCAPI:

    def __init__(self, username, password):
        self.create_session(username, password)

    @staticmethod
    def create_session(username, password):
        CloudCommerceAPISession.get_session(username, password)

    @staticmethod
    def search_products(search_text):
        return requests.DoSearch(search_text)

    @staticmethod
    def get_sku(range_sku=False):
        response = requests.ProductOperations('getgeneratedsku')
        sku = response.data
        if range_sku is True:
            sku = 'RNG_{}'.format(sku)
        return sku

    @staticmethod
    def get_variation_by_id(variation_id):
        return requests.FindProductSelectedOptionsOnly(variation_id)

    @staticmethod
    def get_product_options():
        return requests.GetOptions()

    @staticmethod
    def update_product_stock_level(
            product_id, new_stock_level, old_stock_level):
        requests.UpdateProductStockLevel(
            str(product_id), new_stock_level, old_stock_level)
