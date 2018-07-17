"""The SalesChannel class."""


class SalesChannel:
    """Container for Cloud Commerce Sales Channels."""

    def __init__(self, data):
        """Set attributes from API data."""
        self.json = data
        self.id = data.get('ID', None)
        self.name = data.get('Name', None)
        self.domain = data.get('Domain', None)
        self.brand_id = data.get('BrandID', None)
        self.account_id = data.get('AccountID', None)
        self.brand_name = data.get('BrandName', None)
        self.country_id = data.get('CountryID', None)
        self.country_name = data.get('CountryName', None)
        self.account_name = data.get('AccountName', None)
        self.pre_order = data.get('PreOrder', None)
        self.type_id = data.get('TypeID', None)
        self.type_name = data.get('TypeName', None)
        self.nominal_code_id = data.get('NominalCodeID', None)
        self.external_shop_id = data.get('ExtShopID', None)
        self.pseudo_stock_level_type = data.get('PseudoStockLevelType', None)
        self.currency_symbol = data.get('CurrencySymbol', None)
        self.loyalty_point_per_value = data.get('LoyaltyPointPerValue', None)
        self.loyalty_value_per_point = data.get('LoyaltyValuePerPoint', None)
        self.disabled = data.get('disabled', None)
        self.deleted = data.get('deleted', None)
        self.note = data.get('Note', None)

    def __repr__(self):
        return 'Sales Channel: {}'.format(self.name)
