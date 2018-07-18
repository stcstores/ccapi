"""
setOptionSelect request.

Set weather a Product Option is a drop down for a Product Range.
"""

from ..apirequest import APIRequest


class SetOptionSelect(APIRequest):
    """setOptionSelect request."""

    uri = 'Handlers/Range/setOptionSelect.ashx'

    def __new__(self, *, range_id, option_id, drop_down):
        """Create setOptionSelect request.

        Args:
            range_id: ID of Product Range.
            option_id: ID of Product Option.
            drop_down: (Bool) Product Option is a drop down.
        """
        self.range_id = range_id
        self.option_id = option_id
        self.drop_down = bool(drop_down)
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'prdid': self.range_id,
            'optid': self.option_id,
            'onoff': int(self.value),
        }
        return data

    def process_response(self, response):
        """Handle request response."""
        pass
