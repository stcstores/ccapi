"""ProductImage class."""

from ccapi import ccapi


class ProductImage:
    """Container for a Product Image."""

    def __init__(self, url):
        """
        Create ProductImage.

        Args:
            url: URL for Product Image.
        """
        self.url = url
        self.filename = url.split("/")[-1]
        self.id = self.filename.split(".")[0]
        self.extension = self.filename.split(".")[-1]

    def delete(self):
        """Delete this Product Image."""
        return ccapi.CCAPI.delete_image(self.id)
