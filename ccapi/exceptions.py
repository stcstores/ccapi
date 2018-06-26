"""Exceptions for the ccapi package."""

import http


class CloudCommerceNoResponseError(http.client.RemoteDisconnected):
    """Handler for RemoteDisconnected errors."""

    pass


class ProductNotCreatedError(Exception):
    """Exception for product creation failures."""

    def __init__(self):
        """Raise exception."""
        super().__init__('Product creation failed.')
