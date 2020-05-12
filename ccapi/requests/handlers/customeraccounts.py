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
    S_NOMINAL = "sNominal"
    GATEWAY_TYPE_ID = "gatewayTypeId"

    INSERT_PAYMENT = "InsertPayment"

    def __new__(
        self,
        *,
        prog_type,
        customer_ID,
        factory_ID=0,
        brand_ID=0,
        login_ID,
        transaction_type=13,
        credit_note_type=0,
        currency,
        gbp=None,
        description=None,
        reference=None,
        payment_date=None,
        bank_account_ID,
        proforma_ID=None,
        invoice_ID,
        channel_ID,
        exchange_rate="",
        s_nominal="",
        gateway_type_ID=None,
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
        self.customer_ID = int(customer_ID)
        self.factory_ID = int(factory_ID)
        self.brand_ID = int(brand_ID)
        self.login_ID = int(login_ID)
        self.transaction_type = transaction_type
        self.credit_note_type = credit_note_type
        self.currency = float(currency)
        self.gbp = float(gbp) if gbp is not None else self.currency
        self.invoice_ID = int(invoice_ID)
        self.description = description or f"PAYMENT+INV{invoice_ID}"
        self.reference = reference or f"PAYMENT+INV{invoice_ID}"
        self.payment_date = payment_date
        self.bank_account_ID = int(bank_account_ID)
        self.proforma_ID = None if proforma_ID is None else int(proforma_ID)
        self.channel_ID = int(channel_ID)
        self.exchange_rate = exchange_rate
        self.s_nominal = s_nominal
        self.gateway_type_ID = None if gateway_type_ID is None else int(gateway_type_ID)
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
                self.S_NOMINAL: self.s_nominal,
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
