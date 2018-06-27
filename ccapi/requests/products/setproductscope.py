"""setProductScope Request."""

from ..apirequest import APIRequest


class SetProductScope(APIRequest):
    """
    setProductScope Request.

    Sets several attributes for products.

    Sets weight, height, length, width, large letter compatibilty and
    external ID.
    """

    uri = 'Handlers/Products/setProductScope.ashx'

    def __new__(
            self,
            *,
            product_id,
            weight,
            height,
            length,
            width,
            large_letter_compatible,
            external_id=''):
        """
        Create setProductScope request.

        Args:
            product_id: ID of Product to update.
            weight: Product weight in grams.
            height: Product height in mm.
            length: Product lenght in mm.
            width: Product width in mm.
            large_letter_compatible: (bool) Item can be shipped as Large
                Letter.
            external_id: External ID of product.
        """
        self.product_id = product_id
        self.weight = weight
        self.height = height
        self.length = length
        self.width = width
        self.large_letter_compatible = large_letter_compatible
        self.external_id = external_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response,
            'Error setting product scope for product with ID "{}".'.format(
                self.product_id))
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            'ProductID': self.product_id,
            'Weight': self.weight,
            'Height': self.height,
            'Length': self.length,
            'Width': self.width,
            'LargeLetterCompatible': int(bool(self.large_letter_compatible)),
            'ExternalID': self.external_id
        }

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '920'}
