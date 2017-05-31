from . ccapisession import APIRequest


class FindProductSelectedOptionsOnly(APIRequest):
    uri = 'Handlers/Products/findProductSelectedOptionsOnly.ashx'

    def __new__(self, product_id, channel_id=0):
        self.product_id = product_id
        self.channel_id = channel_id
        return super().__new__(self)

    def get_data(self):
        return {'ProductID': self.product_id, 'channelID': self.channel_id}

    def process_response(self, response):
        results = response.json()
        return FindProductSelectedOptionsOnlyResult(results)


class FindProductSelectedOptionsOnlyResult:

    def __init__(self, data):
        self.stock_level = data['StockLevel']
        self.fba_stock_level = data['FBAStockLevel']
        self.product = Product(data['product'])
        self.options = [Option(option) for option in data['options']]


class Product:

    def __init__(self, data):
        self.is_checked = data['isChecked']
        self.is_listed = data['isListed']
        self.supplier_sku = data['SupplierSKU']
        self.id = data['ID']
        self.name = data['Name']
        self.full_name = data['FullName']
        self.options = data['Options']
        self.description = data['Description']
        self.manufacturer_sku = data['ManufacturerSKU']
        self.base_price = data['BasePrice']
        self.vat_rate_id = data['VatRateID']
        self.vat_rate = data['VatRate']
        self.barcode = data['Barcode']
        self.range_id = data['RangeID']
        self.range_name = data['RangeName']
        self.pre_order = data['PreOrder']
        self.end_of_line = data['EndOfLine']
        self.stock_level = data['StockLevel']
        self.pseudo_stock_type = data['PseudoStockType']
        self.pseudo_stock_level = data['PseudoStockLevel']
        self.status_id = data['StatusID']
        self.product_type = data['ProductType']
        self.length_mm = data['LengthMM']
        self.width_mm = data['WidthMM']
        self.height_mm = data['HeightMM']
        self.length_cm = data['LengthCM']
        self.width_cm = data['WidthCM']
        self.height_cm = data['HeightCM']
        self.large_letter_compatible = data['LargeLetterCompatible']
        self.external_product_id = data['ExternalProductId']
        self.additional_shipping_label = data['AdditionalShippingLabel']
        self.default_image_url = data['defaultImageUrl']
        self.delivery_lead_time = data['DeliveryLeadTimeDays']
        self.product_template_id = data['ProductTemplateId']
        self.product_template_mode = data['ProductTemplateMode']
        self.additional_barcodes = data['AdditionalBarcodes']
        self.locations = data['Locations']
        self.dimensions = data['Dimensions']


class Option:

    def __init__(self, data):
        self.id = data['ID']
        self.option_name = data['OptionName']
        self.option_ebay_name = data['OptionEbayName']
        self.option_amazon_name = data['OptionAmazonName']
        self.option_pretty_name = data['OptionPrettyName']
        self.option_web_name = data['OptionWebName']
        self.option_sort_order = data['OptionSortOrder']
        self.option_type = data['OptionType']
        self.master = data['Master']
        self.hidden = data['Hidden']
        self.pre_select_on_create_range = data['PreSelectOnCreateRange']
        self.status = data['Statusw']
        self.exclude_amazon = data['excludeAmazon']
        self.exclude_ebay = data['excludeEbay']
        self.exclude_market_place = data['excludeMarketPlace']
        self.exclude_epos = data['excludeEpos']
        self.exclude_magento = data['excludeMagento']
        self.exclude_woo_commerce = data['excludeWooCommerce']
        self.exclude_shopify = data['excludeShopify']
        self.exclude_tesco = data['excludeTesco']
        self.exclude_google = data['excludeGoogle']
        self.selected = data['Selected']
        self.option_values = [
            OptionValues(option) for option in data['optionValues']]


class OptionValues:

    def __init__(self, data):
        self.id = data['ID']
        self.brand_id = data['BrandID']
        self.option_id = data['OptionID']
        self.option_value = data['OptionValue']
        self.option_value_trans = data['OptionValueTrans']
        self.option_sort_order = data['OptionsortOrder']
        self.selected = data['Selected']
        self.product_count = data['ProductCount']
        self.option_name = data['OptionName']
