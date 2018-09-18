"""
CreatePayment request.

Create a payment for an order.
"""

import datetime

from ...apirequest import APIRequest


class CreatePayment(APIRequest):
    """CreatePayment request."""

    uri = "Handlers/Accounts/Payment/CreatePayment.ashx"

    BRAND_ID = "brandId"
    CUSTOMER_ID = "customerId"
    LOGIN_ID = "loginId"
    TRANSACTION_TYPE_ID = "transactionTypeId"
    BANK_NOMINAL_CODE = "bankNominalCode"
    TRANSACTION_DATE = "transactionDate"
    BANK_ACCOUNT_ID = "bankAccountId"
    AMOUNT = "amount"
    INVOICE_ID = "invoiceId"
    PROFORMA_ID = "proformaId"
    GATEWAY_ID = "gatewayId"
    CURRENCY_CODE_ID = "CurrencyCodeId"
    CURRENCY_CODE = "CurrencyCode"
    EXCHANGE_RATE = "exchangeRate"

    def __new__(
        self,
        *,
        customer_id,
        invoice_id,
        amount,
        transaction_type_id=12,
        bank_nominal_code=None,
        transaction_date=None,
        bank_account_id=0,
        proforma_id=None,
        gateway_id=0,
        currency_code_id=1,
        currency_code=None,
        exchange_rate=1,
        brand_id=None,
        login_id=None,
    ):
        """
        Create CreatePayment request.

        This request is used to mark an order as paied.

        Kwargs:
            customer_id (int) (required): The ID of the customer that originated the
                payment.
            invoice_id (int) (required): The ID of the invoice being paid.
            amount (float) (required): The amount paid.
            transaction_type_id (int): The ID of the transaction type. Default: 12.
            bank_nominal_code (int):
            transaction_date (datetime.datetime or None): The date of the transaction.
                If None, the current date will be used.
            bank_account_id (int): The ID of the customer's bank account. 0 is used
                when no bank account is to be indicated. Default: 0.
            proforma_id (int or None): The ID of the transaction proforma. "0" is used
                when no proforma is to be indicated. Default: None.
            gateway_id: 0 is used when no gateway ID is to be indicated. Default: 0.
            currency_code_id (int or None): The ID of the currency used for the
                transaction. Default: 1 (GBP).
            currency_code (int or None): Three letter code for the currency of the
                transaction. Not required. Default: None.
            exchange_rate (int): The rate of exchange between the transaction currency
                and GBP. Default: "1".
            brand_id (int or None): Not required. Default: None
            login_id (int or None): Not required. Default: None
        """
        self.customer_id = customer_id
        self.invoice_id = invoice_id
        self.login_id = login_id
        self.transaction_type_id = transaction_type_id
        self.bank_nominal_code = bank_nominal_code
        self.transaction_date = transaction_date or datetime.datetime.now()
        self.bank_account_id = bank_account_id
        self.amount = amount
        self.proforma_id = proforma_id
        self.gateway_id = gateway_id
        self.currency_code_id = currency_code_id
        self.currency_code = currency_code
        self.exchange_rate = exchange_rate
        self.brand_id = brand_id
        return super().__new__(self)

    def get_headers(self):
        """Return headers to be sent with the request."""
        return {"RequestMode": "pay_invoice"}

    def get_data(self):
        """Get data for get request."""
        data = {
            self.BRAND_ID: self.brand_id,
            self.CUSTOMER_ID: self.customer_id,
            self.LOGIN_ID: self.login_id,
            self.TRANSACTION_TYPE_ID: self.transaction_type_id,
            self.BANK_NOMINAL_CODE: self.bank_nominal_code,
            self.TRANSACTION_DATE: self.transaction_date.strftime("%d/%m/%Y"),
            self.BANK_ACCOUNT_ID: self.bank_account_id,
            self.AMOUNT: self.amount,
            self.INVOICE_ID: self.invoice_id,
            self.PROFORMA_ID: self.proforma_id,
            self.GATEWAY_ID: self.gateway_id,
            self.CURRENCY_CODE_ID: self.currency_code_id,
            self.CURRENCY_CODE: self.currency_code,
            self.EXCHANGE_RATE: self.exchange_rate,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, f"Failed to create payment.")
