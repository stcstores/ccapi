"""Requests using the program type form."""

from .customer import Customer, GetPaymentTerms, UpdateCustomerAddress
from .getsimpleproductpackage import GetSimplePackage, SaveSimplePackage

__all__ = [
    "Customer",
    "GetPaymentTerms",
    "UpdateCustomerAddress",
    "SaveSimplePackage",
    "GetSimplePackage",
]
