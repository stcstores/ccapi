from ccapi import ccapi


class MetaProductOptions(type):

    def __iter__(self):
        for option in self.options:
            yield option

    def __getitem__(self, index):
        return self.option_names[index]

    @property
    def options(self):
        if self._options is None:
            self._options = ccapi.CCAPI.get_product_options()
        return self._options

    @property
    def option_names(self):
        if self._option_names is None:
            self._option_names = {
                option.option_name: option for option in self.options}
        return self._option_names


class ProductOptions(metaclass=MetaProductOptions):

    _options = None
    _option_names = None

    def __init__(self, options):
        self.options = options
        self.option_names = {
            option.option_name: option for option in self.options}

    def __iter__(self):
        for option in self.options:
            yield option

    def __getitem__(self, index):
        return self.option_names[index]

    def __repr__(self):
        return '{} product options'.format(len(self.options))


class ProductOption:

    _values = None

    def __init__(self, result):
        self.json = result
        self.id = result['ID']
        self.option_name = result['OptionName']
        self.option_names = {
            'ebay': result['OptionEbayName'],
            'amazon': result['OptionAmazonName'],
            'pretty': result['OptionPrettyName'],
            'web': result['OptionWebName'],
        }
        self.option_type = result['OptionType']
        self.master = result['Master']
        self.hidden = result['Hidden']
        self.pre_selected = result['PreSelectOnCreateRange']
        self.status = result['Statusw']
        self.exclusions = {
            'amazon': result['excludeAmazon'],
            'ebay': result['excludeEbay'],
            'market_place': result['excludeMarketPlace'],
            'epos': result['excludeEpos'],
            'magento': result['excludeMagento'],
            'woo_commerce': result['excludeWooCommerce'],
            'shopify': result['excludeShopify'],
            'tesco': result['excludeTesco'],
            'google': result['excludeGoogle']
        }
        self.selected = result['Selected']
        if 'optionValues' in result:
            self._values = [
                ProductOptionValue(value) for value in result['optionValues']]
            self.reload_values()

    def __repr__(self):
        return self.option_name

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.values[index]
        else:
            return self.value_names[index]

    @property
    def values(self):
        if self._values is None:
            self.reload_values()
        return self._values

    @property
    def value_names(self):
        if self._value_names is None:
            self.load_value_names()
        return self._value_names

    def load_value_names(self):
        return {value.name: value for value in self.values}

    def reload_values(self):
        self._values = ccapi.CCAPI.get_option_values(self.id)
        self.load_value_names()

    def add_value(self, value):
        if value in self._value_names:
            raise Exception(
                'Option Value {} already exists for product option {}'.format(
                    self.option_name, value))
        new_value_id = ccapi.CCAPI.create_option_value(value)
        self.reload_values()
        return new_value_id

    def get_value(self, value, create=False):
        if value in self._value_names:
            return self._value_names[value]
        if create is True:
            self.add_value(value)
            self.reload_values()
            return self._value_names[value]
        raise Exception(
            'Option value {} does not exist for product option {}'.format(
                value, self.option_name))


class ProductOptionValue:

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
