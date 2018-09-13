"""Tests for handler requests."""

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


class TestCustomer(TestRequest):
    """Tests for the Customer request."""

    request_class = handlers.Customer

    RESPONSE = "RESPONSE TEXT"
    TEST_KWARG = "Kwarg"
    TEST_KWARG_VALUE = "Value"
    PROGRAM_TYPE = "GetPaymentTerms"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_Customer_returns_response_text(self):
        """Test the Customer request returns the response text."""
        response = self.mock_request(program_type=self.PROGRAM_TYPE)
        self.assertEqual(response, self.RESPONSE)

    def test_Customer_sends_program_type(self):
        """Test the Customer request sends a program type."""
        self.mock_request(program_type=self.PROGRAM_TYPE)
        self.assertDataSent("ProgType", self.PROGRAM_TYPE)

    def test_Customer_sends_kwargs(self):
        """Test the Customer request sends kwargs."""
        kwargs = {self.TEST_KWARG: self.TEST_KWARG_VALUE}
        self.mock_request(program_type=self.PROGRAM_TYPE, **kwargs)
        self.assertDataSent(self.TEST_KWARG, self.TEST_KWARG_VALUE)
