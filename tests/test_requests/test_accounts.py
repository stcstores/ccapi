"""Tests for accounts requests."""

import datetime

from ccapi import exceptions
from ccapi.requests import accounts

from .test_request import TestRequest


class TestCreatePayment(TestRequest):
    """Tests for the CreatePayment request."""

    request_class = accounts.CreatePayment

    RESPONSE = "success"

    CUSTOMER_ID = "18495409"
    INVOICE_ID = "17249270"
    AMOUNT = 17.99
    BRAND_ID = "341"
    LOGIN_ID = "1321483154"
    TRANSACTION_TYPE_ID = "12"
    BANK_NOMINAL_CODE = "15438431"
    BANK_ACCOUNT_ID = "13248121"
    PROFORMA_ID = "4513032413"
    GATEWAY_ID = "1651138443"
    CURRENCY_CODE_ID = "12"
    CURRENCY_CODE = "USD"
    EXCHANGE_RATE = "1.25"
    TRANSACTION_DATE = datetime.datetime(day=1, month=1, year=1970)

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_CreatePayment_sends_customer_ID(self):
        """Test the CreatePayment request sends a customer ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID, invoice_id=self.INVOICE_ID, amount=self.AMOUNT
        )
        self.assertDataSent(self.request_class.CUSTOMER_ID, self.CUSTOMER_ID)

    def test_CreatePayment_sends_invoice_ID(self):
        """Test the CreatePayment request sends an invoice ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID, invoice_id=self.INVOICE_ID, amount=self.AMOUNT
        )
        self.assertDataSent(self.request_class.INVOICE_ID, self.INVOICE_ID)

    def test_CreatePayment_sends_amount(self):
        """Test the CreatePayment request sends an amount."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID, invoice_id=self.INVOICE_ID, amount=self.AMOUNT
        )
        self.assertDataSent(self.request_class.AMOUNT, self.AMOUNT)

    def test_CreatePayment_sends_brand_ID(self):
        """Test the CreatePayment request sends a brand ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            brand_id=self.BRAND_ID,
        )
        self.assertDataSent(self.request_class.BRAND_ID, self.BRAND_ID)

    def test_CreatePayment_sends_login_ID(self):
        """Test the CreatePayment request sends a login ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            login_id=self.LOGIN_ID,
        )
        self.assertDataSent(self.request_class.LOGIN_ID, self.LOGIN_ID)

    def test_CreatePayment_sends_transaction_type_ID(self):
        """Test the CreatePayment request sends a transaction type ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            transaction_type_id=self.TRANSACTION_TYPE_ID,
        )
        self.assertDataSent(
            self.request_class.TRANSACTION_TYPE_ID, self.TRANSACTION_TYPE_ID
        )

    def test_CreatePayment_sends_bank_nominal_code(self):
        """Test the CreatePayment request sends a bank nominal code."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            bank_nominal_code=self.BANK_NOMINAL_CODE,
        )
        self.assertDataSent(
            self.request_class.BANK_NOMINAL_CODE, self.BANK_NOMINAL_CODE
        )

    def test_CreatePayment_sends_bank_account_ID(self):
        """Test the CreatePayment request sends a bank account ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            bank_account_id=self.BANK_ACCOUNT_ID,
        )
        self.assertDataSent(self.request_class.BANK_ACCOUNT_ID, self.BANK_ACCOUNT_ID)

    def test_CreatePayment_sends_proforma_ID(self):
        """Test the CreatePayment request sends a proforma ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            proforma_id=self.PROFORMA_ID,
        )
        self.assertDataSent(self.request_class.PROFORMA_ID, self.PROFORMA_ID)

    def test_CreatePayment_sends_gateway_ID(self):
        """Test the CreatePayment request sends a gateway ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            gateway_id=self.GATEWAY_ID,
        )
        self.assertDataSent(self.request_class.GATEWAY_ID, self.GATEWAY_ID)

    def test_CreatePayment_sends_currency_code_ID(self):
        """Test the CreatePayment request sends a currency code ID."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            currency_code_id=self.CURRENCY_CODE_ID,
        )
        self.assertDataSent(self.request_class.CURRENCY_CODE_ID, self.CURRENCY_CODE_ID)

    def test_CreatePayment_sends_currency_code(self):
        """Test the CreatePayment request sends a currency code."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            currency_code=self.CURRENCY_CODE,
        )
        self.assertDataSent(self.request_class.CURRENCY_CODE, self.CURRENCY_CODE)

    def test_CreatePayment_sends_exchange_rate(self):
        """Test the CreatePayment request sends an exchange rate."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            exchange_rate=self.EXCHANGE_RATE,
        )
        self.assertDataSent(self.request_class.EXCHANGE_RATE, self.EXCHANGE_RATE)

    def test_CreatePayment_sends_current_date_as_transaction_date(self):
        """Test the request sends the current date when no transaction date is passed."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID, invoice_id=self.INVOICE_ID, amount=self.AMOUNT
        )
        self.assertDataSent(
            self.request_class.TRANSACTION_DATE,
            datetime.datetime.now().strftime("%d/%m/%Y"),
        )

    def test_CreatePayment_sends_passed_transaction_date(self):
        """Test the CreatePayment request sends a passed transaction date."""
        self.mock_request(
            customer_id=self.CUSTOMER_ID,
            invoice_id=self.INVOICE_ID,
            amount=self.AMOUNT,
            transaction_date=self.TRANSACTION_DATE,
        )
        self.assertDataSent(
            self.request_class.TRANSACTION_DATE,
            self.TRANSACTION_DATE.strftime("%d/%m/%Y"),
        )

    def test_CreatePayment_raises_for_non_200(self):
        """Test the AddNewRange request raises for non 200 responses."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(exceptions.CloudCommerceResponseError):
            self.mock_request(
                customer_id=self.CUSTOMER_ID,
                invoice_id=self.INVOICE_ID,
                amount=self.AMOUNT,
            )
