"""Containers for Shipping Rules."""


class CourierRules:
    """Container for courier rules."""

    def __init__(self, courier_rule_data):
        """Add rules."""
        self.json = courier_rule_data
        self.rules = [CourierRule(rule) for rule in courier_rule_data]

    def __iter__(self):
        for rule in self.rules:
            yield rule

    def __getitem__(self, index):
        return self.rules[index]


class CourierRule:
    """Courier Rule."""

    def __init__(self, data=None):
        """
        Create CourierRule.

        Kwargs:
            data: Order data from GetDispatchMethodsForOrder request.
        """
        if data is not None:
            self.load_from_request(data)

    def __str__(self):
        return self.name

    def load_from_request(self, data):
        """Set attributes based on GetDispatchMethodsForOrder request."""
        self.json = data
        self.id = data["ID"]
        if data["ActiveRules"] is None:
            self.active_rules = []
        else:
            self.active_rules = [ActiveRule(data=r) for r in data["ActiveRules"]]
        self.selected = data["Selected"]
        self.rule_applied = data["RuleApplied"]
        self.label_type_enum = data["LabelTypeEnum"]
        self.send_csv_enum = data["SendCSVEnum"]
        self.vat_evavluate_type_enum = data["VATEvaluationTypeEnum"]
        self.brand_id = data["BrandID"]
        self.courier_services_group_id = data["CourierServicesGroupID"]
        self.front_end_price = data["FrontEndPrice"]
        self.name = data["RuleName"]
        self.status_id = data["StatusID"]
        self.status_id_enum = data["StatusIDEnum"]
        self.courier_services_rule_id = data["CourierServicesRuleId"]
        self.baseline_cost = data["BaselineCost"]
        self.brand_courier_selection_type = data["BrandCourierSelectionType"]
        self.country_id = data["CountryId"]
        self.except_country_selected = data["ExceptCountrySelected"]
        self.additional_shipping_label = data["AdditionalShippingLabel"]
        self.initial_weight = data["InitialWeight"]
        self.cost_per_kg = data["CostPerKg"]
        self.label_type = data["LabelType"]
        self.send_csv = data["SendCSV"]
        self.bonus_score = data["BonusScore"]
        self.label_template = data["LabelTemplate"]
        self.vat_value = data["VATValue"]
        self.vat_evaluation_type = data["VATEvaluationType"]
        self.customer_facing_name = data["CustomerFacingName"]
        self.customer_facing_description = data["CustomerFacingDescription"]
        self.signature_value = data["SignatureValue"]
        self.page_size_override = data["PageSizeOverride"]
        self.baseline_weight = data["BaselineWeight"]
        self.rule_courier_account = data["RuleCourierAccount"]
        self.estimated_delivery_days = data["EstDeliveryDays"]
        self.is_priority = data["IsPriority"]
        self.priority_days_to_deliver = data["PriorityDaysToDeliver"]
        self.baseline_weight_max = data["BaselineWeightMax"]
        self.copied_from_id = data["CopiedFromId"]
        self.is_default_rule = data["IsDefaultRule"]


class ActiveRule:
    """Container for active Cloud Commerce shipping rules."""

    def __init__(self, data=None):
        """
        Create ShippingRule.

        Kwargs:
            data: Courier rule data from ShippingRules request.
        """
        if data is not None:
            self.load_from_request(data)

    def load_from_request(self, data):
        """Set attributes based on data from getOrdersForDispatch request."""
        self.json = data
        self.id = data["id"]
        self.brand_id = data["BrandID"]
        self.brand_courier_selection_id = data["BrandCourierSelectionID"]
        self.name = data["RuleName"]
        self.field = data["Field"]
        self.operator = data["Operator"]
        self.value = data["Value"]
        self.status_id = data["StatusId"]
        self.status_id_enum = data["StatusIdEnum"]
        self.is_optional = data["IsOptional"]
