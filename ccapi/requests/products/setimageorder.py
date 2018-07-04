"""
setImageOrder request.

Reorder images for Product.
"""

from ..apirequest import APIRequest


class SetImageOrder(APIRequest):
    """setImageOrder request."""

    uri = 'Handlers/Products/setImageOrder.ashx'

    def __new__(self, *, product_id=None, image_ids=[]):
        """Create setImageOrder request.

        Kwargs:
            product_id: ID of Product for which Images will be ordered.
            image_order: List containing IDs of images in updated order.
        """
        self.product_id = product_id
        self.image_ids = [str(image_id) for image_id in image_ids]
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response,
            f'Image order not saved for product with ID {self.product_id}.')
        return response.text

    def get_data(self):
        """Get parameters for get request."""
        return {'prodid': self.product_id, 'order': '^^'.join(self.image_ids)}
