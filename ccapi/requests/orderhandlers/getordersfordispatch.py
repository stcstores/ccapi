"""
getOrdersForDispatch request.

Get orders ready for dispatch.
"""

import datetime

from ..apirequest import APIRequest


class GetOrdersForDispatch(APIRequest):
    """getOrdersForDispatch request."""

    uri = "/Handlers/OrderHandlers/getOrdersForDispatch.ashx"

    def __new__(
        self,
        date=None,
        order_type=1,
        number_of_days=1,
        customer_type=0,
        courier_rule_id="CourierRule",
        priority="",
        printed="",
        allocated="",
        picked="",
        courier_type="0",
        note_type="",
        external_order_type=0,
        supplier_id="-1",
        dispatch_date="",
        country="",
        warehouse=0,
        sales_channel_id="0",
        id_list="",
        include_products=True,
        search_term="",
        order_by="",
        order_by_direction="",
        first_run=False,
        manual_fetch=True,
        take_limit=200,
        skip_records=0,
        issue_orders=False,
    ):
        """Create getOrdersForDispatch request."""
        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = date
        self.order_type = order_type
        self.number_of_days = number_of_days
        self.customer_type = customer_type
        self.courier_rule_id = courier_rule_id
        self.priority = priority
        self.printed = printed
        self.allocated = allocated
        self.picked = picked
        self.courier_type = courier_type
        self.note_type = note_type
        self.external_order_type = external_order_type
        self.supplier_id = supplier_id
        self.dispatch_date = dispatch_date
        self.country = country
        self.warehouse = warehouse
        self.sales_channel_id = sales_channel_id
        self.id_list = id_list
        self.include_products = include_products
        self.search_term = search_term
        self.order_by = order_by
        self.order_by_direction = order_by_direction
        self.first_run = first_run
        self.manual_fetch = manual_fetch
        self.take_limit = take_limit
        self.skip_records = skip_records
        self.issue_orders = issue_orders
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        if self.issue_orders:
            return {}
        data = {
            "Date": self.date.strftime("%d/%m/%Y"),
            "OrderType": self.order_type,
            "NumberOfDays": self.number_of_days,
            "CustType": self.customer_type,
            "CourierRuleID": self.courier_rule_id,
            "Priority": self.priority,
            "Printed": self.printed,
            "Allocated": self.allocated,
            "Picked": self.picked,
            "CourierType": self.courier_type,
            "NoteType": self.note_type,
            "ExternalOrderType": self.external_order_type,
            "SupplierID": self.supplier_id,
            "DispatchDate": self.dispatch_date,
            "Country": self.country,
            "Warehouse": self.warehouse,
            "SalesChannelID": self.sales_channel_id,
            "idList": self.id_list,
            "IncludeProducts": self.include_products,
            "SearchTerm": self.search_term,
            "OrderBy": self.order_by,
            "OrderByDirection": self.order_by_direction,
            "FirstRun": self.first_run,
            "ManualFetch": self.manual_fetch,
        }
        return data

    def get_headers(self):
        """Get headers for request."""
        headers = {
            "TakeLimit": str(self.take_limit),
            "SkipRecords": str(self.skip_records),
        }
        if self.issue_orders:
            headers["requestmode"] = "issueorders"
        return headers

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "57"}

    def process_response(self, response):
        """Handle request response."""
        data = response.json()
        return [DispatchOrder(order_data) for order_data in data]


class DispatchOrder:
    """Order for dispatch."""

    def __init__(self, data=None):
        """
        Create DispatchOrder.

        Kwargs:
            data: Order data from getOrdersForDispatch request.
        """
        if data is not None:
            self.load_from_request(data)

    def load_from_request(self, data):
        """Set attributes based on data from getOrdersForDispatch request."""
        self.json = data
        self.order_id = data["OrderID"]
        self.is_pick_list_printed = data["isPickListPrinted"]
        self.priority = data["Priority"]
        self.customer_id = data["CustomerID"]
        self.login_id = data["LoginID"]
        self.company_name = data["CompanyName"]
        self.trading_name = data["TradingName"]
        self.date_recieved = self.to_datetime(data["DateReceived"])
        self.dispatch_date = self.to_datetime(data["DispatchDate"])
        self.note = data["Note"]
        self.pick_list_printed = data["PickListPrinted"]
        self.total_gross = data["TotalGross"]
        self.total_gross_gbp = data["TotalGrossGBP"]
        self.default_cs_rule_id = data["DefaultCSRuleId"]
        self.default_rule_cost_gbp = data["DefaultCSRuleCostGBP"]
        self.default_cs_rule_name = data["DefaultCSRuleName"]
        self.cancelled = data["Cancelled"]
        self.unpaied = data["Unpaid"]
        self.items_left_to_dispatch = data["ItemsLeftToDispatch"]
        self.items_count = data["ItemsCount"]
        self.intended_for_courier = data["IntendedForCourier"]
        self.predicted_order_weight = data["PredictedOrderWeight"]
        self.channel_name = data["ChannelName"]
        self.external_order_type_name = data["ExternalOrderTypeName"]
        self.sales_channel_name = data["SalesChannelName"]
        self.country_code = data["countrycode"]
        self.delivery_country_code = data["deliverycountrycode"]
        self.delivery_name = data["DeliveryName"]
        self.delivery_name_from_udf = data["DeliveryNameFromUDF"]
        self.address_conflict = data["AddressConflict"]
        self.delilvery_address = data["DeliveryAddress"]
        self.delivery_user_id = data["DeliveryUserID"]
        self.has_unallocated_items = data["HasUnallocatedItems"]
        self.can_process_order = data["CanProcessOrder"]
        self.on_watch_list = data["OnWatchList"]
        self.watch_list_reason = data["WatchListReason"]
        self.pick_status = data["PickStatus"]
        self.external_transaction_id = data["ExternalTransactionID"]
        self.esimated_delivery_days = data["EstDeliveryDays"]
        self.products = [DispatchOrderProduct(product) for product in data["Products"]]
        self.factory_ids = data["FactoryIds"]
        self.is_exported = data["IsExported"]
        self.exported_date = data["ExportedDate"]
        self.delivery_date = data["DeliveryDate"]
        self.dispatch_order_by = data["DispatchOrderBy"]
        self.delivery_from = data["DeliveryFrom"]
        self.delivery_to = data["DeliveryTo"]
        self.ranged_delivery = data["RangedDelivery"]
        self.customer_type = data["CustomerType"]
        self.rule_base_weight = data["RuleBaseWeight"]
        self.creation_date = data["CreationDate"]
        self.hide_until_date = data["HideUntilDate"]
        self.tracking_code = data["TrackingCode"]
        self.assigned_to_warehouse_id = data["AssignedToWarehouseId"]
        self.item_summary = data["ItemSummary"]

    def to_datetime(self, date_time_string):
        """Return recieved date string as datetime.datetime object."""
        date, time = date_time_string.split(" ")
        day, month, year = date.split("/")
        hour, minute = time.split(":")
        return datetime.datetime(
            day=int(day),
            month=int(month),
            year=int(year),
            hour=int(hour),
            minute=int(minute),
        )


class DispatchOrderProduct:
    """Product associated with an order ready for dispatch."""

    def __init__(self, data=None):
        """
        Create DispatchOrderProduct.

        kwargs:
            data: dict containing data for dispatch order product from
            DispatchOrderProduct request.
        """
        if data is not None:
            self.load_from_request(data)

    def load_from_request(self, data):
        """Set attributes based on data from DispatchOrderProduct request."""
        self.json = data
        self.id = data["intID"]
        self.price = float(data["strPrice"])
        self.customer_order_id = data["strCustomerOrderID"]
        self.product_id = data["strProductID"]
        self.product_range_id = data["strProductRangeID"]
        self.product_name = data["strProductName"]
        self.product_full_name = data["strProductFullName"]
        self.barcode = data["strBarCodeNumber"]
        self.image_url = data["strImageUrl"]
        self.customer_id = data["CustomerID"]
        self.customer_name = data["CustomerName"]
        self.pending_dispatch = data["pendingDispatch"]
        self.sku = data["SKU"]
        self.quantity = data["Quantity"]
        self.dispatched = data["Dispatched"]
        self.allocated = data["Allocated"]
        self.can_process_item = data["CanProcessItem"]
        self.amount_sent_to_channel = data["AmountSentToChannel"]
        self.expected_delivery_date = data["ExpectedDeliveryDate"]
        self.item_handling_time = data["ItemHandlingTime"]
        self.parent_product_id = data["ParentProductID"]
        self.parent_product_range_id = data["ParentProductRangeID"]
        self.parent_product_name = data["ParentProductName"]
        self.order_item_product_type = data["OrderItemProductType"]
        self.current_stock_level = data["CurrentStockLevel"]
        self.per_item_weight = data["PerItemWeight"]
        self.gift_message = data["GiftMessage"]
        self.bay_locations = data["BayLocations"]
        self.listing_id = data["ListingID"]
        self.pick_from_wearehouse_by_id = data["PickFromWarehouseBayId"]
        self.pick_from_warehouse_id = data["PickFromWarehouseId"]
