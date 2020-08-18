"""CommonDataSource request."""

import json

from ccapi.requests import APIRequest


class CommonDataSource(APIRequest):
    """CommonDataSource request."""

    uri = "Handlers/Common/CommonDataSource.ashx"

    SEARCH_TERM = "searchTerm"

    def __new__(self, search_term):
        """Search for an HS Code."""
        self.search_term = search_term
        return super().__new__(self)

    def get_data(self):
        """Get data for get request."""
        data = {self.SEARCH_TERM: self.search_term}
        return data

    def get_headers(self):
        """Return request headers."""
        return {"requestmode": "hscodes"}

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, "Failed to get HS code options")
        try:
            codes = json.loads(response.json()["Data"])
            return {item["Name"]: item["Description"] for item in codes}
        except Exception as e:
            raise Exception(f"Failed to parse response: {str(e)}")
