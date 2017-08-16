"""This module contains classes for working with Product Options."""

from ccapi import ccapi
import time


class MetaProductOptions(type):
    """Meta class for ProductOptions class."""

    def __iter__(self):
        for option in self.options:
            yield option

    def __getitem__(self, index):
        return self.option_names[index]

    @property
    def options(self):
        """Return all Product Options."""
        if self._options is None:
            self._options = ccapi.CCAPI.get_product_options()
        return self._options

    @property
    def option_names(self):
        """Return dict organising Product Options by name."""
        if self._option_names is None:
            self._option_names = {
                option.option_name: option for option in self.options}
        return self._option_names


class ProductOptions(metaclass=MetaProductOptions):
    """Class for working with groups of Product Options."""

    _options = None
    _option_names = None

    def __init__(self, options):
        """Create ProductOptions object.

        Args:
            options: list containg ProductOption objects.
        """
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
    """Wrapper for Product Options."""

    _values = None
    _value_names = None

    def __init__(self, result):
        """
        Create Product Option object.

        Args:
            result: Cloud Commerce Product Option JSON object.
        """
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
        self.set_value(result)

    def set_value(self, result):
        """Set Option Values."""
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
        """Return list of Values belonging to this Product Option."""
        if self._values is None:
            self.reload_values()
        return self._values

    @property
    def value_names(self):
        """Return dict organising Values by name."""
        if self._value_names is None:
            self._value_names = self.load_value_names()
        return self._value_names

    def load_value_names(self):
        """Return dict organising Values by name."""
        return {value.value: value for value in self.values}

    def reload_values(self):
        """Get Product Option Values for this Product Option."""
        self._values = ccapi.CCAPI.get_option_values(self.id)
        self._value_names = self.load_value_names()

    def add_value(self, value):
        """
        Create Product Option Value for this Product Option.

        Args:
            value: New value.

        Returns: (str) ID of new Product Option Value.

        """
        if ccapi.CCAPI.get_option_value_id(self.id, value) is not None:
            raise Exception(
                'Option Value {} already exists for product option {}'.format(
                    self.option_name, value))
        ccapi.CCAPI.create_option_value(self.id, value)
        time.sleep(0.5)
        self.reload_values()
        return ccapi.CCAPI.get_product_option_id(value)

    def get_value(self, value, create=False):
        """
        Get ID of Product Option Value by name for this Product Option.

        Args:
            value: Product Option Value to find.

        Kwargs:
            create: If True the Product Option Value will be added to the
                Product Option. Default: False.

        Returns: (str) ID of Product Option Value or None.

        """
        if value in self.value_names:
            return self.value_names[value]
        if create is True:
            self.add_value(value)
            self.reload_values()
            return self._value_names[value]
        raise Exception(
            'Option value {} does not exist for product option {}'.format(
                value, self.option_name))


class ProductOptionValue:
    """Class for working with Product Option Values."""

    def __init__(self, result):
        """
        Create ProductOptionValue object.

        Args:
            result: Cloud Commerce Product Option Value JSON object.
        """
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

    def delete(self):
        """Delete this Product Option Value."""
        ccapi.CCAPI.delete_product_option_value(self.id)
        del self


class AppliedProductOptions(ProductOptions):
    """Container for AppliedProductOptions."""

    def __init__(self, options):
        """Create AppliedProductOptions object.

        Args:
            options: list containg ProductOption objects.
        """
        self.options = [
            AppliedProductOption(option_data) for option_data in options]
        self.option_names = {
            option.option_name: option for option in self.options}

    def __repr__(self):
        return(str(self.options))


class AppliedProductOption(ProductOption):
    """Wrapper for Product Options applied to a Product."""

    def set_value(self, option_data):
        """Set Option Values."""
        if len(option_data['optionValues']) > 0:
            self.value = AppliedProductOptionValue(
                option_data['optionValues'][0])
        else:
            self.value = None

    def __repr__(self):
        return '{}: {}'.format(self.option_name, self.value)


class AppliedProductOptionValue(ProductOptionValue):
    """Container for Product Option values applied to a product."""

    def __repr__(self):
        return self.value

    def delete(self):
        """Product Option Values should not be deleted from here."""
        raise NotImplementedError
