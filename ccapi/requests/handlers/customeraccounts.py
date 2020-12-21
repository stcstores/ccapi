"""
CreateOrder request.

Add a new customer to Cloud Commerce.
"""

import datetime

from ccapi.exceptions import CloudCommerceResponseError
from ccapi.requests import APIRequest


class CustomerAccounts(APIRequest):
    """CustomerAccounts request."""

    uri = "Handlers/CustomerAccounts.ashx"

    PROG_TYPE = "ProgType"
    CUSTOMER_ID = "CustID"
    FACTORY_ID = "FactoryID"
    BRAND_ID = "BrandID"
    LOGIN_ID = "LoginID"
    TRANSACTION_TYPE = "TransType"
    CREDIT_NOTE_TYPE = "CrNoteType"
    CURRENCY = "Currency"
    GBP = "GBP"
    DESCRIPTION = "Description"
    REFERENCE = "Reference"
    PAYMENT_DATE = "PaymentDate"
    BANK_ACCOUNT_ID = "BankAccID"
    PROFORMA_ID = "proformaID"
    INVOICE_ID = "invoiceID"
    CHANNEL_ID = "chanid"
    EXCHANGE_RATE = "flTodaysExchangeRate"
    BANK_NOMINAL = "BankNominal"
    GATEWAY_TYPE_ID = "gatewayTypeId"

    INSERT_PAYMENT = "InsertPayment"

    def __new__(
        self,
        *,
        prog_type,
        customer_id,
        invoice_id,
        amount,
        channel_id,
        factory_id="0",
        brand_id="0",
        login_id="0",
        transaction_type="13",
        credit_note_type="0",
        description=None,
        reference=None,
        payment_date=None,
        bank_account_id="0",
        proforma_id="",
        exchange_rate="",
        bank_nominal="",
        gateway_type_id="0",
        gbp=None,
    ):
        """
        Create a CustomerAccounts request.

        The CreateOrder request is used manage customer accounts.

        Kwargs:
            prog_type (str): The type of request to send.
            customer_ID (int): The ID of the customer to apply the payment to.
            login_ID (int): The ID of the user creating the payment.
            currency (float): The amount paid.
            gbp (float): The amount paid in GBP.
            payment_date (datetime.datetime) The date of the payment.
            bank_account_ID (int): The ID of the bank account into which the payment was
                made.
            invoice_ID (int): The ID of the invoice that has been paid.
            channel_ID (int): The ID of the channel from which the invoice was created.
        """
        self.prog_type = prog_type
        self.customer_ID = customer_id
        self.factory_ID = factory_id
        self.brand_ID = brand_id
        self.login_ID = login_id
        self.transaction_type = transaction_type
        self.credit_note_type = credit_note_type
        self.currency = amount
        self.gbp = amount if gbp is not None else self.currency
        self.invoice_ID = invoice_id
        self.description = description or f"PAYMENT+INV{invoice_id}"
        self.reference = reference or f"PAYMENT+INV{invoice_id}"
        self.payment_date = payment_date or datetime.datetime.now()
        self.bank_account_ID = bank_account_id
        self.proforma_ID = proforma_id
        self.channel_ID = channel_id
        self.exchange_rate = exchange_rate
        self.bank_nominal = bank_nominal
        self.gateway_type_ID = gateway_type_id
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        payment_date = self.payment_date or datetime.datetime.now()
        if self.prog_type == self.INSERT_PAYMENT:
            data = {
                self.PROG_TYPE: self.INSERT_PAYMENT,
                self.CUSTOMER_ID: self.customer_ID,
                self.FACTORY_ID: self.factory_ID,
                self.BRAND_ID: self.brand_ID,
                self.LOGIN_ID: self.login_ID,
                self.TRANSACTION_TYPE: self.transaction_type,
                self.CREDIT_NOTE_TYPE: self.credit_note_type,
                self.CURRENCY: self.currency,
                self.GBP: self.gbp,
                self.DESCRIPTION: self.description,
                self.REFERENCE: self.reference,
                self.PAYMENT_DATE: payment_date.strftime("%d/%m/%Y"),
                self.BANK_ACCOUNT_ID: self.bank_account_ID,
                self.PROFORMA_ID: self.proforma_ID,
                self.INVOICE_ID: self.invoice_ID,
                self.CHANNEL_ID: self.channel_ID,
                self.EXCHANGE_RATE: self.exchange_rate,
                self.BANK_NOMINAL: self.bank_nominal,
                self.GATEWAY_TYPE_ID: self.gateway_type_ID,
            }
        else:
            raise ValueError(
                (
                    f"Prog type {self.prog_type} is not recognised for CustomerAccounts "
                    "reqeuest."
                )
            )
        return data

    def process_response(self, response):
        """Handle request response."""
        if self.prog_type == self.INSERT_PAYMENT:
            self.raise_for_non_200(self, response, "Failed to create payment.")
        if "Inserted" in response.text:
            return True
        else:
            raise CloudCommerceResponseError("Payment not inserted.")
