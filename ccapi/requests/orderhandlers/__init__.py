"""Order Handlers requests."""

from .getdispatchmethodsfororder import GetDispatchMethodsForOrder
from .getordersfordispatch import GetOrdersForDispatch
from .getrecentordersbycustomerid import GetRecentOrdersByCustomerID

__all__ = [
    "GetOrdersForDispatch",
    "GetDispatchMethodsForOrder",
    "GetRecentOrdersByCustomerID",
]
