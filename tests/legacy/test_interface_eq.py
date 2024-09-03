from enum import Enum, IntEnum
from unittest import TestCase

from enum_properties import (
    IntEnumProperties,
    IntFlagProperties,
    StrEnumProperties,
)


class TestInterfaceEquivalency(TestCase):
    """
    Enums should hash the same as their values.
    """

    def test_operators(self):
        class MyIntEnum(Enum):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertNotEqual(MyIntEnum.ONE, 1)

        class MyIntEnum(IntEnum):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertTrue(MyIntEnum.ONE == 1)
        self.assertTrue(MyIntEnum.ONE != 2)

        self.assertTrue(1 == MyIntEnum.ONE)
        self.assertTrue(2 != MyIntEnum.ONE)

        self.assertTrue(MyIntEnum.ONE < 2)
        self.assertTrue(2 < MyIntEnum.THREE)
        self.assertTrue(MyIntEnum.ONE < 2)
        self.assertTrue(2 < MyIntEnum.THREE)
        self.assertTrue(MyIntEnum.TWO <= 2)
        self.assertTrue(2 <= MyIntEnum.TWO)

        self.assertTrue(MyIntEnum.TWO > 1)
        self.assertTrue(3 > MyIntEnum.TWO)
        self.assertTrue(MyIntEnum.TWO > 1)
        self.assertTrue(2 > MyIntEnum.ONE)
        self.assertTrue(MyIntEnum.THREE >= 2)
        self.assertTrue(3 >= MyIntEnum.TWO)

        self.assertTrue(MyIntEnum.TWO % 2 == 0)
        self.assertTrue(MyIntEnum.TWO % 3 == 2)

        class MyIntEnum(IntEnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertTrue(MyIntEnum.ONE == 1)
        self.assertTrue(MyIntEnum.ONE != 2)

        self.assertTrue(1 == MyIntEnum.ONE)
        self.assertTrue(2 != MyIntEnum.ONE)

        self.assertTrue(MyIntEnum.ONE < 2)
        self.assertTrue(2 < MyIntEnum.THREE)
        self.assertTrue(MyIntEnum.ONE < 2)
        self.assertTrue(2 < MyIntEnum.THREE)
        self.assertTrue(MyIntEnum.TWO <= 2)
        self.assertTrue(2 <= MyIntEnum.TWO)

        self.assertTrue(MyIntEnum.TWO > 1)
        self.assertTrue(3 > MyIntEnum.TWO)
        self.assertTrue(MyIntEnum.TWO > 1)
        self.assertTrue(2 > MyIntEnum.ONE)
        self.assertTrue(MyIntEnum.THREE >= 2)
        self.assertTrue(3 >= MyIntEnum.TWO)

        self.assertTrue(MyIntEnum.TWO % 2 == 0)
        self.assertTrue(MyIntEnum.TWO % 3 == 2)

    def test_hashing_issue_53(self):
        class MyIntEnum(IntEnum):
            ONE = 1
            TWO = 2
            THREE = 3

        class MyStrEnum(str, Enum):
            A = "a"
            B = "b"
            C = "c"

        # self.assertEqual(hash(MyIntEnum.ONE), hash(1))
        # self.assertEqual(hash(MyStrEnum.C), hash('c'))

        test_dict = {1: "One", 2: "Two", MyIntEnum.THREE: "Three"}

        self.assertIn(MyIntEnum.ONE, test_dict)
        self.assertEqual(test_dict[MyIntEnum.ONE], "One")
        self.assertIn(3, test_dict)

        test_dict = {"a": "A", "b": "B", MyStrEnum.C: "C"}

        self.assertIn(MyStrEnum.B, test_dict)
        self.assertEqual(test_dict[MyStrEnum.A], "A")
        self.assertIn("c", test_dict)

        self.assertIn(MyIntEnum.ONE, {1, 2, 3})
        self.assertIn(MyStrEnum.A, {"a", "b", "c"})
        self.assertIn(1, {MyIntEnum.ONE, MyIntEnum.TWO, MyIntEnum.THREE})
        self.assertIn(3, {MyIntEnum.ONE, MyIntEnum.TWO, MyIntEnum.THREE})
        self.assertIn("a", {MyStrEnum.A, MyStrEnum.B, MyStrEnum.C})

        class MyIntEnum(IntEnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

        class MyStrEnum(StrEnumProperties):
            A = "a"
            B = "b"
            C = "c"

        test_dict = {1: "One", 2: "Two", MyIntEnum.THREE: "Three"}

        self.assertIn(MyIntEnum.ONE, test_dict)
        self.assertEqual(test_dict[MyIntEnum.ONE], "One")
        self.assertIn(3, test_dict)

        test_dict = {"a": "A", "b": "B", MyStrEnum.C: "C"}

        self.assertIn(MyStrEnum.B, test_dict)
        self.assertEqual(test_dict[MyStrEnum.A], "A")
        self.assertIn("c", test_dict)

        self.assertIn(MyIntEnum.ONE, {1, 2, 3})
        self.assertIn(MyStrEnum.A, {"a", "b", "c"})
        self.assertIn(1, {MyIntEnum.ONE, MyIntEnum.TWO, MyIntEnum.THREE})
        self.assertIn(3, {MyIntEnum.ONE, MyIntEnum.TWO, MyIntEnum.THREE})
        self.assertIn("a", {MyStrEnum.A, MyStrEnum.B, MyStrEnum.C})

        class MyIntFlagEnum(IntFlagProperties):
            ONE = 1
            TWO = 2
            THREE = 4

        test_dict = {1: "One", 2: "Two", MyIntFlagEnum.THREE: "Three"}

        self.assertIn(MyIntFlagEnum.ONE, test_dict)
        self.assertEqual(test_dict[MyIntFlagEnum.ONE], "One")
        self.assertIn(4, test_dict)

    def test_hashing_example(self):
        from enum import Enum

        from enum_properties import EnumPropertiesMeta, SymmetricMixin, s

        class Color(
            SymmetricMixin,
            tuple,
            Enum,
            s("hex", case_fold=True),
            metaclass=EnumPropertiesMeta,
        ):
            # name   value      rgb       hex
            RED = (1, 0, 0), "0xff0000"
            GREEN = (0, 1, 0), "0x00ff00"
            BLUE = (0, 0, 1), "0x0000ff"

            def __hash__(self):
                return tuple.__hash__(self)

        assert {(1, 0, 0): "Found me!"}[Color.RED] == "Found me!"
