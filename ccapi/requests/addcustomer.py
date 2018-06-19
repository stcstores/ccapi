"""
addCustomer request.

Add a new customer to Cloud Commerce.
"""

from .apirequest import APIRequest


class AddCustomer(APIRequest):
    """addCustomer request."""

    uri = 'Handlers/addCustomer.ashx'

    def __new__(
            self,
            account_id=None,
            account_name='',
            customer_name='',
            address_1='',
            address_2='',
            agent_id=0,
            company_fax='',
            company_mobile='',
            company_telephone='',
            contact_email='',
            contact_fax='',
            contact_name=None,
            contact_phone='',
            contact_mobile='',
            country='',
            county='',
            create=0,
            customer_type=8,
            eu_vat=True,
            link_to=0,
            post_code='',
            payment_terms='1^^1^^',
            town='',
            trade_name=None,
            vat_number='',
            selling_channel_id=None,
            special_instructions=''):
        """Create addCustomer request."""
        self.account_id = account_id
        self.account_name = account_name
        self.customer_name = customer_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.agent_id = agent_id
        self.company_fax = company_fax
        self.company_mobile = company_mobile
        self.company_telephone = company_telephone
        self.contact_email = contact_email
        self.contact_fax = contact_fax
        self.contact_name = contact_name or self.customer_name
        self.contact_mobile = contact_mobile
        self.contact_phone = contact_phone
        self.country = country
        self.county = county
        self.create = create
        self.customer_type = customer_type
        self.eu_vat = eu_vat
        self.link_to = link_to
        self.post_code = post_code
        self.payment_terms = payment_terms
        self.town = town
        self.trade_name = trade_name or self.customer_name
        self.vat_number = vat_number
        self.selling_channel_id = selling_channel_id
        self.special_instructions = special_instructions
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {
            'AccountID': self.account_id,
            'CustType': self.customer_type,
            'CustName': self.customer_name,
            'TradName': self.trade_name,
            'VATNo': self.vat_number,
            'agentID': self.agent_id,
            'scID': self.selling_channel_id,
            'oSCID': 0,
            'compTel': self.company_telephone,
            'compFax': self.company_fax,
            'compMob': self.company_mobile,
            'addr1': self.address_1,
            'addr2': self.address_2,
            'town': self.town,
            'pcode': self.post_code,
            'county': self.county,
            'country': self.country,
            'contName': self.contact_name,
            'contEmail': self.contact_email,
            'contPhone': self.contact_phone,
            'contFax': self.contact_fax,
            'contMob': self.contact_mobile,
            'create': self.create,
            'pterms': self.payment_terms,
            'linkTo': self.link_to,
            'EUVAT': int(bool(self.eu_vat)),
            'SpecInstr': int(bool(self.special_instructions)),
            'SpecInstrNote': self.special_instructions,
            'AcctName': self.account_name,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        try:
            response.raise_for_status()
        except Exception:
            raise Exception(response.text)
        return response.text.split('^^')[1]
