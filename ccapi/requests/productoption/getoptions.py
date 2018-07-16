"""GetOptions request.

Gets list of available product options.
"""

from ccapi.cc_objects import ProductOption, ProductOptions

from ..apirequest import APIRequest


class GetOptions(APIRequest):
    """Wrapper for GetOptions request."""

    uri = 'Handlers/ProductOption/getOptions.ashx'

    def process_response(self, response):
        """Handle request response."""
        results = response.json()
        return ProductOptions([ProductOption(item) for item in results])

    def get_data(self):
        """Get data for request."""
        return {'brandID': "341", 'strOptionTypes': "1,+2,+6"}
