"""
CreatePayment request.

Create a payment for an order.
"""

import datetime

from ...apirequest import APIRequest


class CreatePayment(APIRequest):
    """CreatePayment request."""

    uri = '/Handlers/Accounts/Payment/CreatePayment.ashx'

    def __new__(
            self,
            customer_id=None,
            invoice_id=None,
            login_id=None,
            transaction_type_id='12',
            bank_nominal_code='',
            transaction_date=None,
            bank_account_id='0',
            amount=0,
            proforma_id='0',
            gateway_id='0',
            currency_code_id='1',
            currency_code='GBP',
            exchange_rate='1',
            brand_id='341'):
        """Create CreatePayment request."""
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

    def get_data(self):
        """Get data for get request."""
        data = {
            'brandId': self.brand_id,
            'customerId': self.customer_id,
            'loginId': self.login_id,
            'transactionTypeId': self.transaction_type_id,
            'bankNominalCode': self.bank_nominal_code,
            'transactionDate': self.transaction_date.strftime('%d/%m/%Y'),
            'bankAccountId': self.bank_account_id,
            'amount': self.amount,
            'invoiceId': self.invoice_id,
            'proformaId': self.proforma_id,
            'gatewayId': self.gateway_id,
            'CurrencyCodeId': self.currency_code_id,
            'CurrencyCode': self.currency_code,
            'exchangeRate': self.exchange_rate,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response.text == 'success'
