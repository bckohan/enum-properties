import sys
import typing as t
from unittest import TestCase
from typing_extensions import Annotated

from enum_properties import (
    EnumProperties,
    IntEnumProperties,
    Symmetric,
    specialize,
)


class TestSpecialize(TestCase):
    """
    Test the specialize decorator
    """

    def test_specialize_default(self):
        class SpecializedEnum(EnumProperties):
            label: Annotated[str, Symmetric()]

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
        class SpecializedEnum(EnumProperties):
            label: Annotated[str, Symmetric()]

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
        class SpecializedEnum(EnumProperties):
            label: Annotated[str, Symmetric()]

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
        class SpecializedEnum(EnumProperties):
            label: Annotated[str, Symmetric()]

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
        class SpecializedEnum(EnumProperties):
            label: Annotated[str, Symmetric()]

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
        class SpecializedEnum(EnumProperties):
            label: Annotated[str, Symmetric()]

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


class NoneCoercionTests(TestCase):
    def test_string_to_none_coercion_disabled(self):
        class EnumWithNones(EnumProperties):
            prop: Annotated[t.Optional[str], Symmetric(match_none=True)]

            VALUE1 = 1, None
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, "None")

        class EnumWithNones(EnumProperties):
            prop: Annotated[t.Optional[str], Symmetric(case_fold=True, match_none=True)]

            VALUE1 = 1, None
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, "None")

        class EnumWithNones(EnumProperties):
            VALUE1 = None
            VALUE2 = "label"

        self.assertRaises(ValueError, EnumWithNones, "None")
        self.assertEqual(EnumWithNones(None), EnumWithNones.VALUE1)

    def test_none_to_string_coercion_disabled(self):
        class EnumWithNones(EnumProperties):
            prop: Annotated[str, Symmetric(match_none=True)]

            VALUE1 = 1, "None"
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones("None"), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties):
            prop: Annotated[str, Symmetric(case_fold=True, match_none=True)]

            VALUE1 = 1, "None"
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones("none"), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties):
            prop: Annotated[str, Symmetric(match_none=True)]

            VALUE1 = 1, "None"
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones("None"), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties):
            VALUE1 = "None"
            VALUE2 = "label"

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertRaises(KeyError, lambda x: EnumWithNones[x], None)
        self.assertEqual(EnumWithNones("None"), EnumWithNones.VALUE1)
