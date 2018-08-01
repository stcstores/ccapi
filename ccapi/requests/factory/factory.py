"""
Factory request.

Work with Factories.
"""

from ..apirequest import APIRequest


class Factory(APIRequest):
    """Factory request."""

    UPDATE_FACTORY = "UpdFactory"
    DELETE_FACTORY = "delFactory"

    uri = "/Handlers/Factory/Factory.ashx"

    def __new__(
        self,
        prog_type=None,
        comp_to_del=None,
        currency_symbol=None,
        delivery_method=None,
        exchange_rate=None,
        factory_id=None,
        name=None,
        nominal_code=None,
        order_to_comp=None,
    ):
        """Make factory request."""
        self.prog_type = prog_type
        self.comp_to_del = comp_to_del
        self.currency_symbol = currency_symbol
        self.delivery_method = delivery_method
        self.exchange_rate = exchange_rate
        self.factory_id = factory_id
        self.name = name
        self.nominal_code = nominal_code
        self.order_to_comp = order_to_comp
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        if self.prog_type == self.UPDATE_FACTORY:
            return {
                "ProgType": self.prog_type,
                "ComptoDel": self.comp_to_del or "",
                "CurrencySymbol": self.currency_symbol or "",
                "DeliveryMethod": self.delivery_method or "",
                "ExchangeRate": self.exchange_rate or "",
                "FactoryID": self.factory_id,
                "Name": self.name or "",
                "NominalCode": self.nominal_code or "",
                "OrderToComp": self.order_to_comp or "",
            }
        if self.prog_type == self.DELETE_FACTORY:
            return {"ProgType": self.prog_type, "FactoryID": self.factory_id}

    def process_response(self, response):
        """Handle request response."""
        if self.prog_type == self.UPDATE_FACTORY:
            return int(response.text.split("^^")[1])
        if self.prog_type == self.DELETE_FACTORY:
            response.raise_for_status()
            return response
