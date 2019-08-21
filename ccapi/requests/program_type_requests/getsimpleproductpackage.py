"""
getSimpleProductPackage request.

Handle customers.
"""

from ccapi.cc_objects import MultipackInfo, MultipackItem

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

    MULTIPACK_PRODUCT_ID = "ProductID"
    DEFINITION = "Defn"

    error_message = "Failed to create multipack."

    def __new__(self, multipack_product_id, *items):
        """
        Set multipack items for a multipack product.

        Note: This request puts swaps the ID of the multipack item and the first item being
        added to it.

        Args:
            multipack_product_id (str): Product ID of the multipack item to be added too.
            *items (tuple): Tuple(multipack item ID, quantity, item_price) for each item
                in the multipack.

        """
        self.multipack_product_id = multipack_product_id
        self.items = MultipackInfo(
            self.multipack_product_id,
            *(
                MultipackItem(product_id=product_id, quantity=quantity, price=price)
                for product_id, quantity, price in items
            ),
        )
        self.kwargs = {
            self.MULTIPACK_PRODUCT_ID: self.items[0].product_id,
            self.DEFINITION: self.create_definition(self, self.items),
        }
        return super().__new__(self)

    def create_definition(self, items):
        """
        Return a multipack items definition string.

        Note: The multipack product ID and the first item ID are swapped.
        """
        items = items[:]
        items[0].product_id = self.multipack_product_id
        definition = "".join(
            (SaveSimplePackage.create_item_definition(item) for item in items)
        )
        print(definition)
        return definition

    @staticmethod
    def create_item_definition(item):
        """Return a multipack item definition string."""
        return f"^{item.product_id}~{item.percent}~{item.quantity}"


class GetSimplePackage(GetSimpleProductPackage):
    """Return multipack information for a multipack product."""

    PROGRAM_TYPE = "GetSimplePackage"

    error_message = "Failed to get multipack item information."

    MULTIPACK_PRODUCT_ID = "ProductID"

    def __new__(self, multipack_product_id):
        """Return multipack information for a multipack product."""
        self.multipack_product_id = multipack_product_id
        self.kwargs = {self.MULTIPACK_PRODUCT_ID: self.multipack_product_id}
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        super().process_response(self, response)
        return MultipackInfo.load_json(self.multipack_product_id, response.json())
