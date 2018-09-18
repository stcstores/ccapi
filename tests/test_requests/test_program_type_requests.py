"""Tests for Program Type requests."""

from ccapi.requests import program_type_requests

from .test_request import TestRequest


class TestProgramTypeRequest(TestRequest):
    """Tests for the Customer request."""

    request_class = program_type_requests.Customer

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

    request_class = program_type_requests.GetPaymentTerms
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


class TestGetPaymentTerms(ProgramTypeRequestSubclass):
    """Test the GetPaymentTerms request."""

    request_class = program_type_requests.GetPaymentTerms

    RESPONSE = (
        "RecFound^^11^^10^^14 Days Credit^^2^^28 Days Credit^^8^^30 Days Credit"
        "^^6^^30% Deposit - Balance on Delivery^^5^^50% Upfront Balance in 30 Days"
        "^^3^^60 Days Credit^^9^^7 Days Credit^^39^^Cash On Delivery^^7^^Direct debit"
        "^^1^^Full Payment Before Dispatch^^4^^"
        "Full Payment With 10% Early Payment Discount"
    )
