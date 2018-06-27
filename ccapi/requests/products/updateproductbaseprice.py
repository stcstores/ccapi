"""updateProductBasePrice Request."""

from ..apirequest import APIRequest


class UpdateProductBasePrice(APIRequest):
    """
    updateProductBasePrice Request.

    Sets base price for product.
    """

    uri = 'Handlers/Products/updateProductBasePrice.ashx'

    def __new__(self, *, product_id, price):
        """
        Create updateProductBasePrice request.

        Args:
            product_id: ID of Product to update.
            price: New base price for Product.
        """
        self.product_id = product_id
        self.price = price
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response,
            'Error setting base price for product with ID "{}".'.format(
                self.product_id))
        return response.text

    def get_data(self):
        """Get data for request."""
        return {'prodid': self.product_id, 'price': self.price}

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '917'}
