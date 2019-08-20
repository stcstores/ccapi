"""setProductType Request."""

from ..apirequest import APIRequest


class SetProductType(APIRequest):
    """
    setProductType Request.

    Sets the product type of the product.
    """

    uri = "Handlers/Products/setProductType.ashx"

    PRODUCT_ID = "ProductID"
    TYPE = "Type"

    STANDARD = 0
    MULTIPACK = 1

    def __new__(self, *, product_id, type):
        """
        Create setProductType request.

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
        self.type = type
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Error setting product type for "{}".'.format(self.product_id),
        )
        return response.text

    def get_data(self):
        """Get data for request."""
        return {self.PRODUCT_ID: self.product_id, self.TYPE: self.type}
