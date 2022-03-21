"""Classes for holding information about multipack items."""


class MultipackInfo:
    """Container for multipack product information."""

    def __init__(self, data):
        """
        Add multipack items.

        Args:
            product_id (str): The ID of the Multipack product to which the info applies.
            items (list[MultipackItem]): the items in the multipack

        """
        self.json = data
        self.items = [MultipackItem(_) for _ in self.json]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    @property
    def price(self):
        """Return the price of the multipack based on it's items."""
        return sum((_.price * _.quantity for _ in self.items))


class MultipackItem:
    """Container for multipack product items."""

    PRODUCT_ID = "links"
    QUANTITY = "quantity"
    PERCENT = "percent"
    PRICE = "prices"

    def __init__(self, data):
        """Create a multipack item."""
        self.json = data
        self.name = data["Name"]
        self.product_id = str(data["ProductID"])
        self.range_id = str(data["RangeID"])
        self.quantity = int(data["Quantity"])
        self.product_price_percentage = int(data["ProductPricePercentage"])
