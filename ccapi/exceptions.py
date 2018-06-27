"""Exceptions for the ccapi package."""


class CloudCommerceResponseError(Exception):
    """Exception for failed API Requests."""

    def __init__(self, message='API Request failed.'):
        """Raise exception."""
        super().__init__(message)


class CloudCommerceNoResponseError(CloudCommerceResponseError):
    """Handler for RemoteDisconnected errors."""

    def __init__(self):
        """Raise exception."""
        super(Exception, self).__init__('Cloud Commerce Pro did not respond')


class ProductNotCreatedError(CloudCommerceResponseError):
    """Exception for product creation failures."""

    def __init__(self):
        """Raise exception."""
        super(Exception, self).__init__('Product creation failed.')


class ProductNotFoundError(CloudCommerceResponseError):
    """Exception for failed requests for product data."""

    def __init__(self, product_ID):
        """Raise exception."""
        super(Exception, self).__init__(
            'Product not found with ID "{}"'.format(product_ID))


class DescriptionNotSavedError(CloudCommerceResponseError):
    """Exception for a failure when updating a product description."""

    def __init__(self, product_ids):
        """Raise exception."""
        super(Exception, self).__init__(
            'Product description not saved for product IDs "{}"'.format(
                product_ids))


class ProductNameNotSavedError(CloudCommerceResponseError):
    """Exception for a failure when updating a product name."""

    def __init__(self, product_ids):
        """Raise exception."""
        super(Exception, self).__init__(
            'Product name not saved for product IDs "{}"'.format(product_ids))


class ProductOptionValueNotSavedError(CloudCommerceResponseError):
    """Exception for a failure when updating a product name."""

    def __init__(self, product_ids):
        """Raise exception."""
        super(Exception, self).__init__(
            'Product Option Value not saved for product IDs "{}"'.format(
                product_ids))
