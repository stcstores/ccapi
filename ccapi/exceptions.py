"""Exceptions for the ccapi package."""


class BaseCloudCommerceAPIError(Exception):
    """Base exception for ccapi errors."""

    pass


class NotLoggedInError(Exception):
    """Raised when login information is not available."""

    def __init__(self):
        """Raise exception."""
        super().__init__("No session Cloud Commerce session exists.")


class CloudCommerceResponseError(BaseCloudCommerceAPIError):
    """Exception for failed API Requests."""

    def __init__(self, message="API Request failed."):
        """Raise exception."""
        super().__init__(message)


class CloudCommerceNoResponseError(BaseCloudCommerceAPIError):
    """Handler for RemoteDisconnected errors."""

    def __init__(self):
        """Raise exception."""
        super().__init__("Cloud Commerce Pro did not respond")


class ProductNotFoundError(BaseCloudCommerceAPIError):
    """Raised when retrieving product information fails."""

    def __init__(self, product_id):
        """Raise exception."""
        super().__init__(
            'Product information not found for product ID "{}"'.format(product_id)
        )
