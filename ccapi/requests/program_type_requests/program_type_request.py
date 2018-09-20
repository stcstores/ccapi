"""Requests using the ProgramType form."""

from ccapi.requests import APIRequest


class ProgramTypeRequest(APIRequest):
    """Base class for requests using the program type form."""

    PROGRAM_TYPE = None
    kwargs = {}

    def __new__(self, program_type=None, **kwargs):
        """Create addCustomer request."""
        self.program_type = program_type or self.PROGRAM_TYPE
        self.kwargs = kwargs or self.kwargs
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {"ProgType": self.program_type}
        data.update(self.kwargs)
        return data

    def process_response(self, response):
        """Handle request response."""
        raise NotImplementedError()
