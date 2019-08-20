"""
getSimpleProductPackage request.

Handle customers.
"""

from .program_type_request import ProgramTypeRequest


class GetSimpleProductPackage(ProgramTypeRequest):
    """getSimpleProductPackage request."""

    uri = "Handlers/Products/getSimpleProductPackage.ashx"

    def process_response(self, response):
        """Handle request response."""
        super().process_response(self, response)
        return response.json()


class SaveSimplePackage(GetSimpleProductPackage):
    """Create a multipack."""

    PROGRAM_TYPE = "SaveSimplePackage"

    MULTIPACK_ITEM_PRODUCT_ID = "ProductID"
    DEFINITION = "Defn"

    error_message = "Failed to create multipack."

    def __new__(
        self,
        *,
        multipack_product_id,
        multipack_item_product_id,
        price_percentage,
        quantity,
    ):
        """
        Add an item to a multipack product.

        Kwargs:
            multipack_product_id (str): Product ID of the multipack item to be added too.
            multipack_item_product_id (str): Product ID of the item to be added.
            price_percentage (str): The percentage of the item price to add to the
                multipack price.
            quantity (int): The number of the item that appears in the multipack.

        """
        self.multipack_product_id = multipack_product_id
        self.multipack_item_product_id = multipack_item_product_id
        self.price_percentage = price_percentage
        self.quantity = quantity
        self.kwargs = {
            self.MULTIPACK_ITEM_PRODUCT_ID: self.multipack_item_product_id,
            self.DEFINITION: self.create_definition(self),
        }
        return super().__new__(self)

    def create_definition(self):
        """Return a multipack item definition string."""
        return f"^{self.multipack_product_id}~{self.price_percentage}~{self.quantity}"
