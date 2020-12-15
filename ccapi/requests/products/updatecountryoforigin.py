"""updateProductBasePrice Request."""

from ..apirequest import APIRequest


class UpdateCountryOfOrigin(APIRequest):
    """
    updateCountryOfOrigin Request.

    Sets the country of origin for a product.
    """

    uri = "Handlers/Products/updateCountryOfOrigin.ashx"

    def __new__(self, *, product_id, country_id):
        """
        Create updateCountryOfOrigin request.

        Args:
            product_id: ID of Product to update.
            country_id: The ID of the country of origin.
        """
        self.product_id = product_id
        self.country_id = country_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Error setting country of origin for product with ID "{}".'.format(
                self.product_id
            ),
        )
        return response.text

    def get_data(self):
        """Get data for request."""
        return {"prodid": self.product_id, "countryid": self.country_id}
