"""Tests for handler requests."""

import datetime
import json
import unittest

from ccapi import NewOrderItem, exceptions
from ccapi.requests import handlers

from .test_request import TestRequest


class TestAddCustomer(TestRequest):
    """Tests for the AddCustomer request."""

    request_class = handlers.AddCustomer

    CUSTOMER_ID = "18495409"
    RESPONSE = f"Company Created for Company Name^^{CUSTOMER_ID}"

    ACCOUNT_NAME = "Account 001"
    ADDRESS_1 = "1 Way Street"
    ADDRESS_2 = "Villageton"
    AGENT_ID = 3
    COMPANY_FAX = "02135 465135"
    COMPANY_MOBILE = "09135 453 901"
    COMPANY_TELEPHONE = "132485 63156"
    CONTACT_EMAIL = "contact@nowhere.com"
    CONTACT_FAX = "15441 8464 6541"
    CONTACT_MOBILE = "09874 751 665"
    CONTACT_NAME = "Contact Test Customer"
    CONTACT_PHONE = "01324 164861"
    COUNTRY = "United Kingdom"
    COUNTY = "Townshire"
    CUSTOMER_NAME = "Test Customer"
    CUSTOMER_TYPE = 6
    EU_VAT = False
    POST_CODE = "ES23 5LN"
    PAYMENT_TERMS = 3
    SELLING_CHANNEL_ID = "3541"
    SPECIAL_INSTRUCTIONS_NOTE = "Leave packages in Porch."
    TOWN = "Townsville"
    TRADE_NAME = "Shop Co."
    VAT_NUMBER = "8759453"
    CREDIT_LIMIT = 7

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_AddCustomer_returns_customer_ID(self):
        """Test the AddCustomer request returns a customer ID."""
        response = self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertEqual(response, self.CUSTOMER_ID)

    def test_AddCustomer_request_sends_required_parameters(self):
        """Test the AddCustomer request sends required parameters."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataValueIsNone("AccountID", None)
        self.assertDataSent(self.request_class.CUSTOMER_NAME, self.CUSTOMER_NAME)
        self.assertDataSent(self.request_class.ADDRESS_1, self.ADDRESS_1)
        self.assertDataSent(self.request_class.COUNTRY, self.COUNTRY)
        self.assertDataSent(
            self.request_class.SELLING_CHANNEL_ID, self.SELLING_CHANNEL_ID
        )
        self.assertDataSent(self.request_class.CREATE, 0)
        self.assertDataSent(self.request_class.LINK_TO, 0)
        self.assertDataSent(self.request_class.OSCID, 0)

    def test_AddCustomer_request_sends_optional_parameters(self):
        """Test the AddCustomer request sends optional parameters."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            account_name=self.ACCOUNT_NAME,
            address_2=self.ADDRESS_2,
            agent_id=self.AGENT_ID,
            company_fax=self.COMPANY_FAX,
            company_mobile=self.COMPANY_MOBILE,
            company_telephone=self.COMPANY_TELEPHONE,
            contact_email=self.CONTACT_EMAIL,
            contact_fax=self.CONTACT_FAX,
            contact_mobile=self.CONTACT_MOBILE,
            contact_name=self.CONTACT_NAME,
            contact_phone=self.CONTACT_PHONE,
            county=self.COUNTY,
            customer_type=self.CUSTOMER_TYPE,
            eu_vat=self.EU_VAT,
            post_code=self.POST_CODE,
            payment_terms=self.PAYMENT_TERMS,
            town=self.TOWN,
            trade_name=self.TRADE_NAME,
            vat_number=self.VAT_NUMBER,
            credit_limit=self.CREDIT_LIMIT,
        )
        self.assertDataSent(self.request_class.ACCOUNT_NAME, self.ACCOUNT_NAME)
        self.assertDataSent(self.request_class.ADDRESS_2, self.ADDRESS_2)
        self.assertDataSent(self.request_class.AGENT_ID, self.AGENT_ID)
        self.assertDataSent(self.request_class.COMPANY_FAX, self.COMPANY_FAX)
        self.assertDataSent(self.request_class.COMPANY_MOBILE, self.COMPANY_MOBILE)
        self.assertDataSent(
            self.request_class.COMPANY_TELEPHONE, self.COMPANY_TELEPHONE
        )
        self.assertDataSent(self.request_class.CONTACT_EMAIL, self.CONTACT_EMAIL)
        self.assertDataSent(self.request_class.CONTACT_FAX, self.CONTACT_FAX)
        self.assertDataSent(self.request_class.CONTACT_MOBILE, self.CONTACT_MOBILE)
        self.assertDataSent(self.request_class.CONTACT_NAME, self.CONTACT_NAME)
        self.assertDataSent(self.request_class.CONTACT_PHONE, self.CONTACT_PHONE)
        self.assertDataSent(self.request_class.COUNTY, self.COUNTY)
        self.assertDataSent(self.request_class.CUSTOMER_TYPE, self.CUSTOMER_TYPE)
        self.assertDataSent(self.request_class.EU_VAT, int(bool(self.EU_VAT)))
        self.assertDataSent(self.request_class.POST_CODE, self.POST_CODE)
        self.assertDataSent(self.request_class.PAYMENT_TERMS, self.PAYMENT_TERMS)
        self.assertDataSent(self.request_class.TOWN, self.TOWN)
        self.assertDataSent(self.request_class.TRADE_NAME, self.TRADE_NAME)
        self.assertDataSent(self.request_class.VAT_NUMBER, self.VAT_NUMBER)
        self.assertDataSent(self.request_class.CREDIT_LIMIT, self.CREDIT_LIMIT)

    def test_AddCustomer_request_sends_special_instructions(self):
        """Test the AddCustomer request sends special instructions."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            special_instructions=self.SPECIAL_INSTRUCTIONS_NOTE,
        )
        self.assertDataSent(self.request_class.SPECIAL_INSTRUCTIONS, 1)
        self.assertDataSent(
            self.request_class.SPECIAL_INSTRUCTIONS_NOTE, self.SPECIAL_INSTRUCTIONS_NOTE
        )

    def test_AddCustomer_request_without_special_instructions(self):
        """Test False is send for special instructions when no note is passed."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            special_instructions=None,
        )
        self.assertDataSent(self.request_class.SPECIAL_INSTRUCTIONS, 0)
        self.assertDataValueIsNone(self.request_class.SPECIAL_INSTRUCTIONS_NOTE, None)

    def test_trade_name_defaults_to_customer_name(self):
        """Test the trade_name parameter defaults to the customer name."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            trade_name=None,
        )
        self.assertDataSent(self.request_class.CUSTOMER_NAME, self.CUSTOMER_NAME)
        self.assertDataSent(self.request_class.TRADE_NAME, self.CUSTOMER_NAME)

    def test_contact_name_defaults_to_customer_name(self):
        """Test the contact_name parameter defaults to the customer name."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            contact_name=None,
        )
        self.assertDataSent(self.request_class.CUSTOMER_NAME, self.CUSTOMER_NAME)
        self.assertDataSent(self.request_class.CONTACT_NAME, self.CUSTOMER_NAME)

    def test_AddCustomer_raises_for_non_200_response(self):
        """Test the AddCustomer request raises for a non 200 response status code."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                customer_name=self.CUSTOMER_NAME,
                address_1=self.ADDRESS_1,
                country=self.COUNTRY,
                selling_channel_id=self.SELLING_CHANNEL_ID,
            )


class TestCreateOrderRequest(TestRequest):
    """Tests for the Create Order request."""

    request_class = handlers.CreateOrder

    RETURNED_ERROR = ""
    RETURNED_ORDER_ID = 21232732
    RETURNED_INVOICE_ID = 17288332
    RETURNED_PAYMENT_TERM_ID = 1
    RETURNED_GATEWAY_TYPE = "PayPal"
    RETURNED_DAYS_OF_CREDIT = 0
    RETURNED_REFERENCE = ""
    RETURNED_TOTAL_GROSS = 17.15

    ITEMS = [
        NewOrderItem(
            product_id=4176861,
            item_net=12.5,
            item_gross=15,
            total_net=12.5,
            total_gross=15,
        ),
        NewOrderItem(
            product_id=3176869,
            item_net=13.12,
            item_gross=19,
            total_net=22.5,
            total_gross=18,
        ),
    ]

    RESPONSE = {
        handlers.createorder.CreateOrderResponse.ERROR: RETURNED_ERROR,
        handlers.createorder.CreateOrderResponse.ORDER_ID: RETURNED_ORDER_ID,
        handlers.createorder.CreateOrderResponse.INVOICE_ID: RETURNED_INVOICE_ID,
        handlers.createorder.CreateOrderResponse.PAYMENT_TERM_ID: RETURNED_PAYMENT_TERM_ID,
        handlers.createorder.CreateOrderResponse.GATEWAY_TYPE: RETURNED_GATEWAY_TYPE,
        handlers.createorder.CreateOrderResponse.DAYS_OF_CREDIT: RETURNED_DAYS_OF_CREDIT,
        handlers.createorder.CreateOrderResponse.REFERENCE: RETURNED_REFERENCE,
        handlers.createorder.CreateOrderResponse.TOTAL_GROSS: RETURNED_TOTAL_GROSS,
    }

    CUSTOMER_ID = 18495409
    DELIVERY_ADDRESS_ID = 134864315
    BILLING_ADDRESS_ID = 786315135
    DELIVERY_DATE = datetime.datetime.now()
    LOGIN_ID = 134876131
    SEASON_ID = 5
    CHANNEL_ID = 3151
    ORDER_NOTE = "Order Note text"
    SEND_EMAIL = 1
    CARRIAGE_NET = 3.65
    CARRIAGE_VAT = 15.87
    TOTAL_NET = 15.84
    TOTAL_VAT = 12.80
    TOTAL_GROSS = 2.90
    DISCOUNT_NET = 1.50
    FREE_OF_CHARGE = True
    SHIPPING_RULE_ID = 487315
    REFERENCE = "reference value"
    PREP = "prep value"
    POSTAGE_OVERRIDE = "postage override value"
    ORDER_ID = 154313143

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(json=self.RESPONSE)

    def test_CreateOrder_returns_CreateOrderResponse(self):
        """Test CreateOrder returns an instance of CreateOrderResponse."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertIsInstance(response, handlers.createorder.CreateOrderResponse)

    def test_CreateOrder_required_parameters(self):
        """Test the CreateOrder request sends a customer ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(self.request_class.CUSTOMER_ID, self.CUSTOMER_ID)
        self.assertDataSent(
            self.request_class.ITEMS, json.dumps([i.to_dict() for i in self.ITEMS])
        )
        self.assertDataSent(
            self.request_class.DELIVERY_ADDRESS_ID, self.DELIVERY_ADDRESS_ID
        )
        self.assertDataSent(
            self.request_class.BILLING_ADDRESS_ID, self.BILLING_ADDRESS_ID
        )
        self.assertDataSent(
            self.request_class.DELIVERY_DATE, self.DELIVERY_DATE.strftime("%d/%m/%Y")
        )
        self.assertDataSent(self.request_class.CSRID, self.request_class.CSRID_VALUE)

    def test_CreateOrder_optional_arguments(self):
        """Test the CreateOrder request sends a login ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            login_id=self.LOGIN_ID,
            season_id=self.SEASON_ID,
            channel_id=self.CHANNEL_ID,
            reference=self.REFERENCE,
            order_id=self.ORDER_ID,
            prep=self.PREP,
            order_note=self.ORDER_NOTE,
            send_email=self.SEND_EMAIL,
            postage_override=self.POSTAGE_OVERRIDE,
            carriage_net=self.CARRIAGE_NET,
            carriage_vat=self.CARRIAGE_VAT,
            total_net=self.TOTAL_NET,
            total_vat=self.TOTAL_VAT,
            total_gross=self.TOTAL_GROSS,
            discount_net=self.DISCOUNT_NET,
            free_of_charge=self.FREE_OF_CHARGE,
            shipping_rule_id=self.SHIPPING_RULE_ID,
        )
        self.assertDataSent(self.request_class.LOGIN_ID, self.LOGIN_ID)
        self.assertDataSent(self.request_class.SEASON_ID, self.SEASON_ID)
        self.assertDataSent(self.request_class.CHANNEL_ID, self.CHANNEL_ID)
        self.assertDataSent(self.request_class.REFERENCE, self.REFERENCE)
        self.assertDataSent(self.request_class.ORDER_ID, self.ORDER_ID)
        self.assertDataSent(self.request_class.PREP, self.PREP)
        self.assertDataSent(self.request_class.ORDER_NOTE, self.ORDER_NOTE)
        self.assertDataSent(self.request_class.SEND_EMAIL, self.SEND_EMAIL)
        self.assertDataSent(self.request_class.POSTAGE_OVERRIDE, self.POSTAGE_OVERRIDE)
        self.assertDataSent(self.request_class.CARRIAGE_NET, self.CARRIAGE_NET)
        self.assertDataSent(self.request_class.CARRIAGE_VAT, self.CARRIAGE_VAT)
        self.assertDataSent(self.request_class.TOTAL_NET, self.TOTAL_NET)
        self.assertDataSent(self.request_class.TOTAL_VAT, self.TOTAL_VAT)
        self.assertDataSent(self.request_class.TOTAL_GROSS, self.TOTAL_GROSS)
        self.assertDataSent(self.request_class.DISCOUNT_NET, self.DISCOUNT_NET)
        self.assertDataSent(
            self.request_class.FREE_OF_CHARGE, str(self.FREE_OF_CHARGE).lower()
        )
        self.assertDataSent(self.request_class.SHIPPING_RULE_ID, self.SHIPPING_RULE_ID)

    def test_CreateOrder_raises_for_non_200_response(self):
        """Test the CreateOrder request raises for non 200 responses."""
        self.register(json=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                items=self.ITEMS,
                customer_id=self.CUSTOMER_ID,
                delivery_address_id=self.DELIVERY_ADDRESS_ID,
                billing_address_id=self.BILLING_ADDRESS_ID,
                delivery_date=self.DELIVERY_DATE,
            )

    def test_CreatOrder_raises_when_response_contains_error(self):
        """Test the request raises when the response error field is not empty."""
        response = dict(self.RESPONSE)
        response[handlers.createorder.CreateOrderResponse.ERROR] = "An Error occured"
        self.register(json=response)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                items=self.ITEMS,
                customer_id=self.CUSTOMER_ID,
                delivery_address_id=self.DELIVERY_ADDRESS_ID,
                billing_address_id=self.BILLING_ADDRESS_ID,
                delivery_date=self.DELIVERY_DATE,
            )

    def test_CreatOrder_raises_when_response_order_id_is_zero(self):
        """Test the request raises when the response error field is not empty."""
        response = dict(self.RESPONSE)
        response[handlers.createorder.CreateOrderResponse.ORDER_ID] = 0
        self.register(json=response)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                items=self.ITEMS,
                customer_id=self.CUSTOMER_ID,
                delivery_address_id=self.DELIVERY_ADDRESS_ID,
                billing_address_id=self.BILLING_ADDRESS_ID,
                delivery_date=self.DELIVERY_DATE,
            )


class TestCreatOrderResponse(unittest.TestCase):
    """Test the CreateOrderResponse class."""

    RETURNED_ORDER_ID = TestCreateOrderRequest.RETURNED_ORDER_ID
    RETURNED_INVOICE_ID = TestCreateOrderRequest.RETURNED_INVOICE_ID
    RETURNED_PAYMENT_TERM_ID = TestCreateOrderRequest.RETURNED_PAYMENT_TERM_ID
    RETURNED_GATEWAY_TYPE = TestCreateOrderRequest.RETURNED_GATEWAY_TYPE
    RETURNED_DAYS_OF_CREDIT = TestCreateOrderRequest.RETURNED_DAYS_OF_CREDIT
    RETURNED_REFERENCE = TestCreateOrderRequest.RETURNED_REFERENCE
    RETURNED_TOTAL_GROSS = TestCreateOrderRequest.RETURNED_TOTAL_GROSS

    RESPONSE = TestCreateOrderRequest.RESPONSE

    def test_CreateOrderResponse_attributes(self):
        """Test the returned object from CreateOrder contains an order ID."""
        response = handlers.createorder.CreateOrderResponse(self.RESPONSE)
        self.assertEqual(response.order_id, self.RETURNED_ORDER_ID)
        self.assertEqual(response.invoice_id, self.RETURNED_INVOICE_ID)
        self.assertEqual(response.payment_term_id, self.RETURNED_PAYMENT_TERM_ID)
        self.assertEqual(response.gateway_type, self.RETURNED_GATEWAY_TYPE)
        self.assertEqual(response.days_of_credit, self.RETURNED_DAYS_OF_CREDIT)
        self.assertEqual(response.reference, self.RETURNED_REFERENCE)
        self.assertEqual(response.total_gross, self.RETURNED_TOTAL_GROSS)
