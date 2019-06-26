"""
customer request.

Handle customers.
"""

from .program_type_request import ProgramTypeRequest


class Customer(ProgramTypeRequest):
    """Customer request."""

    uri = "Handlers/Customer.ashx"

    def process_response(self, response):
        """Handle request response."""
        super().process_response(self, response)
        return response.text


class GetPaymentTerms(Customer):
    """Request to get payment term options."""

    PROGRAM_TYPE = "GetPaymentTerms"

    PAY_TERM_ID = "PayTermID"

    kwargs = {PAY_TERM_ID: 0}

    error_message = "Failed to get payment terms."


class UpdateCustomerAddress(Customer):
    """Request to add or update a customer address."""

    PROGRAM_TYPE = "UpdCustAddr"

    ADMIN = "Admin"
    DELIVERY = "Delivery"
    BILLING = "Billing"

    CUSTOMER_ID = "CustID"
    ADDRESS_TYPE = "AddTitle"
    COMPANY_NAME = "CompanyName"
    FIRST_NAME = "FirstName"
    LAST_NAME = "LastName"
    ADDRESS_1 = "Address1"
    ADDRESS_2 = "Address2"
    POST_CODE = "Postcode"
    TOWN = "Town"
    REGION = "Region"
    COUNTRY = "Country"
    TELEPHONE_NUMBER = "TelNo"
    FAX_NUMBER = "FaxNo"
    MOBILE_NUMBER = "MobNo"
    ADDRESS_ID = "AddressID"
    CUSTOMER_ADD_LINK_ID = "CustAddLinkID"
    EMAIL = "Email"

    error_message = "Failed to add or update a customer address."

    def __new__(
        self,
        *,
        customer_id,
        address_type,
        address_id="0",
        company_name="",
        first_name="",
        last_name="",
        address_1="",
        address_2="",
        post_code="",
        town="",
        region="",
        country="",
        telephone_number="",
        fax_number="",
        mobile_number="",
        customer_add_link_id="0",
        email="",
    ):
        """
        Add or update a customer address.

        Kwargs:
            customer_id (int): The customer ID of the customer to which the address
                belongs.
            address_type (str): The type of the address. Available options
                are "Admin", "Delivery" and "Billing". Optionally use
                UpdateCustomerAddress.ADMIN, UpdateCustomerAddress.DELIVERY or
                UpdateCustomerAddress.BILLING.
            address_id (int): The ID of the address to edit. Use 0 to create a new
                address.
            company_name (str): The adressee's company name. Use an empty string if
                this is not applicable. Default: Empty string.
            first_name (str): The adressee's first name. Default: Empty string.
            last_name (str): The adressee's last name. Default: Empty string.
            address_1 (str): The first line of the address. Default: Empty string.
            address_2 (str): The second line of the address. Default: Empty string.
            post_code (str): The postal or zip code of the address.
                Default: Empty string.
            town (str): The adress's town. Default: Empty string.
            region (str): The county, region or province of the address.
                Default: Empty string.
            country (str): The country the address is in. Default: Empty string.
            telephone_number (str): A contact telephone number for the address.
                Default: Empty string.
            fax_number (str): A contact fax number for the address.
            Default: Empty string.
            mobile_number (str): A contact mobile phone number for the address.
                Default: Empty string.
            customer_add_link_id: Use "0" for a null value. Default "0".

        Returns:
            (str) Body text from the HTTP response.

        """
        self.kwargs[self.CUSTOMER_ID] = customer_id
        self.kwargs[self.ADDRESS_TYPE] = address_type
        self.kwargs[self.COMPANY_NAME] = company_name
        self.kwargs[self.FIRST_NAME] = first_name
        self.kwargs[self.LAST_NAME] = last_name
        self.kwargs[self.ADDRESS_1] = address_1
        self.kwargs[self.ADDRESS_2] = address_2
        self.kwargs[self.POST_CODE] = post_code
        self.kwargs[self.TOWN] = town
        self.kwargs[self.REGION] = region
        self.kwargs[self.COUNTRY] = country
        self.kwargs[self.TELEPHONE_NUMBER] = telephone_number
        self.kwargs[self.FAX_NUMBER] = fax_number
        self.kwargs[self.MOBILE_NUMBER] = mobile_number
        self.kwargs[self.ADDRESS_ID] = address_id
        self.kwargs[self.CUSTOMER_ADD_LINK_ID] = customer_add_link_id
        self.kwargs[self.EMAIL] = email
        return super().__new__(self)
