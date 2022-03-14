"""
StockControlCheck request.

Creates a stock control report for a product range.
"""

import datetime as dt

from bs4 import BeautifulSoup

from ..apirequest import APIRequest


class StockControlCheck(APIRequest):
    """AddNewRange request."""

    uri = "Handlers/Reports/StockControlCheck.ashx"

    def __new__(self, *, range_id):
        """Create StockControlCheck request.

        Args:
            range_id: ID of the product range to stock control check

        """
        self.range_id = range_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        self.raise_for_non_200(
            self, response, f'Error creating stock control check "{self.range_id}"'
        )
        try:
            return _StockControlReport(response.text)
        except Exception:
            from pathlib import Path

            with open(Path.home() / "Desktop/report.txt", "w") as f:
                f.write(response.text)
            raise

    def get_data(self):
        """Get data for request."""
        return {
            "ProgType": "ViewReport",
            "Option": self.range_id,
        }

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "1496918496099"}


class _StockControlReportEntry:
    def __init__(self, html):
        self.html = html
        rows = self.html.find_all("div")
        column_values = [self._parse_row(row) for row in rows]
        self.title = column_values[0]
        self.sku = column_values[1]
        self.reason = column_values[2]
        self.date = self._parse_date(column_values[3])
        self.quantity = int(column_values[4])
        self.dispatched = int(column_values[5])
        self.order_number = (
            int(column_values[6]) if int(column_values[6]) != 0 else None
        )
        self.user = column_values[8]

    def _parse_row(self, html):
        font_tag = html.find("font")
        if font_tag:
            return font_tag.text.strip()
        return html.text.strip()

    def _parse_date(self, date_string):
        day, month, year = date_string.split("/")
        return dt.datetime(day=int(day), month=int(month), year=int(year))


class _StockControlReport:
    def __init__(self, report_html):
        self.report_html = report_html
        soup = BeautifulSoup(self.report_html, features="html.parser")
        report_table = soup.find_all("div", {"class": "reportRowWrapper"})[-1]
        if report_table.find_all("div")[0].string == "No Stock Records Found":
            self.rows = []
        else:
            self.rows = [_StockControlReportEntry(row) for row in report_table]
            self.rows.sort(key=lambda x: x.date, reverse=True)

    def __iter__(self):
        for row in self.rows:
            yield row

    def __len__(self):
        return len(self.rows)
