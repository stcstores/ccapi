"""Containers for product export data."""


import datetime


class ProductExportUpdateResponse:
    """Wrapper for GetProductExport responses."""

    PSEUDO_EXPORTS = "pseudoExports"
    PRODUCT_EXPORTS = "productExports"
    SUPPLIER_EXPORTS = "supplierExports"
    SUPPLIER_SKU_EXPORTS = "supplierSKUExports"
    MULTIPACK_EXPORTS = "multipackExports"
    CHANNEL_PRICES_EXPORTS = "channelPricesExports"

    def __init__(self, **kwargs):
        """Load properties from export data."""
        self.raw = kwargs
        self.pseudo_exports = PseudoExports(kwargs[self.PSEUDO_EXPORTS])
        self.product_exports = ProductExports(kwargs[self.PRODUCT_EXPORTS])
        self.supplier_exports = SupplierExports(kwargs[self.SUPPLIER_EXPORTS])
        self.supplier_SKU_exports = SupplierSKUExports(
            kwargs[self.SUPPLIER_SKU_EXPORTS]
        )
        self.multipack_exports = MultipackExports(kwargs[self.MULTIPACK_EXPORTS])
        self.channel_prices_exports = ChannelPricesExports(
            kwargs[self.CHANNEL_PRICES_EXPORTS]
        )


class BaseProductExport:
    """Wrapper for product exports."""

    ID = "ID"
    CHANNEL = "Channel"
    COPY_IMAGE = "CopyImages"
    PRODUCT_COUNT = "ProductCount"
    PRODUCTS_EXPORTED = "ProductsExported"
    STATUS = "Status"
    ERROR = "Error"
    FILE_NAME = "FileName"
    DATE_REQUESTED = "DateRequested"
    DATE_STARTED = "DateStarted"
    DATE_COMPLETED = "DateCompleted"
    SPREADSHEET = "spreadSheet"
    ZIP_FILE = "zipFile"

    def __init__(self, **kwargs):
        """Load properties from export data."""
        self.export_ID = kwargs[self.ID]
        self.channel = kwargs[self.CHANNEL]
        self.copy_image = kwargs[self.COPY_IMAGE]
        self.product_count = kwargs[self.PRODUCT_COUNT]
        self.products_exported = kwargs[self.PRODUCTS_EXPORTED]
        self.status = kwargs[self.STATUS]
        self.error = kwargs[self.ERROR]
        self.file_name = kwargs[self.FILE_NAME]
        self.date_requested = self.parse_date(kwargs[self.DATE_REQUESTED])
        self.date_started = self.parse_date(kwargs[self.DATE_STARTED])
        self.date_completed = self.parse_date(kwargs[self.DATE_COMPLETED])
        self.spreadsheet = ExportFile(**kwargs[self.SPREADSHEET])
        self.zip_file = ExportFile(**kwargs[self.ZIP_FILE])

    def __gt__(self, other):
        return self.date_completed > other.date_completed

    @staticmethod
    def parse_date(date_string):
        """Return datetime.datetime for date string in the format '04/10/2016 11:31'."""
        date, time = date_string.split(" ")
        day, month, year = date.split("/")
        hour, minute = time.split(":")
        return datetime.datetime(
            day=int(day),
            month=int(month),
            year=int(year),
            hour=int(hour),
            minute=int(minute),
        )


class PseudoExport(BaseProductExport):
    """Wrapper for pseudo exports."""

    def __repr__(self):
        return f"Pseudo Export '{self.file_name}'"


class ProductExport(BaseProductExport):
    """Wrapper for product exports."""

    def __repr__(self):
        return f"Product Export '{self.file_name}'"


class SupplierExport(BaseProductExport):
    """Wrapper for supplier exports."""

    def __repr__(self):
        return f"Supplier Export '{self.file_name}'"


class SupplierSKUExport(BaseProductExport):
    """Wrapper for supplier SKU exports."""

    def __repr__(self):
        return f"Supplier SKU Export '{self.file_name}'"


class MultipackExport(BaseProductExport):
    """Wrapper for mulitpack exports."""

    def __repr__(self):
        return f"Multipack Export '{self.file_name}'"


class ChannelPricesExport(BaseProductExport):
    """Wrapper for channel prices exports."""

    def __repr__(self):
        return f"Channel Prices Export '{self.file_name}'"


class BaseProductExports:
    """Container for product exports."""

    def __init__(self, exports):
        """Load with exports."""
        self.exports = sorted([self.export_class(**_) for _ in exports])

    def __iter__(self):
        for _ in self.exports:
            yield _

    def __getitem__(self, index):
        return self.exports[index]

    def __len__(self):
        return len(self.exports)


class PseudoExports(BaseProductExports):
    """Container for pseudo exports."""

    export_class = PseudoExport

    def __repr__(self):
        return f"{len(self.exports)} pseudo exports"


class ProductExports(BaseProductExports):
    """Container for product exports."""

    export_class = ProductExport

    def __repr__(self):
        return f"{len(self.exports)} product exports"


class SupplierExports(BaseProductExports):
    """Container for supplier exports."""

    export_class = SupplierExport

    class PseudoExports(BaseProductExports):
        """Container for pseudo exports."""

        export_class = PseudoExport

        def __repr__(self):
            return f"{len(self.exports)} supplier exports"


class SupplierSKUExports(BaseProductExports):
    """Container for supplier SKU exports."""

    export_class = SupplierSKUExport

    class PseudoExports(BaseProductExports):
        """Container for pseudo exports."""

        export_class = PseudoExport

        def __repr__(self):
            return f"{len(self.exports)} supplier SKU exports"


class MultipackExports(BaseProductExports):
    """Container for multipack exports."""

    export_class = MultipackExport

    class PseudoExports(BaseProductExports):
        """Container for pseudo exports."""

        export_class = PseudoExport

        def __repr__(self):
            return f"{len(self.exports)} multipack exports"


class ChannelPricesExports(BaseProductExports):
    """Container for channel prices exports."""

    export_class = ChannelPricesExport

    class PseudoExports(BaseProductExports):
        """Container for pseudo exports."""

        export_class = PseudoExport

        def __repr__(self):
            return f"{len(self.exports)} channel prices exports"


class ExportFile:
    """Wrapper for export file data."""

    COLUMNS = "cols"
    ROWS = "rows"
    ERROR = "error"
    FOUND = "found"
    SIZE = "size"

    def __init__(self, **kwargs):
        """Load properties from export data."""
        self.columns = kwargs[self.COLUMNS]
        self.rows = kwargs[self.ROWS]
        self.found = kwargs[self.FOUND]
        self.size = kwargs[self.SIZE]
