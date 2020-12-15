"""API Requests for Cloud Commerce Products."""

from .addproduct import AddProduct
from .deleteallproductfactorylink import DeleteAllProductFactoryLink
from .deleteimage import DeleteImage
from .deleteproductfactorylink import DeleteProductFactoryLink
from .dosearch import DoSearch
from .findproductfactorylinks import FindProductFactoryLinks
from .findproductselectedoptionsonly import FindProductSelectedOptionsOnly
from .productoperations import ProductOperations
from .savebarcode import SaveBarcode
from .savedescription import SaveDescription
from .savehandlingtime import SaveHandlingTime
from .saveproductname import SaveProductName
from .setimageorder import SetImageOrder
from .setproductoptionvalue import SetProductOptionValue
from .setproductscope import SetProductScope
from .setproducttype import SetProductType
from .updatecountryoforigin import UpdateCountryOfOrigin
from .updateonsaleschannel import UpdateProductOnSalesChannel
from .updateproductbaseprice import UpdateProductBasePrice
from .updateproductstocklevel import UpdateProductStockLevel
from .updateproductvatrate import UpdateProductVatRate
from .uploadimage import UploadImage

__all__ = [
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
    "UpdateCountryOfOrigin",
    "UpdateProductOnSalesChannel",
    "UpdateProductBasePrice",
    "UpdateProductStockLevel",
    "UpdateProductVatRate",
    "UploadImage",
]
