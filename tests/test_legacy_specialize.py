import enum
import sys
from unittest import TestCase

from enum_properties import (
    EnumProperties,
    s,
    specialize,
)


class TestSpecialize(TestCase):
    """
    Test the specialize decorator
    """

    def test_specialize(self):
        class SpecializedEnum(EnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

            @specialize(ONE)
            def method(self):
                return "method_one()"

            @specialize(TWO)
            def method(self):
                return "method_two()"

            @specialize(THREE)
            def method(self):
                return "method_three()"

        self.assertEqual(SpecializedEnum.ONE.method(), "method_one()")
        self.assertEqual(SpecializedEnum.TWO.method(), "method_two()")
        self.assertEqual(SpecializedEnum.THREE.method(), "method_three()")

    def test_specialize_default(self):
        class SpecializedEnum(EnumProperties, s("label")):
            ONE = 1, "one"
            TWO = 2, "two"
            THREE = 3, "three"

            def test(self):
                return "test_default()"

            @specialize(THREE)
            def test(self):
                return "test_three()"

        self.assertEqual(SpecializedEnum.ONE.test(), "test_default()")
        self.assertEqual(SpecializedEnum.TWO.test(), "test_default()")
        self.assertEqual(SpecializedEnum.THREE.test(), "test_three()")
        self.assertEqual(SpecializedEnum("three").test(), "test_three()")

    def test_specialize_no_default(self):
        class SpecializedEnum(EnumProperties, s("label")):
            ONE = 1, "one"
            TWO = 2, "two"
            THREE = 3, "three"

            @specialize(TWO)
            def test(self):
                return "test_two()"

            @specialize(THREE)
            def test(self):
                return "test_three()"

        self.assertFalse(hasattr(SpecializedEnum.ONE, "test"))
        self.assertFalse(hasattr(SpecializedEnum("one"), "test"))
        self.assertEqual(SpecializedEnum.TWO.test(), "test_two()")
        self.assertEqual(SpecializedEnum["TWO"].test(), "test_two()")
        self.assertEqual(SpecializedEnum.THREE.test(), "test_three()")

    def test_specialize_class_method(self):
        class SpecializedEnum(EnumProperties, s("label")):
            ONE = 1, "one"
            TWO = 2, "two"
            THREE = 3, "three"

            @specialize(ONE)
            @classmethod
            def test(cls):
                return (1, cls)

            @specialize(TWO)
            @classmethod
            def test(cls):
                return (2, cls)

            @specialize(THREE)
            @classmethod
            def test(cls):
                return (3, cls)

        self.assertEqual(SpecializedEnum.ONE.test(), (1, SpecializedEnum))
        self.assertEqual(SpecializedEnum.TWO.test(), (2, SpecializedEnum))
        self.assertEqual(SpecializedEnum.THREE.test(), (3, SpecializedEnum))
        self.assertEqual(SpecializedEnum("two").test(), (2, SpecializedEnum))

    def test_specialize_static_method(self):
        class SpecializedEnum(EnumProperties, s("label")):
            ONE = 1, "one"
            TWO = 2, "two"
            THREE = 3, "three"

            @specialize(ONE)
            @staticmethod
            def test():
                return "test_one()"

            @specialize(TWO)
            @staticmethod
            def test():
                return "test_two()"

            @specialize(THREE)
            @staticmethod
            def test():
                return "test_three()"

        self.assertEqual(SpecializedEnum.ONE.test(), "test_one()")
        self.assertEqual(SpecializedEnum.TWO.test(), "test_two()")
        self.assertEqual(SpecializedEnum.THREE.test(), "test_three()")
        self.assertEqual(SpecializedEnum("two").test(), "test_two()")

    def test_specialize_arguments(self):
        class SpecializedEnum(EnumProperties, s("label")):
            ONE = 1, "one"
            TWO = 2, "two"
            THREE = 3, "three"

            @specialize(ONE)
            def test(self, count=1):
                return self.label * count

            @specialize(TWO)
            def test(self, count=2):
                return self.label * count

            @specialize(THREE)
            def test(self, count=3):
                return self.label * count

        self.assertEqual(SpecializedEnum.ONE.test(), "one")
        self.assertEqual(SpecializedEnum.TWO.test(), "twotwo")
        self.assertEqual(SpecializedEnum.THREE.test(), "threethreethree")
        self.assertEqual(SpecializedEnum("two").test(count=1), "two")

    def test_specialize_multiple_lists(self):
        class SpecializedEnum(EnumProperties, s("label")):
            ONE = 1, "one"
            TWO = 2, "two"
            THREE = 3, "three"

            @specialize(ONE)
            def test(self, count=1):
                return self.label * count

            @specialize(TWO, THREE)
            def test(self, count=2):
                return self.label * count

        self.assertEqual(SpecializedEnum.ONE.test(), "one")
        self.assertEqual(SpecializedEnum.TWO.test(), "twotwo")
        self.assertEqual(SpecializedEnum.THREE.test(), "threethree")
