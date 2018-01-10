"""
GetDispatchMethodsForOrder request.

Get orders ready for dispatch.
"""

from ccapi.inventoryitems import CourierRule

from ..apirequest import APIRequest


class GetDispatchMethodsForOrder(APIRequest):
    """GetDispatchMethodsForOrder request."""

    uri = '/Handlers/OrderHandlers/GetDispatchMethodsForOrder.ashx'

    def __new__(self, order_id, analyse=True):
        """Create GetDispatchMethodsForOrder request."""
        self.order_id = order_id
        self.analyse = True
        return super().__new__(self)

    def get_params(self):
        """Get parameters for get request."""
        return {'orderid': self.order_id, 'analyse': self.analyse}

    def process_response(self, response):
        """Handle request response."""
        data = response.json()
        return DispatchMethods(data)


class DispatchMethods:
    """Order dispatch methods."""

    def __init__(self, data=None):
        """
        Create DispatchMethods.

        Kwargs:
            data: Order data from GetDispatchMethodsForOrder request.
        """
        if data is not None:
            self.load_from_request(data)

    def __iter__(self):
        for method in self.dispatch_methods:
            yield method

    def __getitem__(self, key):
        return self.dispatch_methods[key]

    def load_from_request(self, data):
        """Set attributes based on GetDispatchMethodsForOrder request."""
        self.json = data
        self.dispatch_methods = [DispatchMethod(method) for method in data]
        self.courier_rules = [d.courier_rule for d in self.dispatch_methods]


class DispatchMethod:
    """Order dispatch method."""

    def __init__(self, data=None):
        """
        Create DispatchMethod.

        Kwargs:
            data: Order data from GetDispatchMethodsForOrder request.
        """
        if data is not None:
            self.load_from_request(data)

    def load_from_request(self, data):
        """Set attributes based on GetDispatchMethodsForOrder request."""
        self.passed_filters = data['passedFilters']
        self.courier_rule = CourierRule(data['CourierRule'])
        self.rule_type = data['RuleType']
        self.match_score = data['MatchScore']
        self.matched_rules = data['MatchedRules']
        self.failed_rules = data['FailedRules']
        self.total_rules = data['TotalRules']
        self.courier_match_cost = data['CourierMatchCost']
        self.shipping_label_count = data['ShippingLabelCount']
        self.total_shipping_label_estimate = data['TotalShippingLabelEstimate']
        self.bonus_score = data['BonusScore']
        self.failed_rules_descriptions = data['FailedRulesDescriptions']
        self.best_matching_courier_rule = data['BestMatchingCourierRule']
