"""updateProductVatRate request.

Set VAT rate for Product.
"""

from ..apirequest import APIRequest


class UpdateProductVatRate(APIRequest):
    """updateProductVatRate request."""

    uri = "Handlers/Products/updateProductVatRate.ashx"

    def __new__(self, *, product_ids, vat_rate_id):
        """
        Create updateProductVatRate request.

        Args:
            product_ids: List containing IDs of products to update.
            vat_rate_id: ID of new VAT rate.
        """
        if isinstance(product_ids, str) or isinstance(product_ids, int):
            self.product_ids = [str(product_ids)]
        else:
            self.product_ids = [str(x) for x in product_ids]
        self.vat_rate_id = int(vat_rate_id)
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        return {
            "prodids": ",".join([str(x) for x in self.product_ids]),
            "vatrate": self.vat_rate_id,
        }

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            'Error saving VAT rate for product IDs "{}".'.format(
                ", ".join(self.product_ids)
            ),
        )
        return response.text
