"""Tests for handler requests."""

import datetime
import json

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

    def test_AddCustomer_request_sends_account_ID(self):
        """Test the AddCustomer request sends an account ID."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataValueIsNone("AcctName", None)

    def test_AddCustomer_request_sends_account_name(self):
        """Test the AddCustomer request sends an account name."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            account_name=self.ACCOUNT_NAME,
        )
        self.assertDataSent("AcctName", self.ACCOUNT_NAME)

    def test_AddCustomer_request_sends_address_1(self):
        """Test the AddCustomer request sends the first address line."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("addr1", self.ADDRESS_1)

    def test_AddCustomer_request_sends_address_2(self):
        """Test the AddCustomer request sends the second address line."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            address_2=self.ADDRESS_2,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("addr2", self.ADDRESS_2)

    def test_AddCustomer_request_sends_agent_ID(self):
        """Test the AddCustomer request sends an agent ID."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            agent_id=self.AGENT_ID,
        )
        self.assertDataSent("agentID", self.AGENT_ID)

    def test_AddCustomer_request_sends_company_fax(self):
        """Test the AddCustomer request sends a company fax."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            company_fax=self.COMPANY_FAX,
        )
        self.assertDataSent("compFax", self.COMPANY_FAX)

    def test_AddCustomer_request_sends_company_mobile(self):
        """Test the AddCustomer request sends a company mobile number."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            company_mobile=self.COMPANY_MOBILE,
        )
        self.assertDataSent("compMob", self.COMPANY_MOBILE)

    def test_AddCustomer_request_sends_company_telephone(self):
        """Test the AddCustomer request sends a company telephone number."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            company_telephone=self.COMPANY_TELEPHONE,
        )
        self.assertDataSent("compTel", self.COMPANY_TELEPHONE)

    def test_AddCustomer_request_sends_contact_email(self):
        """Test the AddCustomer request sends a contact email address."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            contact_email=self.CONTACT_EMAIL,
        )
        self.assertDataSent("contEmail", self.CONTACT_EMAIL)

    def test_AddCustomer_request_sends_contact_fax(self):
        """Test the AddCustomer request sends a contact fax number."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            contact_fax=self.CONTACT_FAX,
        )
        self.assertDataSent("contFax", self.CONTACT_FAX)

    def test_AddCustomer_request_sends_contact_mobile(self):
        """Test the AddCustomer request sends a contact mobile number."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            contact_mobile=self.CONTACT_MOBILE,
        )
        self.assertDataSent("contMob", self.CONTACT_MOBILE)

    def test_AddCustomer_request_sends_contact_name(self):
        """Test the AddCustomer request sends a contact name."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            contact_name=self.CONTACT_NAME,
        )
        self.assertDataSent("contName", self.CONTACT_NAME)

    def test_AddCustomer_request_sends_contact_phone(self):
        """Test the AddCustomer request sends a contact phone number."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            contact_phone=self.CONTACT_PHONE,
        )
        self.assertDataSent("contPhone", self.CONTACT_PHONE)

    def test_AddCustomer_request_sends_country(self):
        """Test the AddCustomer request sends a country."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("country", self.COUNTRY)

    def test_AddCustomer_request_sends_county(self):
        """Test the AddCustomer request sends a county."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            county=self.COUNTY,
        )
        self.assertDataSent("county", self.COUNTY)

    def test_AddCustomer_request_sends_create_parameter(self):
        """Test the AddCustomer request sends the create parameter."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("create", 0)

    def test_AddCustomer_request_sends_customer_name(self):
        """Test the AddCustomer request sends a customer name."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("CustName", self.CUSTOMER_NAME)

    def test_AddCustomer_request_sends_customer_type(self):
        """Test the AddCustomer request sends a customer type."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            customer_type=self.CUSTOMER_TYPE,
        )
        self.assertDataSent("CustType", self.CUSTOMER_TYPE)

    def test_AddCustomer_request_sends_EU_VAT(self):
        """Test the AddCustomer request sends EU VAT."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            eu_vat=self.EU_VAT,
        )
        self.assertDataSent("EUVAT", int(bool(self.EU_VAT)))

    def test_AddCustomer_request_sends_linkTo_parameter(self):
        """Test the AddCustomer request sends the linkTo parameter."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("linkTo", 0)

    def test_AddCustomer_request_sends_oSCID_parameter(self):
        """Test the AddCustomer request sends the oSCID parameter."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("oSCID", 0)

    def test_AddCustomer_request_sends_post_code(self):
        """Test the AddCustomer request sends a post code."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            post_code=self.POST_CODE,
        )
        self.assertDataSent("pcode", self.POST_CODE)

    def test_AddCustomer_request_sends_payment_terms(self):
        """Test the AddCustomer request sends a payment term ID."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            payment_terms=self.PAYMENT_TERMS,
        )
        self.assertDataSent("pterms", self.PAYMENT_TERMS)

    def test_AddCustomer_request_sends_selling_channel_ID(self):
        """Test the AddCustomer request sends a selling channel ID."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
        )
        self.assertDataSent("scID", self.SELLING_CHANNEL_ID)

    def test_AddCustomer_request_sends_special_instructions(self):
        """Test the AddCustomer request sends special instructions."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            special_instructions=self.SPECIAL_INSTRUCTIONS_NOTE,
        )
        self.assertDataSent("SpecInstr", 1)
        self.assertDataSent("SpecInstrNote", self.SPECIAL_INSTRUCTIONS_NOTE)

    def test_AddCustomer_request_sends_false_for_no_special_instructions(self):
        """Test False is send for special instructions when no note is passed."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            special_instructions=None,
        )
        self.assertDataSent("SpecInstr", 0)
        self.assertDataValueIsNone("SpecInstrNote", None)

    def test_AddCustomer_request_sends_town(self):
        """Test the AddCustomer request sends a town."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            town=self.TOWN,
        )
        self.assertDataSent("town", self.TOWN)

    def test_AddCustomer_request_sends_trade_name(self):
        """Test the AddCustomer request sends a trade name."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            trade_name=self.TRADE_NAME,
        )
        self.assertDataSent("TradName", self.TRADE_NAME)

    def test_AddCustomer_request_sends_VAT_number(self):
        """Test the AddCustomer request sends a VAT number."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            vat_number=self.VAT_NUMBER,
        )
        self.assertDataSent("VATNo", self.VAT_NUMBER)

    def test_AddCustomer_request_sends_credit_limit(self):
        """Test the AddCustomer request sends a credit limit."""
        self.mock_request(
            customer_name=self.CUSTOMER_NAME,
            address_1=self.ADDRESS_1,
            country=self.COUNTRY,
            selling_channel_id=self.SELLING_CHANNEL_ID,
            credit_limit=self.CREDIT_LIMIT,
        )
        self.assertDataSent("CreditLimit", self.CREDIT_LIMIT)


class TestCreateOrderCustomer(TestRequest):
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

    def test_CreateOrder_returns_order_id(self):
        """Test the returned object from CreateOrder contains an order ID."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.order_id, self.RETURNED_ORDER_ID)

    def test_CreateOrder_returns_invoice_id(self):
        """Test the returned object from CreateOrder contains an invoice ID."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.invoice_id, self.RETURNED_INVOICE_ID)

    def test_CreateOrder_returns_payment_term_id(self):
        """Test the returned object from CreateOrder contains a payment term ID."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.payment_term_id, self.RETURNED_PAYMENT_TERM_ID)

    def test_CreateOrder_returns_gateway_type(self):
        """Test the returned object from CreateOrder contains a gateway_type."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.gateway_type, self.RETURNED_GATEWAY_TYPE)

    def test_CreateOrder_returns_days_of_credit(self):
        """Test the returned object from CreateOrder contains the days of credit."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.days_of_credit, self.RETURNED_DAYS_OF_CREDIT)

    def test_CreateOrder_returns_reference(self):
        """Test the returned object from CreateOrder contains a reference."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.reference, self.RETURNED_REFERENCE)

    def test_CreateOrder_returns_total_gross(self):
        """Test the returned object from CreateOrder contains the total gross."""
        response = self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertEqual(response.total_gross, self.RETURNED_TOTAL_GROSS)

    def test_CreateOrder_sends_customer_ID(self):
        """Test the CreateOrder request sends a customer ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(self.request_class.CUSTOMER_ID, self.CUSTOMER_ID)

    def test_CreateOrder_sends_items(self):
        """Test the CreateOrder request sends a dict of items."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(
            self.request_class.ITEMS, json.dumps([i.to_dict() for i in self.ITEMS])
        )

    def test_CreateOrder_sends_delivery_address_ID(self):
        """Test the CreateOrder request sends a delivery address ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(
            self.request_class.DELIVERY_ADDRESS_ID, self.DELIVERY_ADDRESS_ID
        )

    def test_CreateOrder_sends_billing_address_ID(self):
        """Test the CreateOrder request sends a billing address ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(
            self.request_class.BILLING_ADDRESS_ID, self.BILLING_ADDRESS_ID
        )

    def test_CreateOrder_sends_delivery_date(self):
        """Test the CreateOrder request sends a delivery_date."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(
            self.request_class.DELIVERY_DATE, self.DELIVERY_DATE.strftime("%d/%m/%Y")
        )

    def test_CreateOrder_sends_login_ID(self):
        """Test the CreateOrder request sends a login ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            login_id=self.LOGIN_ID,
        )
        self.assertDataSent(self.request_class.LOGIN_ID, self.LOGIN_ID)

    def test_CreateOrder_sends_season_ID(self):
        """Test the CreateOrder request sends a season ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            season_id=self.SEASON_ID,
        )
        self.assertDataSent(self.request_class.SEASON_ID, self.SEASON_ID)

    def test_CreateOrder_sends_channel_ID(self):
        """Test the CreateOrder request sends a channel ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            channel_id=self.CHANNEL_ID,
        )
        self.assertDataSent(self.request_class.CHANNEL_ID, self.CHANNEL_ID)

    def test_CreateOrder_sends_reference(self):
        """Test the CreateOrder request sends a reference."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            reference=self.REFERENCE,
        )
        self.assertDataSent(self.request_class.REFERENCE, self.REFERENCE)

    def test_CreateOrder_sends_order_ID(self):
        """Test the CreateOrder request sends an order ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            order_id=self.ORDER_ID,
        )
        self.assertDataSent(self.request_class.ORDER_ID, self.ORDER_ID)

    def test_CreateOrder_sends_prep(self):
        """Test the CreateOrder request sends prep."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            prep=self.PREP,
        )
        self.assertDataSent(self.request_class.PREP, self.PREP)

    def test_CreateOrder_sends_order_note(self):
        """Test the CreateOrder request sends order note."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            order_note=self.ORDER_NOTE,
        )
        self.assertDataSent(self.request_class.ORDER_NOTE, self.ORDER_NOTE)

    def test_CreateOrder_sends_send_email(self):
        """Test the CreateOrder request sends whether to send an email."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            send_email=self.SEND_EMAIL,
        )
        self.assertDataSent(self.request_class.SEND_EMAIL, self.SEND_EMAIL)

    def test_CreateOrder_sends_postage_override(self):
        """Test the CreateOrder request sends postage override."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            postage_override=self.POSTAGE_OVERRIDE,
        )
        self.assertDataSent(self.request_class.POSTAGE_OVERRIDE, self.POSTAGE_OVERRIDE)

    def test_CreateOrder_sends_carriage_net(self):
        """Test the CreateOrder request sends carriage net."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            carriage_net=self.CARRIAGE_NET,
        )
        self.assertDataSent(self.request_class.CARRIAGE_NET, self.CARRIAGE_NET)

    def test_CreateOrder_sends_carriage_vat(self):
        """Test the CreateOrder request sends carriage vat."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            carriage_vat=self.CARRIAGE_VAT,
        )
        self.assertDataSent(self.request_class.CARRIAGE_VAT, self.CARRIAGE_VAT)

    def test_CreateOrder_sends_total_net(self):
        """Test the CreateOrder request sends total net."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            total_net=self.TOTAL_NET,
        )
        self.assertDataSent(self.request_class.TOTAL_NET, self.TOTAL_NET)

    def test_CreateOrder_sends_total_vat(self):
        """Test the CreateOrder request sends total vat."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            total_vat=self.TOTAL_VAT,
        )
        self.assertDataSent(self.request_class.TOTAL_VAT, self.TOTAL_VAT)

    def test_CreateOrder_sends_total_gross(self):
        """Test the CreateOrder request sends total gross."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            total_gross=self.TOTAL_GROSS,
        )
        self.assertDataSent(self.request_class.TOTAL_GROSS, self.TOTAL_GROSS)

    def test_CreateOrder_sends_discount_net(self):
        """Test the CreateOrder request sends net discount."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            discount_net=self.DISCOUNT_NET,
        )
        self.assertDataSent(self.request_class.DISCOUNT_NET, self.DISCOUNT_NET)

    def test_CreateOrder_sends_free_of_charge(self):
        """Test the CreateOrder request sends free of charge."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            free_of_charge=self.FREE_OF_CHARGE,
        )
        self.assertDataSent(
            self.request_class.FREE_OF_CHARGE, str(self.FREE_OF_CHARGE).lower()
        )

    def test_CreateOrder_sends_shipping_rule_ID(self):
        """Test the CreateOrder request sends a channel ID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
            shipping_rule_id=self.SHIPPING_RULE_ID,
        )
        self.assertDataSent(self.request_class.SHIPPING_RULE_ID, self.SHIPPING_RULE_ID)

    def test_CreateOrder_sends_CSRID(self):
        """Test the CreateOrder request sends CSRID."""
        self.mock_request(
            items=self.ITEMS,
            customer_id=self.CUSTOMER_ID,
            delivery_address_id=self.DELIVERY_ADDRESS_ID,
            billing_address_id=self.BILLING_ADDRESS_ID,
            delivery_date=self.DELIVERY_DATE,
        )
        self.assertDataSent(self.request_class.CSRID, self.request_class.CSRID_VALUE)

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
