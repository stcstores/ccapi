"""ProductOperations request."""

from ..apirequest import APIRequest


class ProductOperations(APIRequest):
    """ProductOperations request."""

    uri = 'Handlers/Products/ProductOperations.ashx'

    def __new__(self, request_mode):
        """Create ProductOperations request.

        Args:
            request_mode: requestmode header
        """
        self.request_mode = request_mode
        return super().__new__(self)

    def get_headers(self):
        """Get headers for request."""
        return {'requestmode': self.request_mode}

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '769'}

    def process_response(self, response):
        """Handle request response."""
        result = response.json()
        return ProductOperationsResult(result)


class ProductOperationsResult:
    """Response from ProductOperations request."""

    def __init__(self, result):
        """Get information from ProductOperations request."""
        self.success = result['Success']
        self.message = result['Message']
        self.record_count = result['RecordCount']
        self.data = result['Data']
