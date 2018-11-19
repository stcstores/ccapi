"""Tests for the ccapi.cc_objects.productexport module."""

import datetime

from ccapi import cc_objects

from .. import test_data
from .test_cc_objects import TestCCObjects


class TestProductExport(TestCCObjects):
    """Base test class for Product Export objects."""

    EXPORT_DATA = test_data.GET_PRODUCT_EXPORT_UPDATE_RESPONSE


class TestProductExportUpdateResponse(TestProductExport):
    """Tests for the cc_api.cc_objects.productexport.ProductExportUpdateResponse class."""

    def setUp(self):
        """Get exports."""
        super().setUp()
        self.exports = cc_objects.ProductExportUpdateResponse(**self.EXPORT_DATA)

    def test_raw(self):
        """Test the ProductExportUpdateResponse raw attribute."""
        self.assertEqual(self.exports.raw, self.EXPORT_DATA)

    def test_export_types(self):
        """Test each export type exists as an attribute."""
        self.assertIsInstance(
            self.exports.pseudo_exports, cc_objects.productexport.PseudoExports
        )
        self.assertIsInstance(
            self.exports.product_exports, cc_objects.productexport.ProductExports
        )
        self.assertIsInstance(
            self.exports.supplier_exports, cc_objects.productexport.SupplierExports
        )
        self.assertIsInstance(
            self.exports.supplier_SKU_exports,
            cc_objects.productexport.SupplierSKUExports,
        )
        self.assertIsInstance(
            self.exports.multipack_exports, cc_objects.productexport.MultipackExports
        )
        self.assertIsInstance(
            self.exports.channel_prices_exports,
            cc_objects.productexport.ChannelPricesExports,
        )


class TestBaseProductExport(TestProductExport):
    """Tests for ccapi.cc_objects.productexport.BaseProductExport."""

    EXPORT_DATA = {
        "ID": 3056,
        "Channel": "Not Selected",
        "CopyImages": False,
        "ProductCount": 31,
        "ProductsExported": 31,
        "Status": "Complete",
        "Error": "",
        "FileName": "ProductsExport_636111775182718600",
        "DateRequested": "04/10/2016 11:31",
        "DateStarted": "04/10/2016 11:31",
        "DateCompleted": "04/10/2016 11:31",
        "spreadSheet": {
            "found": True,
            "size": "11Kb",
            "rows": "0",
            "cols": "0",
            "error": "",
        },
        "zipFile": {
            "found": False,
            "size": "???",
            "rows": "???",
            "cols": "???",
            "error": "",
        },
    }

    def setUp(self):
        """Get export."""
        super().setUp()
        self.export = cc_objects.productexport.BaseProductExport(**self.EXPORT_DATA)

    def test_parse_date_returns_correct_date(self):
        """Test the parse_date method returns the correct datetime.datetime object."""
        test_date = datetime.datetime(day=4, month=10, year=2018, hour=11, minute=31)
        self.assertEqual(
            test_date,
            cc_objects.productexport.BaseProductExport.parse_date("04/10/2018 11:31"),
        )

    def test_export_ID(self):
        """Test BaseProductID's export_ID attribute."""
        self.assertEqual(self.export.export_ID, self.EXPORT_DATA[self.export.ID])

    def test_channel(self):
        """Test BaseProductID's channel attribute."""
        self.assertEqual(self.export.channel, self.EXPORT_DATA[self.export.CHANNEL])

    def test_copy_image(self):
        """Test BaseProductID's copy_images attribute."""
        self.assertEqual(
            self.export.copy_image, self.EXPORT_DATA[self.export.COPY_IMAGE]
        )

    def test_product_count(self):
        """Test BaseProductID's product_count attribute."""
        self.assertEqual(
            self.export.product_count, self.EXPORT_DATA[self.export.PRODUCT_COUNT]
        )

    def test_products_exported(self):
        """Test BaseProductID's products_exported attribute."""
        self.assertEqual(
            self.export.products_exported,
            self.EXPORT_DATA[self.export.PRODUCTS_EXPORTED],
        )

    def test_status(self):
        """Test BaseProductID's status attribute."""
        self.assertEqual(self.export.status, self.EXPORT_DATA[self.export.STATUS])

    def test_error(self):
        """Test BaseProductID's error attribute."""
        self.assertEqual(self.export.error, self.EXPORT_DATA[self.export.ERROR])

    def test_file_name(self):
        """Test BaseProductID's file_name attribute."""
        self.assertEqual(self.export.file_name, self.EXPORT_DATA[self.export.FILE_NAME])

    def test_date_requested(self):
        """Test BaseProductID's date_requested attribute."""
        expected_date = cc_objects.productexport.BaseProductExport.parse_date(
            self.EXPORT_DATA[self.export.DATE_REQUESTED]
        )
        self.assertEqual(self.export.date_requested, expected_date)

    def test_date_started(self):
        """Test BaseProductID's date_started attribute."""
        expected_date = cc_objects.productexport.BaseProductExport.parse_date(
            self.EXPORT_DATA[self.export.DATE_STARTED]
        )
        self.assertEqual(self.export.date_started, expected_date)

    def test_date_completed(self):
        """Test BaseProductID's date_completed attribute."""
        expected_date = cc_objects.productexport.BaseProductExport.parse_date(
            self.EXPORT_DATA[self.export.DATE_COMPLETED]
        )
        self.assertEqual(self.export.date_completed, expected_date)

    def test_spreadsheet(self):
        """Test BaseProductID's spreadsheet attribute."""
        self.assertIsInstance(
            self.export.spreadsheet, cc_objects.productexport.ExportFile
        )

    def test_zip_file(self):
        """Test BaseProductID's zip_file attribute."""
        self.assertIsInstance(self.export.zip_file, cc_objects.productexport.ExportFile)

    def test_sorting(self):
        """Test exports sort by date_requested."""
        early_update = cc_objects.productexport.BaseProductExport(**self.EXPORT_DATA)
        late_update = cc_objects.productexport.BaseProductExport(**self.EXPORT_DATA)
        early_update.date_requested = datetime.datetime(year=2016, day=1, month=1)
        late_update.date_requested = datetime.datetime(year=2018, day=1, month=1)
        exports = sorted([late_update, early_update])
        self.assertEqual(exports[0], early_update)
        self.assertEqual(exports[1], late_update)

    def test_status_properties(self):
        """Test export status properties."""
        self.export.status = self.export.COMPLETE
        self.assertTrue(self.export.complete)
        self.export.status = self.export.RUNNING
        self.assertTrue(self.export.running)
        self.export.status = self.export.FAILED
        self.assertTrue(self.export.failed)

    def test_null_date_started(self):
        """Test export.date_started is None if it is a null value in the export data."""
        export_class = cc_objects.productexport.BaseProductExport
        export_data = dict(self.EXPORT_DATA)
        export_data[export_class.DATE_STARTED] = export_class.NULL_VALUE
        export = cc_objects.productexport.BaseProductExport(**export_data)
        self.assertIsNone(export.date_started)

    def test_null_date_completed(self):
        """Test export.date_started is None if it is a null value in the export data."""
        export_class = cc_objects.productexport.BaseProductExport
        export_data = dict(self.EXPORT_DATA)
        export_data[export_class.DATE_COMPLETED] = export_class.NULL_VALUE
        export = cc_objects.productexport.BaseProductExport(**export_data)
        self.assertIsNone(export.date_completed)


class TestProductExports(TestProductExport):
    """Tests for cc_objects.productexport.BaseProductExports and it's sublcasses."""

    def setUp(self):
        """Get exports."""
        super().setUp()
        self.export_data = self.EXPORT_DATA[
            cc_objects.ProductExportUpdateResponse.PRODUCT_EXPORTS
        ]
        self.exports = cc_objects.productexport.ProductExports(self.export_data)

    def test_exports_has_exports(self):
        """Test the BaseProductsExports instance has exports."""
        self.assertIsInstance(self.exports.exports, list)
        self.assertIsInstance(
            self.exports.exports[0], cc_objects.productexport.ProductExport
        )

    def test_null_date_completed(self):
        """Test export can be instanciated when no date completed is provided."""
        export_data = {
            "ID": 3056,
            "Channel": "Not Selected",
            "CopyImages": False,
            "ProductCount": 31,
            "ProductsExported": 31,
            "Status": "Complete",
            "Error": "",
            "FileName": "ProductsExport_636111775182718600",
            "DateRequested": "04/10/2016 11:31",
            "DateStarted": "04/10/2016 11:31",
            "DateCompleted": "???",
            "spreadSheet": {
                "found": True,
                "size": "11Kb",
                "rows": "0",
                "cols": "0",
                "error": "",
            },
            "zipFile": {
                "found": False,
                "size": "???",
                "rows": "???",
                "cols": "???",
                "error": "",
            },
        }

        export = cc_objects.productexport.ProductExport(**export_data)
        self.assertIsNone(export.date_completed)

    def test_get_by_ID(self):
        """Test the get_by_ID method."""
        export_ID = 3056
        export = self.exports.get_by_ID(export_ID)
        self.assertIsInstance(export, cc_objects.productexport.ProductExport)
        self.assertEqual(export.export_ID, export_ID)
