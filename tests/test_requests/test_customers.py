"""Tests for customers requests."""

import datetime

import ccapi

from .test_request import TestRequest


class TestGetLogs(TestRequest):
    """Test the GetLogs request."""

    request_class = ccapi.requests.customers.GetLogs

    RESPONSE = [
        {
            "DateStampString": "05/11/2018 10:23",
            "ID": 367033441,
            "AddedByLoginID": 1000000,
            "Note": "Message Text",
            "NoteSnippet": None,
            "Name": "MessageCentreMessages",
            "UserName": "user@example.co.uk",
            "AddedByUser": "System",
            "DateStamp": "0001-01-01T00:00:00",
            "LogTypeID": 18,
            "LoginID": 20722015,
            "StatusID": 1,
            "CustomerID": 0,
            "ContentHTML": "...",
            "LogIcon": 5,
            "MessagingID": 0,
        }
    ]

    CUSTOMER_ID = "367033441"

    CustomerLog = ccapi.requests.customers.getlogs.CustomerLog

    def test_GetLogs_request(self):
        """Test GetLogs sends a customer ID."""
        self.register(json=self.RESPONSE)
        self.mock_request(self.CUSTOMER_ID)
        self.assertDataSent("CustID", self.CUSTOMER_ID)

    def test_returns_CustomerLog(self):
        """Test the GetLogs request returns an instance of CustomerLog."""
        self.register(json=self.RESPONSE)
        response = self.mock_request(self.CUSTOMER_ID)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], self.CustomerLog)

    def test_CustomerLog_attributes(self):
        """Test the returned CustomerLog instance is valid."""
        self.register(json=self.RESPONSE)
        response = self.mock_request(self.CUSTOMER_ID)
        response_data = self.RESPONSE[0]
        log = response[0]
        self.assertEqual(
            log.customer_ID, str(response_data[self.CustomerLog.CUSTOMER_ID])
        )
        self.assertIsInstance(log.timestamp, datetime.datetime)
        self.assertEqual(log.note, response_data[self.CustomerLog.NOTE])
        self.assertEqual(log.note_snippet, response_data[self.CustomerLog.NOTE_SNIPPET])
        self.assertEqual(log.name, response_data[self.CustomerLog.NAME])
        self.assertEqual(
            log.customer_user_name, response_data[self.CustomerLog.CUSTOMER_USER_NAME]
        )
        self.assertEqual(
            log.added_by_username, response_data[self.CustomerLog.ADDED_BY_USERNAME]
        )
        self.assertEqual(
            log.added_by_user_ID, response_data[self.CustomerLog.ADDED_BY_USER_ID]
        )
        self.assertEqual(log.log_type_ID, response_data[self.CustomerLog.LOG_TYPE_ID])
        self.assertEqual(log.login_ID, str(response_data[self.CustomerLog.LOGIN_ID]))
        self.assertEqual(log.status_ID, response_data[self.CustomerLog.STATUS_ID])
        self.assertEqual(log.HTML_content, response_data[self.CustomerLog.HTML_CONTENT])
        self.assertEqual(log.log_icon, response_data[self.CustomerLog.LOG_ICON])
        self.assertEqual(log.message_ID, response_data[self.CustomerLog.MESSAGE_ID])

    def test_empty_response(self):
        """Test the GetLogs requests returns an empty list when no logs exist."""
        self.register(json=[])
        response = self.mock_request(self.CUSTOMER_ID)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 0)

    def test_raises_for_non_200(self):
        """Test request raises for non 200 response codes."""
        self.register(json=[], status_code=500)
        with self.assertRaises(ccapi.exceptions.CloudCommerceResponseError):
            self.mock_request(self.CUSTOMER_ID)
