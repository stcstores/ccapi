"""
ShippingRules request.

Get courier shipping rules.
"""

from ccapi.cc_objects import CourierRule

from ..apirequest import APIRequest


class ShippingRules(APIRequest):
    """ShippingRules request."""

    uri = "/Handlers/Configuration/ShippingRules.ashx"

    def __new__(self):
        """Create ShippingRules request."""
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        data = response.json()
        return [CourierRule(order_data) for order_data in data]
