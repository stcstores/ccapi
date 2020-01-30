from ccapi import exceptions
from ccapi.requests import orderhandlers
from ccapi.requests.orderhandlers.getrecentordersbycustomerid import RecentOrder

from .test_request import TestRequest


class TestGetRecentOrdersByCustomerID(TestRequest):
    request_class = orderhandlers.GetRecentOrdersByCustomerID

    CUSTOMER_ID = "30920403"

    RESPONSE = [
        {
            "Cost": "12.99",
            "CostGBP": "7.56",
            "CurrencySymbol": "$",
            "Date": "26 January 2020",
            "ExternalOrderRef": "701-2720067-5257021",
            "ID": 49550044,
            "ImageUrl": "/Images/Default/Icons/OrderCancelled.png",
            "Note": "",
            "Quantity": 2,
            "Reference": "",
            "ReturnedItems": 0,
            "SalesChannelName": "Amazon",
            "SalesChannelTitle": "Seaton Trading Amazon Canada",
            "Status": "Cancelled",
            "Title": "",
        },
        {
            "Cost": "8.49",
            "CostGBP": "5.21",
            "CurrencySymbol": "$",
            "Date": "28 September 2019",
            "ExternalOrderRef": "701-5663724-3180217",
            "ID": 41194697,
            "ImageUrl": "/Images/Default/Icons/OrderDispatched.png",
            "Note": "",
            "Quantity": 1,
            "Reference": "",
            "ReturnedItems": 0,
            "SalesChannelName": "Amazon",
            "SalesChannelTitle": "Seaton Trading Amazon Canada",
            "Status": "Dispatched",
            "Title": "Dispatched on 29/09/2019",
        },
    ]

    def test_GetRecentOrdersByCustomerID_request(self):
        self.register(json=self.RESPONSE)
        response = self.mock_request(self.CUSTOMER_ID)
        self.assertDataSent("intCustomerID", self.CUSTOMER_ID)
        self.assertIsInstance(response, dict)
        for order in self.RESPONSE:
            self.assertIn(str(order["ID"]), response)
            response_order = response[str(order["ID"])]
            self.assertIsInstance(response_order, RecentOrder)
            self.assertEqual(response_order.json, order)
            self.assertEqual(response_order.order_id, str(order[RecentOrder.ID]))
            self.assertEqual(response_order.cost, order[RecentOrder.COST])
            self.assertEqual(response_order.cost_GBP, order[RecentOrder.COST_GBP])
            self.assertEqual(response_order.date, order[RecentOrder.DATE])
            self.assertEqual(
                response_order.external_order_reference,
                order[RecentOrder.EXTERNAL_ORDER_REFERENCE],
            )
            self.assertEqual(response_order.image_URL, order[RecentOrder.IMAGE_URL])
            self.assertEqual(response_order.note, order[RecentOrder.NOTE])
            self.assertEqual(response_order.quantity, order[RecentOrder.QUANTITY])
            self.assertEqual(response_order.reference, order[RecentOrder.REFERENCE])
            self.assertEqual(
                response_order.returned_items, order[RecentOrder.RETURNED_ITEMS]
            )
            self.assertEqual(
                response_order.sales_channel, order[RecentOrder.SALES_CHANNEL_NAME]
            )
            self.assertEqual(response_order.status, order[RecentOrder.STATUS])

    def test_raises_for_non_200(self):
        self.register(json=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(self.CUSTOMER_ID)

    def test_RecentOrder(self):
        data = self.RESPONSE[0]
        order = RecentOrder(data)
        self.assertEqual(order.json, data)
        self.assertEqual(order.order_id, str(data[RecentOrder.ID]))
        self.assertEqual(order.cost, data[RecentOrder.COST])
        self.assertEqual(order.cost_GBP, data[RecentOrder.COST_GBP])
        self.assertEqual(order.date, data[RecentOrder.DATE])
        self.assertEqual(
            order.external_order_reference, data[RecentOrder.EXTERNAL_ORDER_REFERENCE]
        )
        self.assertEqual(order.image_URL, data[RecentOrder.IMAGE_URL])
        self.assertEqual(order.note, data[RecentOrder.NOTE])
        self.assertEqual(order.quantity, data[RecentOrder.QUANTITY])
        self.assertEqual(order.reference, data[RecentOrder.REFERENCE])
        self.assertEqual(order.returned_items, data[RecentOrder.RETURNED_ITEMS])
        self.assertEqual(order.sales_channel, data[RecentOrder.SALES_CHANNEL_NAME])
        self.assertEqual(order.status, data[RecentOrder.STATUS])
