"""
customer request.

Handle customers.
"""

from .program_type_request import ProgramTypeRequest


class Customer(ProgramTypeRequest):
    """Customer request."""

    uri = "Handlers/Customer.ashx"

    def process_response(self, response):
        """Handle request response."""
        return response.text


class GetPaymentTerms(Customer):
    """Request to get payment term options."""

    PROGRAM_TYPE = "GetPaymentTerms"
    kwargs = {"PayTermID": 0}
