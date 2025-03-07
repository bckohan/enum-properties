from unittest import TestCase
from typing_extensions import Annotated

from enum_properties import EnumProperties, symmetric


class TestSymmetricDecorator(TestCase):
    """
    Test the specialize decorator
    """

    def test_symmetric_decorator_case_fold(self):
        class SymEnum(EnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

            @symmetric(case_fold=True)
            @property
            def label(self):
                return self.name

        self.assertEqual(SymEnum.ONE.label, "ONE")
        self.assertEqual(SymEnum.TWO.label, "TWO")
        self.assertEqual(SymEnum.THREE.label, "THREE")

        self.assertTrue(SymEnum("one") is SymEnum.ONE)
        self.assertTrue(SymEnum("tWo") is SymEnum.TWO)
        self.assertTrue(SymEnum("THRee") is SymEnum.THREE)

    def test_symmetric_decorator_none(self):
        class SymEnum(EnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

            @symmetric()
            @property
            def label(self):
                if self.value == 1:
                    return None
                return self.name

        self.assertTrue(SymEnum.ONE.label is None)
        self.assertEqual(SymEnum.TWO.label, "TWO")
        self.assertEqual(SymEnum.THREE.label, "THREE")

        self.assertRaises(ValueError, SymEnum, None)
        self.assertRaises(ValueError, SymEnum, "tWo")
        self.assertTrue(SymEnum("TWO") is SymEnum.TWO)
        self.assertTrue(SymEnum("THREE") is SymEnum.THREE)

        class SymNoneEnum(EnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

            @symmetric(match_none=True)
            @property
            def label(self):
                if self.value == 1:
                    return None
                return self.name

        self.assertTrue(SymNoneEnum(None) is SymNoneEnum.ONE)

    def test_symmetric_decorator_function(self):
        class SymEnum(EnumProperties):
            ONE = 1
            TWO = 2
            THREE = 3

            # lol - should work with anything
            @symmetric()
            def label(self):
                return self.name

        self.assertEqual(SymEnum.ONE.label(), "ONE")
        self.assertEqual(SymEnum.TWO.label(), "TWO")
        self.assertEqual(SymEnum.THREE.label(), "THREE")

        self.assertTrue(SymEnum(SymEnum.ONE.label) is SymEnum.ONE)
        self.assertTrue(SymEnum(SymEnum.TWO.label) is SymEnum.TWO)
        self.assertTrue(SymEnum(SymEnum.THREE.label) is SymEnum.THREE)
