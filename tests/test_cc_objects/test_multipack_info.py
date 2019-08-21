"""Tests for the ccapi.cc_objects.MultipackInfo class."""

from decimal import Decimal

from ccapi import cc_objects

from .test_cc_objects import TestCCObjects


class TestMultipackInfo(TestCCObjects):

    RESPONSE = [
        {
            "CanEdit": True,
            "type": 0,
            "percent": 77,
            "links": "12174169",
            "quantity": 2,
            "names": ["Test Multipack  - Single"],
            "prices": ["5.00"],
            "StatusID": 1,
        },
        {
            "CanEdit": True,
            "type": 0,
            "percent": 23,
            "links": "3752158",
            "quantity": 3,
            "names": ["10 Birth Announcements 20 Thank Yous and 20 Envelope "],
            "prices": ["1.00"],
            "StatusID": 1,
        },
    ]
    PRODUCT_ID = "138761531"

    def test_multipack_info(self):
        items = [
            cc_objects.MultipackItem(
                product_id=_["links"], quantity=_["quantity"], price=_["prices"][0]
            )
            for _ in self.RESPONSE
        ]
        info = cc_objects.MultipackInfo(self.PRODUCT_ID, *items)
        self.assertIsInstance(info, cc_objects.MultipackInfo)
        self.assertEqual(info.product_id, self.PRODUCT_ID)
        self.assertEqual(len(info), 2)
        self.assertEqual(info.price, Decimal(13.00))

        self.assertIsInstance(info[0], cc_objects.MultipackItem)
        self.assertEqual(info[0].multipack_info, info)
        self.assertEqual(info[0].product_id, "12174169")
        self.assertEqual(info[0].quantity, 2)
        self.assertEqual(info[0].percent, 77)
        self.assertEqual(info[0].price, Decimal("5.00"))

        self.assertIsInstance(info[1], cc_objects.MultipackItem)
        self.assertEqual(info[1].multipack_info, info)
        self.assertEqual(info[1].product_id, "3752158")
        self.assertEqual(info[1].quantity, 3)
        self.assertEqual(info[1].percent, 23)
        self.assertEqual(info[1].price, Decimal("1.00"))

        for item in info:
            self.assertIsInstance(item, cc_objects.MultipackItem)

    def test_MultipackInfo_load_json(self):
        info = cc_objects.MultipackInfo.load_json(self.PRODUCT_ID, self.RESPONSE)
        self.assertIsInstance(info, cc_objects.MultipackInfo)
        self.assertEqual(len(info), 2)
        self.assertEqual(info.price, Decimal(13.00))

        self.assertIsInstance(info[0], cc_objects.MultipackItem)
        self.assertEqual(info[0].multipack_info, info)
        self.assertEqual(info[0].product_id, "12174169")
        self.assertEqual(info[0].quantity, 2)
        self.assertEqual(info[0].percent, 77)
        self.assertEqual(info[0].price, Decimal("5.00"))

        self.assertIsInstance(info[1], cc_objects.MultipackItem)
        self.assertEqual(info[1].multipack_info, info)
        self.assertEqual(info[1].product_id, "3752158")
        self.assertEqual(info[1].quantity, 3)
        self.assertEqual(info[1].percent, 23)
        self.assertEqual(info[1].price, Decimal("1.00"))
