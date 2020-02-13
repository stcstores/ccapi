"""
GetLogs request.

Return a log of changes made to orders for a customer.
"""

import datetime

from ..apirequest import APIRequest


class GetLogs(APIRequest):
    """GetLogs request."""

    uri = "Handlers/Customers/GetLogs.ashx"

    def __new__(self, customer_id, added_by=None, log_type=None, number_of_records=100):
        """Create GetLogs request.

        args:
            customer_id: ID of customer.

        """
        self.customer_id = customer_id
        self.added_by = added_by or 0
        self.log_type = log_type or 0
        self.number_of_records = number_of_records
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            "AddedBy": self.added_by,
            "CustID": self.customer_id,
            "LogType": self.log_type,
            "NoRecords": self.number_of_records,
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(self, response, "Error retrieving customer logs.")
        return [CustomerLog(log) for log in response.json()]


class CustomerLog:
    """Wrapper for Cloud Commerce customer log records."""

    TIMESTAMP = "DateStampString"
    CUSTOMER_ID = "ID"
    NOTE = "Note"
    NOTE_SNIPPET = "NoteSnippet"
    NAME = "Name"
    CUSTOMER_USER_NAME = "UserName"
    ADDED_BY_USERNAME = "AddedByUser"
    ADDED_BY_USER_ID = "AddedByLoginID"
    LOG_TYPE_ID = "LogTypeID"
    LOGIN_ID = "LoginID"
    STATUS_ID = "StatusID"
    HTML_CONTENT = "ContentHTML"
    LOG_ICON = "LogIcon"
    MESSAGE_ID = "MessagingID"

    def __init__(self, raw):
        """Create log record from API response."""
        self.raw = raw
        self.timestamp = self.parse_timestamp(raw[self.TIMESTAMP])
        self.customer_ID = str(raw[self.CUSTOMER_ID])
        self.note = raw[self.NOTE]
        self.note_snippet = raw[self.NOTE_SNIPPET]
        self.name = raw[self.NAME]
        self.customer_user_name = raw[self.CUSTOMER_USER_NAME]
        self.added_by_username = raw[self.ADDED_BY_USERNAME]
        self.added_by_user_ID = raw[self.ADDED_BY_USER_ID]
        self.log_type_ID = raw[self.LOG_TYPE_ID]
        self.login_ID = str(raw[self.LOGIN_ID])
        self.status_ID = raw[self.STATUS_ID]
        self.HTML_content = raw[self.HTML_CONTENT]
        self.log_icon = raw[self.LOG_ICON]
        self.message_ID = raw[self.MESSAGE_ID]

    @staticmethod
    def parse_timestamp(timestamp_string):
        """Return log date string as datetime.datetime.

        Convert a timestamp in the format "05/11/2018 10:23" to a datetime.datetime
        object.
        """
        date, time = timestamp_string.split(" ")
        day, month, year = [int(_) for _ in date.split("/")]
        hour, minute = [int(_) for _ in time.split(":")]
        timestamp = datetime.datetime(
            day=day, month=month, year=year, hour=hour, minute=minute
        )
        return timestamp
