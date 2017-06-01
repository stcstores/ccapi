from . ccapisession import APIRequest


class GetOptions(APIRequest):
    uri = 'Handlers/ProductOption/getOptions.ashx'

    def process_response(self, response):
        print(response.text)
        results = response.json()
        return [GetOptionsResult(item) for item in results]

    def get_data(self):
        return {
            'brandID': "341",
            'strOptionTypes': "1,+2,+6"}


class GetOptionsResult:
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
        self.values = result['optionValues']

    def __repr__(self):
        return self.option_name
