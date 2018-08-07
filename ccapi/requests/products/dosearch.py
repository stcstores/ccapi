"""
DoSearch request.

Searches for products.
"""

from ..apirequest import APIRequest


class DoSearch(APIRequest):
    """DoSearch request."""

    uri = "Handlers/Products/doSearch.ashx"

    def __new__(self, text):
        """
        Create Do Search request.

        Args:
            text: Text string to search
        """
        self.text = text
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, 'Search for "{}" failed.'.format(self.text)
        )
        results = response.json()
        return [DoSearchResult(item) for item in results]

    def get_data(self):
        """Get data for request."""
        return {"brandid": "341", "text": self.text, "type": "range"}


class DoSearchResult:
    """Response from DoSearch request."""

    def __init__(self, result):
        """Get information from search result."""
        self.id = result["ID"]
        self.variation_id = result["variationID"]
        self.name = result["Name"]
        self.sku = result["SKU"]
        self.thumbnail = result["Thumbnail"]

    def __repr__(self):
        return self.name
