"""
uploadImage request.

Add Product Image.
"""

from ..apirequest import APIRequest


class UploadImage(APIRequest):
    """deleteImage request."""

    uri = 'Handlers/Products/uploadImage.ashx'

    def __new__(self, product_ids=[], channel_ids=[], image_file=None):
        """Create deleteImage request.

        Kwargs:
            product_ids: IDs of products to add image to.
            channel_ids: IDs of channels to add image to.
            image_file: File to upload.
        """
        self.product_ids = [str(product_id) for product_id in product_ids]
        self.channel_ids = [str(channel_id) for channel_id in channel_ids]
        self.image_file = image_file
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response

    def get_params(self):
        """Get parameters for get request."""
        return {
            'prodIDs': ','.join(self.product_ids),
            'channelids': ','.join(self.channel_ids),
            'brandID': '341'}

    def get_files(self):
        """Get file for request."""
        files = {'upload_file': self.image_file}
        return files
