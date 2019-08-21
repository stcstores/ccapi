"""Classes for holding information about multipack items."""
from decimal import Decimal


class MultipackInfo:
    """Container for multipack product information."""

    def __init__(self, product_id, *items):
        """
        Add multipack items.

        Args:
            product_id (str): The ID of the Multipack product to which the info applies.
            items (list[MultipackItem]): the items in the multipack

        """
        self.json = None
        self.product_id = product_id
        self.items = items
        for item in self.items:
            item.multipack_info = self

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    @property
    def price(self):
        """Return the price of the multipack based on it's items."""
        return sum((_.price * _.quantity for _ in self.items))

    @classmethod
    def load_json(cls, product_id, json):
        """Create MultilpackInfo from Cloud Commerce response."""
        items = [MultipackItem.load_json(_) for _ in json]
        info = cls(product_id, *items)
        info.json = json
        return info


class MultipackItem:
    """Container for multipack product items."""

    PRODUCT_ID = "links"
    QUANTITY = "quantity"
    PERCENT = "percent"
    PRICE = "prices"

    def __init__(self, *, product_id, quantity, price):
        """
        Create a multipack item.

        kwargs:
            product_id (str): The ID of an item in the multipack.
            quantity (int): The quantity of the product in the multipack.
            price (decimal.Decimal): The price of a single item.

        """
        self.multipack_info = None
        self.product_id = str(product_id)
        self.quantity = int(quantity)
        self.price = Decimal(price)

    @classmethod
    def load_json(cls, data):
        """Create MultipackItem from Cloud Commerce response."""
        item = cls(
            product_id=data[cls.PRODUCT_ID],
            quantity=data[cls.QUANTITY],
            price=Decimal(data[cls.PRICE][0]),
        )
        item.json = data
        return item

    @property
    def percent(self):
        """Return the percentage of the total multipack price contributed by this items."""
        percentage = ((self.price * self.quantity) / self.multipack_info.price) * 100
        return int(round(percentage))
