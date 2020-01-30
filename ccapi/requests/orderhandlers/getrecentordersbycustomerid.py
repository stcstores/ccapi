"""
getRecentOrdersByCustomerID request.

Get recent orders for a customer.
"""

from ..apirequest import APIRequest


class GetRecentOrdersByCustomerID(APIRequest):
    """getRecentOrdersByCustomerID request."""

    CUSTOMER_ID = "intCustomerID"

    uri = "Handlers/OrderHandlers/getRecentOrdersByCustomerID.ashx"

    def __new__(self, customer_ID):
        """Create getRecentOrdersByCustomerID request."""
        self.customer_ID = customer_ID
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {self.CUSTOMER_ID: self.customer_ID}
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            f"Error retrieving recent orders for customer ID {self.customer_ID}.",
        )
        return {str(order["ID"]): RecentOrder(order) for order in response.json()}


class RecentOrder:
    """Wrapper for orders returned by GetRecentOrderByCustomerID."""

    DISPATCHED = "Dispatched"
    CANCELLED = "Cancelled"

    ID = "ID"
    COST = "Cost"
    COST_GBP = "CostGBP"
    DATE = "Date"
    EXTERNAL_ORDER_REFERENCE = "ExternalOrderRef"
    IMAGE_URL = "ImageUrl"
    NOTE = "Note"
    QUANTITY = "Quantity"
    REFERENCE = "Reference"
    RETURNED_ITEMS = "ReturnedItems"
    SALES_CHANNEL_NAME = "SalesChannelName"
    STATUS = "Status"

    def __init__(self, json):
        """Set properties."""
        self.json = json
        self.order_id = str(json[self.ID])
        self.cost = json[self.COST]
        self.cost_GBP = json[self.COST_GBP]
        self.date = json[self.DATE]
        self.external_order_reference = json[self.EXTERNAL_ORDER_REFERENCE]
        self.image_URL = json[self.IMAGE_URL]
        self.note = json[self.NOTE]
        self.quantity = json[self.QUANTITY]
        self.reference = json[self.REFERENCE]
        self.returned_items = json[self.RETURNED_ITEMS]
        self.sales_channel = json[self.SALES_CHANNEL_NAME]
        self.status = json[self.STATUS]
