"""ProductOperations request."""

from ..apirequest import APIRequest


class ProductOperations(APIRequest):
    """ProductOperations request."""

    uri = "Handlers/Products/ProductOperations.ashx"
    GET_GENERATED_SKU = "getgeneratedsku"
    UPDATE_HS_CODE = "updatehscode"

    PRODUCT_IDS = "ProductIDs"
    HS_CODE = "HSCode"

    def __new__(self, request_mode, product_IDs=[], HS_code=None):
        """Create ProductOperations request.

        Args:
            request_mode: requestmode header

        """
        self.request_mode = request_mode
        self.product_IDs = (product_IDs,)
        self.HS_code = HS_code
        return super().__new__(self)

    def get_headers(self):
        """Get headers for request."""
        return {"requestmode": self.request_mode}

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "769"}

    def get_data(self):
        """Return request data."""
        data = None
        if self.request_mode == self.UPDATE_HS_CODE:
            data = {self.PRODUCT_IDS: self.product_IDs, self.HS_CODE: self.HS_code}
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, "Product Operations request returned an error code."
        )
        result = response.json()
        return ProductOperationsResult(result)


class ProductOperationsResult:
    """Response from ProductOperations request."""

    def __init__(self, result):
        """Get information from ProductOperations request."""
        self.success = result["Success"]
        self.message = result["Message"]
        self.record_count = result["RecordCount"]
        self.data = result["Data"]
