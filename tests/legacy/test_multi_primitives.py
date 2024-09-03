from unittest import TestCase

from enum_properties import EnumProperties


class TestMultiPrimitives(TestCase):
    def test_multiple_primitive_types(self):
        from datetime import date

        class MyEnum(EnumProperties):
            V1 = None
            V2 = 5
            V3 = "label"
            V4 = date(year=1970, month=1, day=1)

        self.assertEqual(MyEnum.V1, None)
        self.assertEqual(MyEnum.V2, 5)
        self.assertEqual(MyEnum.V3, "label")
        self.assertEqual(MyEnum.V4, date(year=1970, month=1, day=1))
