import typing as t
from unittest import TestCase
from typing_extensions import Annotated

from enum_properties import (
    EnumProperties,
    Symmetric,
)


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
