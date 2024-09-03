from unittest import TestCase

from enum_properties import (
    EnumProperties,
    s,
)


class NoneCoercionTests(TestCase):
    def test_string_to_none_coercion_disabled(self):
        class EnumWithNones(EnumProperties, s("prop", match_none=True)):
            VALUE1 = 1, None
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, "None")

        class EnumWithNones(
            EnumProperties, s("prop", case_fold=True, match_none=False)
        ):
            VALUE1 = 1, None
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, "None")

        class EnumWithNones(EnumProperties):
            VALUE1 = None
            VALUE2 = "label"

        self.assertRaises(ValueError, EnumWithNones, "None")
        self.assertEqual(EnumWithNones(None), EnumWithNones.VALUE1)

    def test_none_to_string_coercion_disabled(self):
        class EnumWithNones(EnumProperties, s("prop", match_none=True)):
            VALUE1 = 1, "None"
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones("None"), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties, s("prop", case_fold=True, match_none=True)):
            VALUE1 = 1, "None"
            VALUE2 = 2, "label"

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones("none"), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties, s("prop", match_none=False)):
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
