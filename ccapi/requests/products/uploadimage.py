"""
uploadImage request.

Add Product Image.
"""

from ccapi.exceptions import CloudCommerceResponseError

from ..apirequest import APIRequest


class UploadImage(APIRequest):
    """uploadImage request."""

    uri = 'Handlers/Products/uploadImage.ashx'
    SUCCESS_RESULT = 'OK'

    def __new__(self, *, product_ids, image_file, channel_ids=[]):
        """Create uploadImage request.

        Kwargs:
            product_ids: IDs of products to add image to.
            channel_ids: IDs of channels to add image to.
            image_file: File object containing the image to upload.
        """
        self.product_ids = [str(product_id) for product_id in product_ids]
        self.channel_ids = [str(channel_id) for channel_id in channel_ids]
        self.image_file = image_file
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response,
            'Error saving image for product ID(s) "{}".'.format(
                ', '.join(self.product_ids)))
        response_data = response.json()
        if response_data.get('result') == self.SUCCESS_RESULT:
            return response_data
        raise CloudCommerceResponseError(
            f'Image not saved for product(s) {", ".join(self.product_ids)}')

    def get_params(self):
        """Get parameters for get request."""
        return {
            'prodIDs': ','.join(self.product_ids),
            'channelids': ','.join(self.channel_ids),
            'brandID': '341'
        }

    def get_files(self):
        """Get file for request."""
        files = {'upload_file': self.image_file}
        return files
