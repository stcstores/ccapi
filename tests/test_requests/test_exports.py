"""Tests for exports requests."""

import ccapi

from .. import test_data
from .test_request import TestRequest


class TestGetProductExportUpdate(TestRequest):
    """Tests for the GetProductExportUpdate request."""

    request_class = ccapi.requests.exports.GetProductExportUpdate

    RESPONSE = test_data.GET_PRODUCT_EXPORT_UPDATE_RESPONSE

    def test_GetProductExportUpdate_request(self):
        """Test the GetProductUpdate request."""
        self.register(json=self.RESPONSE)
        self.mock_request()
        self.assertDataSent("brandID", 341)

    def test_raises_for_non_200(self):
        """Test request raises for non 200 response codes."""
        self.register(json=self.RESPONSE, status_code=500)
        with self.assertRaises(ccapi.exceptions.CloudCommerceResponseError):
            self.mock_request()
