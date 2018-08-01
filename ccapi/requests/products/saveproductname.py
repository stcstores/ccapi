"""
saveProductName request.

Set name of Product.
"""

from ..apirequest import APIRequest


class SaveProductName(APIRequest):
    """setOptionSelect request."""

    uri = "Handlers/Products/saveProductName.ashx"

    def __new__(self, *, name, product_ids):
        """Create saveProductName request.

        Args:
            name: New name for Product.
            product_ids: IDs of Products to update.

        """
        self.name = name
        if isinstance(product_ids, str) or isinstance(product_ids, int):
            self.product_ids = [str(product_ids)]
        else:
            self.product_ids = [str(x) for x in product_ids]
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            "prodids": ",".join([str(x) for x in self.product_ids]),
            "name": self.name,
            "channelID": 0,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self,
            response,
            "Error saving name for product ID(s) {}".format(
                ", ".join(self.product_ids)
            ),
        )
        return response.text
