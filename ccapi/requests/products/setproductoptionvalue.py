"""setProductOptionValue Request."""

from ..apirequest import APIRequest


class SetProductOptionValue(APIRequest):
    """
    SetProductOptionValue Request.

    Applies a Product Option Value to a set of products.
    """

    uri = "Handlers/Products/setProductOptionValue.ashx"

    def __new__(self, *, product_ids, option_id, option_value_id):
        """
        Create setProductOptionValue request.

        Args:
            product_ids: Tuple of products to which the value will be applied.
            option_id: ID of Product Option to set.
            value_id: ID of Product Option Value to set.
        """
        if isinstance(product_ids, str) or isinstance(product_ids, int):
            self.product_ids = [str(product_ids)]
        else:
            self.product_ids = [str(x) for x in product_ids]
        self.option_id = option_id
        self.option_value_id = option_value_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            (
                'Error setting product option value with ID "{}" for product '
                'option with ID "{}" on product(s) with ID(s) "{}".'
            ).format(self.option_value_id, self.option_id, ", ".join(self.product_ids)),
        )
        return response.text

    def get_data(self):
        """Get data for request."""
        return {
            "prodids": ",".join(self.product_ids),
            "OptionID": int(self.option_id),
            "OptionValueID": int(self.option_value_id),
        }

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "178"}
