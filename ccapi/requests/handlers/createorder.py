"""
CreateOrder request.

Add a new customer to Cloud Commerce.
"""

import json

from ccapi.requests import APIRequest


class CreateOrder(APIRequest):
    """CreateOrder request."""

    uri = "/Handlers/OrderFromStock/CreateOrder.ashx"

    def __new__(
        self,
        items,
        customer_id=None,
        login_id=None,
        season_id=0,
        channel_id=None,
        reference="",
        order_id=0,
        prep="0",
        delivery_date=None,
        order_note="",
        send_email="0",
        postage_override="",
        carriage_net=0,
        carriage_vat=0,
        total_net=None,
        total_vat=None,
        total_gross=None,
        discount_net=None,
        free_of_charge=False,
        delivery_address_id=None,
        billing_address_id=None,
        shipping_rule_id=None,
    ):
        """Create CreateOrder request."""
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
            "cusID": str(self.customer_id),
            "loginID": str(self.login_id),
            "seasID": str(self.season_id),
            "items": json.dumps([i.to_dict() for i in self.items]),
            "chanID": str(self.channel_id),
            "ref": str(self.reference),
            "ordID": str(self.order_id),
            "prep": str(self.prep),
            "DeliveryDate": self.delivery_date.strftime("%d/%m/%Y"),
            "orderNote": self.order_note,
            "sendEmail": str(int(self.send_email)),
            "PostageOverride": str(self.postage_override),
            "CarriageNet": str(float(self.carriage_net)),
            "CarriageVat": str(float(self.carriage_vat)),
            "TotalNet": str(float(self.total_net)),
            "TotalVat": str(float(self.total_vat)),
            "TotalGross": str(float(self.total_gross)),
            "DiscountNet": str(float(self.discount_net)),
            "isFOCOrder": str(bool(self.free_of_charge)).lower(),
            "BCSID": str(self.shipping_rule_id),
            "deliveryAddressID": str(self.delivery_address_id),
            "billingAddressID": str(self.billing_address_id),
            "CSRID": "411",
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return CreateOrderResponse(response.json())


class NewOrderItem:
    """Continer for items for CreateOrder requests."""

    def __init__(
        self,
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
        parent_product_id="0",
        product_type="0",
    ):
        """Initialise with data."""
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
        self.parent_product_id = str(parent_product_id)
        self.product_type = str(product_type)

    def to_dict(self):
        """Return item data as a dict."""
        return {
            "ProductID": int(self.product_id),
            "ItemQuantity": int(self.quantity),
            "RowCurrency": str(self.currency),
            "ItemNet": self.item_net,
            "ItemGross": self.item_gross,
            "ItemVatRate": self.item_vat_rate,
            "ItemDiscountNet": self.item_discount_net,
            "ItemDiscountGross": self.item_discount_gross,
            "TotalNet": self.total_net,
            "TotalGross": self.total_gross,
            "ParentProductID": str(self.parent_product_id),
            "ProductType": str(self.product_type),
        }

    def to_json(self):
        """Return item data as a JSON encoded string."""
        return json.dumps(self.to_dict())


class CreateOrderResponse:
    """Container for CreateOrder request responses."""

    def __init__(self, response_data):
        """Set attributes from CreateOrder request response."""
        self.error = response_data["error"]
        self.order_id = response_data["orderID"]
        self.invoice_id = response_data["invoiceID"]
        self.payment_term_id = response_data["paymentTermID"]
        self.gateway_type = response_data["gatewayType"]
        self.days_of_credit = response_data["DaysOfCredit"]
        self.reference = response_data["Reference"]
        self.total_gross = response_data["TotalGross"]
        if self.error != "":
            raise ValueError("Order creation returned error: {}".format(self.error))
        if self.order_id == 0:
            raise ValueError("CreateOrder request did not return a valid order ID")
