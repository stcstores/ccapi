"""
CreateOrder request.

Add a new customer to Cloud Commerce.
"""

import json

from ccapi.exceptions import CloudCommerceResponseError
from ccapi.requests import APIRequest


class CreateOrder(APIRequest):
    """CreateOrder request."""

    uri = "Handlers/OrderFromStock/CreateOrder.ashx"

    CUSTOMER_ID = "cusID"
    LOGIN_ID = "loginID"
    SEASON_ID = "seasID"
    ITEMS = "items"
    CHANNEL_ID = "chanID"
    REFERENCE = "ref"
    ORDER_ID = "ordID"
    PREP = "prep"
    DELIVERY_DATE = "DeliveryDate"
    ORDER_NOTE = "orderNote"
    SEND_EMAIL = "sendEmail"
    POSTAGE_OVERRIDE = "PostageOverride"
    CARRIAGE_NET = "CarriageNet"
    CARRIAGE_VAT = "CarriageVat"
    TOTAL_NET = "TotalNet"
    TOTAL_VAT = "TotalVat"
    TOTAL_GROSS = "TotalGross"
    DISCOUNT_NET = "DiscountNet"
    FREE_OF_CHARGE = "isFOCOrder"
    SHIPPING_RULE_ID = "BCSID"
    DELIVERY_ADDRESS_ID = "deliveryAddressID"
    BILLING_ADDRESS_ID = "billingAddressID"
    CSRID = "CSRID"
    CSRID_VALUE = "411"

    def __new__(
        self,
        *,
        customer_id,
        items,
        delivery_address_id,
        billing_address_id,
        delivery_date,
        season_id=0,
        channel_id="",
        reference="",
        order_id=0,
        prep="0",
        order_note="",
        send_email=0,
        postage_override="",
        carriage_net=0,
        carriage_vat=0,
        total_net=0,
        total_vat=0,
        total_gross=0,
        discount_net=0,
        free_of_charge=False,
        shipping_rule_id=None,
        login_id=None,
    ):
        """Create a CreateOrder request."""
        self.items = items
        self.customer_id = customer_id
        self.login_id = login_id
        self.season_id = season_id
        self.channel_id = channel_id
        self.reference = reference
        self.order_id = order_id
        self.prep = prep
        self.delivery_date = delivery_date
        self.order_note = order_note
        self.send_email = send_email
        self.postage_override = postage_override
        self.carriage_net = carriage_net
        self.carriage_vat = carriage_vat
        self.total_net = total_net
        self.total_vat = total_vat
        self.total_gross = total_gross
        self.discount_net = discount_net
        self.free_of_charge = free_of_charge
        self.delivery_address_id = delivery_address_id
        self.billing_address_id = billing_address_id
        self.shipping_rule_id = shipping_rule_id
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {
            self.CUSTOMER_ID: str(self.customer_id),
            self.LOGIN_ID: self.login_id or 0,
            self.SEASON_ID: str(self.season_id),
            self.ITEMS: json.dumps([i.to_dict() for i in self.items]),
            self.CHANNEL_ID: str(self.channel_id),
            self.REFERENCE: str(self.reference),
            self.ORDER_ID: str(self.order_id),
            self.PREP: str(self.prep),
            self.DELIVERY_DATE: self.delivery_date.strftime("%d/%m/%Y"),
            self.ORDER_NOTE: self.order_note,
            self.SEND_EMAIL: str(int(self.send_email)),
            self.POSTAGE_OVERRIDE: str(self.postage_override),
            self.CARRIAGE_NET: str(float(self.carriage_net)),
            self.CARRIAGE_VAT: str(float(self.carriage_vat)),
            self.TOTAL_NET: str(float(self.total_net)),
            self.TOTAL_VAT: str(float(self.total_vat)),
            self.TOTAL_GROSS: str(float(self.total_gross)),
            self.DISCOUNT_NET: str(float(self.discount_net)),
            self.FREE_OF_CHARGE: str(bool(self.free_of_charge)).lower(),
            self.SHIPPING_RULE_ID: str(self.shipping_rule_id),
            self.DELIVERY_ADDRESS_ID: str(self.delivery_address_id),
            self.BILLING_ADDRESS_ID: str(self.billing_address_id),
            self.CSRID: self.CSRID_VALUE,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, f"Failed to create order.")
        response = CreateOrderResponse(response.json())
        if response.error != "":
            raise CloudCommerceResponseError(
                f"Order creation returned error: {response.error}"
            )
        if response.order_id == 0:
            raise CloudCommerceResponseError(
                "CreateOrder request did not return a valid order ID"
            )
        return response


class NewOrderItem:
    """Continer for items for CreateOrder requests."""

    PRODUCT_ID = "ProductID"
    QUANTITY = "ItemQuantity"
    CURRENCY = "RowCurrency"
    ITEM_NET = "ItemNet"
    ITEM_GROSS = "ItemGross"
    ITEM_VAT_RATE = "ItemVatRate"
    ITEM_DISCOUNT_NET = "ItemDiscountNet"
    ITEM_DISCOUNT_GROSS = "ItemDiscountGross"
    TOTAL_NET = "TotalNet"
    TOTAL_GROSS = "TotalGross"
    PARENT_PRODUCT_ID = "ParentProductID"
    PRODUCT_TYPE = "ProductType"
    PARENT_PRODUCT_ID_VALUE = "0"
    PRODUCT_TYPE_VALUE = "0"

    def __init__(
        self,
        *,
        product_id,
        quantity=1,
        currency="£",
        item_net=0,
        item_gross=0,
        item_vat_rate=5,
        item_discount_net=0,
        item_discount_gross=0,
        total_net=0,
        total_gross=0,
    ):
        """
        Create an item to be passed to a CreateOrder request.

        Kwargs:
            product_id (int)(required): The product ID of the product to be added to
                the order.
            quantity (int): The quantity of the product to add to the order. Default: 1.
            currency (str): The currency symbol for the currency used in the transaction.
                Default: "£".
            item_net (float): The net cost per item.
            item_gross (float): The gross per item.
            item_vat_rate (int): The VAT rate ID of the VAT rate charged on the item.
                (Default: 5 (20%))
            item_discount_net (float): The net discount per item.
            item_discount_gross (float): The gross discount per item.
            total_net (float): The net cost of all instances of this item ordered.
            total_gross (float): The gross cost of all instances of this item ordered.
        """
        self.product_id = product_id
        self.quantity = quantity
        self.currency = currency
        self.item_net = item_net
        self.item_gross = item_gross
        self.item_vat_rate = item_vat_rate
        self.item_discount_net = item_discount_net
        self.item_discount_gross = item_discount_gross
        self.total_net = total_net
        self.total_gross = total_gross

    def to_dict(self):
        """Return item data as a dict."""
        return {
            self.PRODUCT_ID: int(self.product_id),
            self.QUANTITY: int(self.quantity),
            self.CURRENCY: str(self.currency),
            self.ITEM_NET: self.item_net,
            self.ITEM_GROSS: self.item_gross,
            self.ITEM_VAT_RATE: self.item_vat_rate,
            self.ITEM_DISCOUNT_NET: self.item_discount_net,
            self.ITEM_DISCOUNT_GROSS: self.item_discount_gross,
            self.TOTAL_NET: self.total_net,
            self.TOTAL_GROSS: self.total_gross,
            self.PARENT_PRODUCT_ID: self.PARENT_PRODUCT_ID_VALUE,
            self.PRODUCT_TYPE: self.PRODUCT_TYPE_VALUE,
        }

    def to_json(self):
        """Return item data as a JSON encoded string."""
        return json.dumps(self.to_dict())


class CreateOrderResponse:
    """Wrapper for CreateOrder request responses."""

    ERROR = "error"
    ORDER_ID = "orderID"
    INVOICE_ID = "invoiceID"
    PAYMENT_TERM_ID = "paymentTermID"
    GATEWAY_TYPE = "gatewayType"
    DAYS_OF_CREDIT = "DaysOfCredit"
    REFERENCE = "Reference"
    TOTAL_GROSS = "TotalGross"

    def __init__(self, response_data):
        """Set attributes from CreateOrder request response."""
        self.error = response_data[self.ERROR]
        self.order_id = response_data[self.ORDER_ID]
        self.invoice_id = response_data[self.INVOICE_ID]
        self.payment_term_id = response_data[self.PAYMENT_TERM_ID]
        self.gateway_type = response_data[self.GATEWAY_TYPE]
        self.days_of_credit = response_data[self.DAYS_OF_CREDIT]
        self.reference = response_data[self.REFERENCE]
        self.total_gross = response_data[self.TOTAL_GROSS]
