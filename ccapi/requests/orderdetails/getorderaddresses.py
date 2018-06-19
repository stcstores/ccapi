"""
getOrderAddresses request.

Get addresses associated with an order.
"""

from ..apirequest import APIRequest


class GetOrderAddresses(APIRequest):
    """getOrderAddresses request."""

    uri = '/Handlers/OrderDetails/getOrderAddresses.ashx'

    def __new__(self, order_id, customer_id):
        """Create getOrderAddresses request.

        args:
            order_id: ID of order.
            customer_id: ID of customer.
        """
        self.order_id = order_id
        self.customer_id = customer_id
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {"OrderID": self.order_id, "CustID": self.customer_id}
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '57'}

    def process_response(self, response):
        """Handle request response."""
        data = response.json()
        return Addresses(**data)


class Addresses:
    """Container for addresses associated with an order."""

    def __init__(self, **kwargs):
        """
        Create Adresses object.

        Kwargs:
            DeliveryAddress: dict containing information about a
                delivery address.
            BillingAddress: dict containing information about a
                billing address.
        """
        if 'DeliveryAddress' in kwargs:
            self.delivery_address = Address(data=kwargs['DeliveryAddress'])
        if 'BillingAddress' in kwargs:
            self.billing_address = Address(data=kwargs['BillingAddress'])


class Address:
    """Container for an address associated with an order."""

    def __init__(self, data=None):
        """
        Create Address object.

        Kwargs:
            data: dict containing information about an address.
        """
        if data is not None:
            self.load_from_request(data)

    def load_from_request(self, data):
        """Set attributes from request response."""
        self.json = data
        self.id = data['ID']
        self.address_id = data['AddressID']
        self.delivery_name = data['DeliveryName']
        self.address_as_string = data['AddressAsString']
        self.first_name = data['FirstName']
        self.last_name = data['LastName']
        self.address = [data['Address1'], data['Address2']]
        self.post_code = data['PostCode']
        self.town_city = data['TownCity']
        self.country = data['Country']
        self.country_id = data['CountryID']
        self.county_region = data['CountyRegion']
        self.status_id = data['StatusID']
        self.company = data['Company']
        self.tel_no = data['TelNo']
        self.fax_no = data['FaxNo']
        self.mob_no = data['MobNo']
        self.enabled = data['Enabled']
        if 'OrderID' in data:
            self.order_id = data['OrderID']
        else:
            self.order_id = None
