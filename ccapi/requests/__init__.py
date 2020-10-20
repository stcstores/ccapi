"""This module contains classes for Cloud Commerce API requests."""

from .accounts import CreatePayment
from .apirequest import APIRequest
from .ccapisession import CloudCommerceAPISession
from .configuration import ShippingRules
from .customers import GetLogs
from .exports import GetProductExportUpdate, RequestProductExport, ViewFile
from .factory import Factory, FindFactories, UpdProductFactoryLink
from .handlers import (
    AddCustomer,
    CommonDataSource,
    CreateOrder,
    CustomerAccounts,
    DeleteRequest,
    GetImages,
    GetProductsForRange,
    PreEmployee,
)
from .orderdetails import GetOrderAddresses
from .orderhandlers import GetDispatchMethodsForOrder, GetOrdersForDispatch
from .printqueue import FindPrintQueue
from .productbarcode import ProductBarcodeInUse
from .productmanager import GetProducts
from .productoption import (
    AddOptionValue,
    DeleteOptionValue,
    GetOptionData,
    GetOptions,
    GetProductData,
)
from .products import (
    AddProduct,
    DeleteAllProductFactoryLink,
    DeleteImage,
    DeleteProductFactoryLink,
    DoSearch,
    FindProductFactoryLinks,
    FindProductSelectedOptionsOnly,
    ProductOperations,
    SaveBarcode,
    SaveDescription,
    SaveHandlingTime,
    SaveProductName,
    SetImageOrder,
    SetProductOptionValue,
    SetProductScope,
    SetProductType,
    UpdateProductBasePrice,
    UpdateProductOnSalesChannel,
    UpdateProductStockLevel,
    UpdateProductVatRate,
    UploadImage,
)
from .program_type_requests import (
    Customer,
    GetPaymentTerms,
    GetSimplePackage,
    SaveSimplePackage,
    UpdateCustomerAddress,
)
from .range import (
    AddNewRange,
    AddRemProductOption,
    CheckRangesOnSalesChannel,
    DeleteProductRange,
    SetOptionSelect,
    UpdateRangeOnSalesChannel,
    UpdateRangeSettings,
)
from .warehouse import FindWarehouse
from .warehousebay import FindWarehouseBay, SaveWarehouseBay

__all__ = [
    "CloudCommerceAPISession",
    "APIRequest",
    "CreatePayment",
    "ShippingRules",
    "GetLogs",
    "GetProductExportUpdate",
    "RequestProductExport",
    "ViewFile" "FindFactories",
    "Factory",
    "UpdProductFactoryLink",
    "CommonDataSource",
    "AddCustomer",
    "CreateOrder",
    "CustomerAccounts",
    "DeleteRequest",
    "GetImages",
    "GetProductsForRange",
    "PreEmployee",
    "GetOrderAddresses",
    "GetOrdersForDispatch",
    "GetDispatchMethodsForOrder",
    "FindPrintQueue",
    "ProductBarcodeInUse",
    "GetProducts",
    "AddOptionValue",
    "DeleteOptionValue",
    "GetOptionData",
    "GetOptions",
    "GetProductData",
    "AddProduct",
    "DeleteAllProductFactoryLink",
    "DeleteImage",
    "DeleteProductFactoryLink",
    "DoSearch",
    "FindProductFactoryLinks",
    "FindProductSelectedOptionsOnly",
    "ProductOperations",
    "SaveBarcode",
    "SaveDescription",
    "SaveHandlingTime",
    "SaveProductName",
    "SetImageOrder",
    "SetProductOptionValue",
    "SetProductScope",
    "SetProductType",
    "UpdateProductOnSalesChannel",
    "UpdateProductBasePrice",
    "UpdateProductStockLevel",
    "UpdateProductVatRate",
    "UploadImage",
    "GetPaymentTerms",
    "Customer",
    "UpdateCustomerAddress",
    "SaveSimplePackage",
    "GetSimplePackage",
    "AddNewRange",
    "AddRemProductOption",
    "DeleteProductRange",
    "CheckRangesOnSalesChannel",
    "SetOptionSelect",
    "UpdateRangeOnSalesChannel",
    "UpdateRangeSettings",
    "FindWarehouse",
    "FindWarehouseBay",
    "SaveWarehouseBay",
    "GetProductExportUpdate",
    "RequestProductExport",
    "ViewFile",
    "FindFactories",
    "Factory",
    "UpdProductFactoryLink",
]
