from unittest import TestCase

from enum_properties import IntEnumProperties, p, s


class TestTypeHints(TestCase):
    def test_type_hints(self):
        from typing import get_type_hints

        class MyEnum(IntEnumProperties, s("label"), p("idx")):
            label: str
            idx: int

            ITEM1 = 1, "item1", 0
            ITEM2 = 2, "item2", 1
            ITEM3 = 3, "item3", 2

        self.assertEqual(MyEnum.ITEM1, 1)
        self.assertEqual(MyEnum.ITEM1.value, 1)
        self.assertEqual(MyEnum.ITEM1.label, "item1")
        self.assertEqual(MyEnum.ITEM1.idx, 0)
        self.assertEqual(get_type_hints(MyEnum.ITEM1), {"label": str, "idx": int})

        self.assertEqual(MyEnum.ITEM2, 2)
        self.assertEqual(MyEnum.ITEM2.value, 2)
        self.assertEqual(MyEnum.ITEM2.label, "item2")
        self.assertEqual(MyEnum.ITEM2.idx, 1)
        self.assertEqual(get_type_hints(MyEnum.ITEM2), {"label": str, "idx": int})

        self.assertEqual(MyEnum.ITEM3, 3)
        self.assertEqual(MyEnum.ITEM3.value, 3)
        self.assertEqual(MyEnum.ITEM3.label, "item3")
        self.assertEqual(MyEnum.ITEM3.idx, 2)
        self.assertEqual(get_type_hints(MyEnum.ITEM3), {"label": str, "idx": int})
