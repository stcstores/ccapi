"""
updateRangeSettings request.

Update Name, SKU, End of Line, Pre Order and Group Items for Product Range.
"""

import json

from .. apirequest import APIRequest


class UpdateRangeSettings(APIRequest):
    """updateRangeSettings request."""

    uri = '/Handlers/Range/updateRangeSettings.ashx'

    def __new__(
            self, range_id, current_name='', current_sku='',
            current_end_of_line='', current_pre_order='',
            current_group_items='', new_name='', new_sku='',
            new_end_of_line='', new_pre_order='', new_group_items='',
            channels=[]):
        """Create updateRangeSettings request.

        Args:
            range_id: ID of range.

        Kwargs:
            current_name: Current name of Range.
            current_sku: Current SKU of Range.
            current_end_of_line: Range is currently end of line.
            current_pre_order: Range is currently pre order.
            current_group_items: Range is currently set to group items.
            new_name: Updated name of Range.
            new_sku: Updated SKU of Range.
            new_end_of_line: New state of Range End Of Line.
            new_pre_order: New state of Range Pre Order.
            new_group_items: New state of Range Group Items.
            channels: Channel IDs to update.
        """
        self.range_id = range_id
        self.current_name = current_name
        self.current_sku = current_sku
        self.current_end_of_line = current_end_of_line
        self.current_pre_order = current_pre_order
        self.current_group_items = current_group_items
        self.new_name = new_name
        self.new_sku = new_sku
        self.new_end_of_line = new_end_of_line
        self.new_pre_order = new_pre_order
        self.new_group_items = new_group_items
        self.channels = channels
        return super().__new__(self)

    def get_data(self):
        """Get data for request."""
        data = {
            'brandID': 341,
            'rangeID': str(self.range_id),
            'currName': str(self.current_name),
            'currSKU': str(self.current_sku),
            'currEoL': int(self.current_end_of_line),
            'currPreO': int(self.current_pre_order),
            'currGBy': str(int(self.current_pre_order)),
            'newName': str(self.new_name),
            'newSKU': str(self.new_sku),
            'newEoL': str(int(self.new_end_of_line)),
            'newPreO': str(int(self.new_pre_order)),
            'newGBy': str(int(self.new_group_items)),
            'channels': ','.join(
                [str(channel_id) for channel_id in self.channels])
            }
        return json.dumps(data)

    def process_response(self, response):
        """Handle request response."""
        response.raise_for_status()
        return response.text
