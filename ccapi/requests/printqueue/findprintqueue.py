"""
FindPrintQueue request.

Get the current contents of the Print Queue.
"""

from datetime import datetime

from ..apirequest import APIRequest


class FindPrintQueue(APIRequest):
    """GetProductsForRange request."""

    uri = '/Handlers/PrintQueue/FindPrintQueue.ashx'

    def __new__(self):
        """Create FindPrintQueue request."""
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {'ProgType': 'normal', 'brandID': '341', 'UnprintedOnly': False}
        return data

    def get_params(self):
        """Get parameters for get request."""
        return {'d': '57'}

    def process_response(self, response):
        """Handle request response."""
        print_queue = [PrintQueueItem(item) for item in response.json()]
        print_queue.sort()
        return print_queue


class PrintQueueItem:
    """Container for Cloud Commerce Print Queue items."""

    def __gt__(self, other):
        return self.date_created > other.date_created

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return 'Order {} for {}'.format(self.order_id, self.customer_name)

    def __init__(self, data):
        """Load from Cloud Commerce API response."""
        self.json = data
        self.file_type_enum = data['FileTypeEnum']
        self.triggered_by = data['TriggeredBy']
        self.customer_name = data['CustomerName']
        self.no_printer_connected = data['NoPrinterConnected']
        self.id = data['ID']
        self.customer_id = data['CustomerID']
        self.html = data['Html']
        self.filename = data['Filename']
        self.file_type = data['FileType']
        self.type = data['Type']
        self.status_id = data['StatusID']
        self.user_id = data['userId']
        self.order_id = data['OrderId']
        self.date_created = self.to_datetime(data['DateCreated'])
        self.trigger_id = data['TriggerId']
        self.check_next_at = self.to_datetime(data['CheckNextAt'])
        self.attempts = data['Attempts']
        if data['DateCompleted'] is not None:
            self.date_completed = self.to_datetime(data['DateCompleted'])
        else:
            self.date_completed = None
        self.customer_order_dispatch_id = data['CustomerOrderDispatchId']

    def to_datetime(self, date_time_string):
        """Convert Cloud Commerce date time string to datetime.datetime."""
        date_string, time_string = date_time_string.split('T')
        time_string = time_string.split('.')[0]
        year, month, day = date_string.split('-')
        hour, minute, second = time_string.split(':')
        return datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second))
