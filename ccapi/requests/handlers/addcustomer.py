"""
addCustomer request.

Add a new customer to Cloud Commerce.
"""

from ccapi.requests import APIRequest


class AddCustomer(APIRequest):
    """addCustomer request."""

    uri = "Handlers/addCustomer.ashx"

    def __new__(
        self,
        *,
        customer_name,
        address_1,
        country,
        selling_channel_id,
        address_2=None,
        town=None,
        post_code=None,
        account_name=None,
        agent_id=0,
        company_fax=None,
        company_mobile=None,
        company_telephone=None,
        contact_email=None,
        contact_fax=None,
        contact_name=None,
        contact_phone=None,
        contact_mobile=None,
        county=None,
        customer_type=8,
        eu_vat=True,
        payment_terms=1,
        trade_name=None,
        vat_number=None,
        special_instructions=None,
        credit_limit=0,
    ):
        """
        Create an addCustomer request.

        Make a request to add a new customer to Cloud Commerce.

        Kwargs:
            customer_name (Required) (str): The new customer's name.
            address_1 (Required) (str): The first line of the customer's address.
            country (Required) (str): The country of the customer's address.
            selling_channel_id (Required) (str): The ID of the selling channel used by
                the customer.
            account_name (str or None): The name of the customer's accound.
                Default: None.
            address_2 (str or None): The second line of the customer's address.
                Default: None.
            agent_id (int): The ID of the agent creating the customer.
                Use 0 to not specify an agent. Default: 0.
            company_fax (str or None): The customer's company fax number.
                Default: None.
            company_mobile (str or None): The customer's company mobile number.
                Default: None.
            company_telephone (str or None): The customer's company telephone number.
                Default: None.
            contact_email (str or None): The customer's contact email address.
                Default: None.
            contact_fax (str or None): The customer's contact fax number.
                Default: None.
            contact_name (str or None): The customer's contact name. Default: None.
            contact_phone (str or None): The customer's contact phone number.
                Default: None.
            contact_mobile (str or None): The customer's contact phone number.
                Default: None.
            county (str or None): The county or region of the customer's address.
                Default: None.
            customer_type (int): The ID of the type of the customer. Default: 8.
            eu_vat (bool): True if the customer is charged EU VAT. Default: True.
            post_code (str or None): The customer's postal or zip code. Default: None.
            payment_terms (int): ID of the payment terms for the customer. A list of
                payment term IDs can be found by calling CCAPI.get_payment_terms().
                Default: 1 (Full Payment Before Dispatch).
            town (str or None): The town in the customer's address. Default: None.
            trade_name (str or None): The customer's trading name. If None customer_name
                will be used. Default: None.
            vat_number (str or None): The customer's VAT number. Default: None.
            special_instructions (str or None): Special instructions for the customer.
                Default: None.
            credit_limit (int): The customer's credit limit. Default 0.

            Returns:
                (str) The ID of the newly created customer.

        """
        self.customer_name = customer_name
        self.address_1 = address_1
        self.selling_channel_id = selling_channel_id
        self.account_name = account_name or ""
        self.address_2 = address_2 or ""
        self.agent_id = agent_id
        self.company_fax = company_fax or ""
        self.company_mobile = company_mobile or ""
        self.company_telephone = company_telephone or ""
        self.contact_email = contact_email or ""
        self.contact_fax = contact_fax or ""
        self.contact_name = contact_name or self.customer_name
        self.contact_mobile = contact_mobile or ""
        self.contact_phone = contact_phone or ""
        self.country = country or ""
        self.county = county or ""
        self.customer_type = customer_type or ""
        self.eu_vat = eu_vat or ""
        self.post_code = post_code or ""
        self.payment_terms = payment_terms or ""
        self.town = town or ""
        self.trade_name = trade_name or self.customer_name
        self.vat_number = vat_number or ""
        self.special_instructions = special_instructions or ""
        self.credit_limit = credit_limit
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {
            "AccountID": None,
            "AcctName": self.account_name,
            "addr1": self.address_1,
            "addr2": self.address_2,
            "agentID": self.agent_id,
            "compFax": self.company_fax,
            "compMob": self.company_mobile,
            "compTel": self.company_telephone,
            "contEmail": self.contact_email,
            "contFax": self.contact_fax,
            "contMob": self.contact_mobile,
            "contName": self.contact_name,
            "contPhone": self.contact_phone,
            "country": self.country,
            "county": self.county,
            "create": 0,
            "CustName": self.customer_name,
            "CustType": self.customer_type,
            "EUVAT": int(bool(self.eu_vat)),
            "linkTo": 0,
            "oSCID": 0,
            "pcode": self.post_code,
            "pterms": self.payment_terms,
            "scID": self.selling_channel_id,
            "SpecInstr": int(bool(self.special_instructions)),
            "SpecInstrNote": self.special_instructions,
            "town": self.town,
            "TradName": self.trade_name,
            "VATNo": self.vat_number,
            "CreditLimit": self.credit_limit,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        try:
            response.raise_for_status()
        except Exception:
            raise Exception(response.text)
        return response.text.split("^^")[1]
