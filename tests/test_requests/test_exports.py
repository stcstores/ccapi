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


class TestRequestProductExport(TestRequest):
    """Tests for the RequestProductExport request."""

    request_class = ccapi.requests.exports.RequestProductExport

    RESPONSE = "OK"

    def test_RequestProductExport_request(self):
        """Test the RequestProductExport request."""
        self.register(text=self.RESPONSE)
        returned_value = self.mock_request(copy_images=False)
        self.assertTrue(returned_value)
        self.assertDataSent(self.request_class.COPY, 0)

    def test_copy_images_parameter(self):
        """Test the copy_images parameter is sent."""
        self.register(text=self.RESPONSE)
        self.mock_request(copy_images=True)
        self.assertDataSent(self.request_class.COPY, 1)

    def test_copy_images_defaults_to_false(self):
        """Test the default value of copy_images is False."""
        self.register(text=self.RESPONSE)
        self.mock_request()
        self.assertDataSent(self.request_class.COPY, 0)

    def test_raises_for_non_200(self):
        """Test request raises for non 200 response codes."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(ccapi.exceptions.CloudCommerceResponseError):
            self.mock_request()


class TestViewFile(TestRequest):
    """Tests for the ViewFile request."""

    request_class = ccapi.requests.exports.ViewFile

    RESPONSE = test_data.PRODUCT_EXPORT_FILE
    FILE_NAME = "ProductExport9999"

    def test_request(self):
        """Test the ViewFile request."""
        self.register(content=self.RESPONSE)
        response = self.mock_request(self.FILE_NAME)
        self.assertEqual(response.content, self.RESPONSE)
        self.assertQuerySent(self.request_class.NAME, self.FILE_NAME)
        self.assertQuerySent(self.request_class.DISP, self.request_class.DISP_VALUE)
        self.assertQuerySent(
            self.request_class.BRAND_ID, self.request_class.BRAND_ID_VALUE
        )

    def test_raises_for_non_200(self):
        """Test request raises for non 200 response codes."""
        self.register(content=self.RESPONSE, status_code=500)
        with self.assertRaises(ccapi.exceptions.CloudCommerceResponseError):
            self.mock_request(self.FILE_NAME)
