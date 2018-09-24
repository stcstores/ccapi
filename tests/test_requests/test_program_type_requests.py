"""Tests for Program Type requests."""

import ccapi

from .test_request import TestRequest


class TestProgramTypeRequest(TestRequest):
    """Tests for the Customer request."""

    request_class = ccapi.requests.program_type_requests.Customer

    RESPONSE = "RESPONSE TEXT"
    TEST_KWARG = "Kwarg"
    TEST_KWARG_VALUE = "Value"
    PROGRAM_TYPE = "GetPaymentTerms"

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_Customer_returns_response_text(self):
        """Test the Customer request returns the response text."""
        response = self.mock_request(program_type=self.PROGRAM_TYPE)
        self.assertEqual(response, self.RESPONSE)

    def test_Customer_sends_program_type(self):
        """Test the Customer request sends a program type."""
        self.mock_request(program_type=self.PROGRAM_TYPE)
        self.assertDataSent("ProgType", self.PROGRAM_TYPE)

    def test_Customer_sends_kwargs(self):
        """Test the Customer request sends kwargs."""
        kwargs = {self.TEST_KWARG: self.TEST_KWARG_VALUE}
        self.mock_request(program_type=self.PROGRAM_TYPE, **kwargs)
        self.assertDataSent(self.TEST_KWARG, self.TEST_KWARG_VALUE)


class ProgramTypeRequestSubclass(TestRequest):
    """Base class for testing Program Type requests."""

    request_class = ccapi.requests.program_type_requests.GetPaymentTerms
    RESPONSE = ""

    def setUp(self):
        """Register request URI."""
        super().setUp()
        self.register(text=self.RESPONSE)

    def test_returns_response_text(self):
        """Test the Customer request returns the response text."""
        response = self.mock_request()
        self.assertEqual(response, self.RESPONSE)

    def test_sends_program_type(self):
        """Test the Customer request sends a program type."""
        self.mock_request()
        self.assertDataSent("ProgType", self.request_class.PROGRAM_TYPE)

    def test_sends_kwargs(self):
        """Test the Customer request sends kwargs."""
        self.mock_request()
        for key, value in self.request_class.kwargs.items():
            self.assertDataSent(key, value)

    def test_raises_for_non_200(self):
        """Test an exception is raised when a request recieved an error status code."""
        self.register(text=self.RESPONSE, status_code=500)
        with self.assertRaises(ccapi.exceptions.CloudCommerceResponseError):
            self.mock_request()


class TestGetPaymentTerms(ProgramTypeRequestSubclass):
    """Test the GetPaymentTerms request."""

    request_class = ccapi.requests.program_type_requests.customer.GetPaymentTerms

    RESPONSE = (
        "RecFound^^11^^10^^14 Days Credit^^2^^28 Days Credit^^8^^30 Days Credit"
        "^^6^^30% Deposit - Balance on Delivery^^5^^50% Upfront Balance in 30 Days"
        "^^3^^60 Days Credit^^9^^7 Days Credit^^39^^Cash On Delivery^^7^^Direct debit"
        "^^1^^Full Payment Before Dispatch^^4^^"
        "Full Payment With 10% Early Payment Discount"
    )


class TestUpdateCustomerAddress(ProgramTypeRequestSubclass):
    """Test the UpdateCustomerAddress request."""

    request_class = ccapi.requests.program_type_requests.customer.UpdateCustomerAddress

    NEW_ADDRESS_ID = "56664022"
    RESPONSE = f"Updated^^0Inserted^^{NEW_ADDRESS_ID}^^57706408"

    CUSTOMER_ID = 18748142
    ADDRESS_TYPE = request_class.DELIVERY
    COMPANY_NAME = "Joe's Blogs"
    FIRST_NAME = "Joe"
    LAST_NAME = "Blog"
    ADDRESS_1 = "1 The Street"
    ADDRESS_2 = "Churchford"
    POST_CODE = "L17 THX"
    TOWN = "Towningsville"
    REGION = "Southwestshire"
    COUNTRY = "United Kingdom"
    TELEPHONE_NUMBER = "04845 16815"
    FAX_NUMBER = "04813 541864"
    MOBILE_NUMBER = "07954 415 638"
    ADDRESS_ID = "96664037"
    CUSTOMER_ADD_LINK_ID = "0"

    def mock_request(self):
        """Make a mock request with self.request_class."""
        return super().mock_request(
            customer_id=self.CUSTOMER_ID,
            address_type=self.ADDRESS_TYPE,
            company_name=self.COMPANY_NAME,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            address_1=self.ADDRESS_1,
            address_2=self.ADDRESS_2,
            post_code=self.POST_CODE,
            town=self.TOWN,
            region=self.REGION,
            country=self.COUNTRY,
            telephone_number=self.TELEPHONE_NUMBER,
            fax_number=self.FAX_NUMBER,
            mobile_number=self.MOBILE_NUMBER,
            address_id=self.ADDRESS_ID,
            customer_add_link_id=self.CUSTOMER_ADD_LINK_ID,
        )
