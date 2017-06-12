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
    def get_options_for_product(product_id):
        response = requests.FindProductSelectedOptionsOnly(product_id)
        return response.options

    @staticmethod
    def get_options_for_range(range_id):
        response = requests.GetProductData(range_id)
        return response.options

    @staticmethod
    def get_product_options():
        return requests.GetOptions()

    @staticmethod
    def get_option_values(option_id):
        return requests.GetOptionData(option_id)

    @staticmethod
    def update_product_stock_level(
            product_id, new_stock_level, old_stock_level):
        requests.UpdateProductStockLevel(
            str(product_id), new_stock_level, old_stock_level)

    @classmethod
    def create_range(cls, range_name, sku=None):
        if sku is None:
            sku = cls.get_sku(range_sku=True)
        new_range_id = requests.AddNewRange(range_name, sku)
        return cls.get_range(new_range_id)

    @staticmethod
    def create_option_value(option_id, value):
        return requests.AddOptionValue(option_id, value)

    @classmethod
    def get_product_option_id(cls, option_name):
        options = cls.get_product_options()
        for option in options:
            if option.option_name == option_name:
                return option.id

    @classmethod
    def get_option_value_id(cls, option_id, value, create=False):
        values = cls.get_option_values(option_id)
        for option_value in values:
            if option_value.value == value:
                return value.id
        if create is True:
            return cls.create_option_value(option_id, value)

    @staticmethod
    def add_option_to_product(product_id, option_id):
        requests.AddRemProductOption(product_id, option_id, action='add')

    @staticmethod
    def remove_option_from_product(product_id, option_id):
        requests.AddRemProductOption(product_id, option_id, action='remove')

    @staticmethod
    def get_range(range_id):
        return requests.GetProductsForRange(range_id)
