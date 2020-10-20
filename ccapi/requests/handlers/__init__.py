"""Requests with no directory."""

from .addcustomer import AddCustomer
from .commondatasource import CommonDataSource
from .createorder import CreateOrder
from .customeraccounts import CustomerAccounts
from .deleterequest import DeleteRequest
from .getimages import GetImages
from .getproductsforrange import GetProductsForRange
from .preemployee import PreEmployee

__all__ = [
    "AddCustomer",
    "CommonDataSource",
    "CreateOrder",
    "CustomerAccounts",
    "DeleteRequest",
    "GetImages",
    "GetProductsForRange",
    "PreEmployee",
]
