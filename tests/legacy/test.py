from collections.abc import Hashable
from enum import Enum, auto
from unittest import TestCase

from enum_properties import EnumProperties, IntEnumProperties, SymmetricMixin, p, s


class TestEnums(TestCase):
    def test_p(self):
        from enum_properties import _Prop

        prop1 = p("prop1")
        prop2 = s("prop2")
        prop3 = s("prop3", case_fold=True)
        prop4 = p("prop4")

        self.assertTrue(issubclass(prop1, _Prop))
        self.assertTrue(issubclass(prop2, _Prop))
        self.assertTrue(issubclass(prop3, _Prop))
        self.assertTrue(issubclass(prop4, _Prop))
        self.assertEqual(prop1.name(), "prop1")
        self.assertEqual(prop2.name(), "prop2")
        self.assertEqual(prop3.name(), "prop3")
        self.assertEqual(prop4.name(), "prop4")
        self.assertEqual(prop1(), "prop1")
        self.assertEqual(prop2(), "prop2")
        self.assertEqual(prop3(), "prop3")
        self.assertEqual(prop4(), "prop4")

        self.assertFalse(prop1.symmetric)
        self.assertTrue(prop2.symmetric)
        self.assertTrue(prop3.symmetric)
        self.assertFalse(prop4.symmetric)

        self.assertFalse(prop1().symmetric)
        self.assertTrue(prop2().symmetric)
        self.assertTrue(prop3().symmetric)
        self.assertFalse(prop4().symmetric)

        self.assertFalse(hasattr(prop1, "case_fold"))
        self.assertFalse(prop2.case_fold)
        self.assertTrue(prop3.case_fold)
        self.assertFalse(hasattr(prop4, "case_fold"))

        self.assertFalse(hasattr(prop1(), "case_fold"))
        self.assertFalse(prop2().case_fold)
        self.assertTrue(prop3().case_fold)
        self.assertFalse(hasattr(prop4(), "case_fold"))

    def test_unhashable_symmetry(self):
        """
        Tests that a value error is thrown when an unhashable type is used as
        a symmetric property
        """
        with self.assertRaises(ValueError):

            class BadEnum(EnumProperties, s("bad_prop")):
                VAL1 = "E1", "E1 Label", "Good prop"
                VAL2 = "E2", "E2 Label", {"hashable": False}

    def test_unicode_casefold(self):
        class CaseAgnostic(EnumProperties, s("label", case_fold=True)):
            ONE = 1, "ß"
            TWO = 2, "Σίσυφος"

        self.assertEqual(CaseAgnostic.ONE, CaseAgnostic("ss"))
        self.assertEqual(CaseAgnostic.TWO, CaseAgnostic("ΣΊΣΥΦΟΣ"))

        # test that closest case matches first
        class CaseFirstMatch(EnumProperties, s("label", case_fold=True)):
            ONE = 1, "ß"
            TWO = 2, "Σίσυφος"
            THREE = 3, "ss"

        self.assertEqual(CaseFirstMatch.THREE, CaseFirstMatch("ss"))
        self.assertEqual(CaseFirstMatch.ONE, CaseFirstMatch("ß"))
        self.assertEqual(CaseFirstMatch.TWO, CaseFirstMatch("ΣΊΣΥΦΟΣ"))

    def test_properties_and_symmetry(self):
        class Color(
            IntEnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)
        ):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), "00ff00"
            BLUE = 3, "Azul", (0, 0, 1), "0000ff"

        self.assertEqual(Color.RED, Color((1, 0, 0)))
        self.assertEqual(Color.RED, Color("ff0000"))
        self.assertEqual(Color.RED, Color("FF0000"))
        self.assertEqual(Color.RED, Color("RED"))
        self.assertEqual(Color.RED, Color["RED"])
        self.assertEqual(Color.RED, Color(1))
        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, "Roja")
        self.assertEqual(Color.RED.hex, "ff0000")
        self.assertRaises(ValueError, Color, "Roja")
        self.assertRaises(ValueError, Color, "Red")

        # test symmetric equality
        self.assertEqual(Color.RED, (1, 0, 0))
        self.assertEqual(Color.RED, "ff0000")
        self.assertEqual(Color.RED, "FF0000")
        self.assertEqual(Color.RED, "RED")
        self.assertEqual(Color.RED, 1)

        self.assertTrue(Color.RED != (1, 1, 0))
        self.assertTrue(Color.RED != "00ff00")
        self.assertTrue(Color.RED != "EE0000")
        self.assertTrue(Color.RED != "GRAY")
        self.assertTrue(Color.RED != 3)

        self.assertFalse(Color.RED != (1, 0, 0))
        self.assertFalse(Color.RED != "ff0000")
        self.assertFalse(Color.RED != "FF0000")
        self.assertFalse(Color.RED != "RED")
        self.assertFalse(Color.RED != 1)

        self.assertNotEqual(Color.RED, (1, 1, 0))
        self.assertNotEqual(Color.RED, "EE0000")
        self.assertNotEqual(Color.RED, "00ff00")
        self.assertNotEqual(Color.RED, "GREEN")
        self.assertNotEqual(Color.RED, 5)
        ############################

        self.assertEqual(Color.GREEN, Color((0, 1, 0)))
        self.assertEqual(Color.GREEN, Color("00ff00"))
        self.assertEqual(Color.GREEN, Color("00FF00"))
        self.assertEqual(Color.GREEN, Color("GREEN"))
        self.assertEqual(Color.GREEN, Color["GREEN"])
        self.assertEqual(Color.GREEN, Color(2))
        self.assertEqual(Color.GREEN.value, 2)
        self.assertEqual(Color.GREEN.spanish, "Verde")
        self.assertEqual(Color.GREEN.hex, "00ff00")
        self.assertRaises(ValueError, Color, "Verde")
        self.assertRaises(ValueError, Color, "Green")

        # test symmetric equality
        self.assertEqual(Color.GREEN, (0, 1, 0))
        self.assertEqual(Color.GREEN, "00ff00")
        self.assertEqual(Color.GREEN, "00FF00")
        self.assertEqual(Color.GREEN, "GREEN")
        self.assertEqual(Color.GREEN, 2)
        self.assertNotEqual(Color.GREEN, "EE0000")

        self.assertEqual(Color.BLUE, Color((0, 0, 1)))
        self.assertEqual(Color.BLUE, Color("0000ff"))
        self.assertEqual(Color.BLUE, Color("0000FF"))
        self.assertEqual(Color.BLUE, Color("BLUE"))
        self.assertEqual(Color.BLUE, Color["BLUE"])
        self.assertEqual(Color.BLUE, Color(3))
        self.assertEqual(Color.BLUE.value, 3)
        self.assertEqual(Color.BLUE.spanish, "Azul")
        self.assertEqual(Color.BLUE.hex, "0000ff")
        self.assertRaises(ValueError, Color, "Azul")
        self.assertRaises(ValueError, Color, "Blue")

        # test symmetric equality
        self.assertEqual(Color.BLUE, (0, 0, 1))
        self.assertEqual(Color.BLUE, "0000ff")
        self.assertEqual(Color.BLUE, "0000FF")
        self.assertEqual(Color.BLUE, "BLUE")
        self.assertEqual(Color.BLUE, 3)
        self.assertNotEqual(Color.BLUE, (0, 1, 1))

    def test_property_lists(self):
        class Color(EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), "00ff00"
            BLUE = 3, "Azul", (0, 0, 1), "0000ff"

        self.assertEqual(
            [prop for prop in Color._properties_ if prop.symmetric], ["rgb", "hex"]
        )

        self.assertEqual(Color._properties_, ["spanish", "rgb", "hex"])

    def test_symmetric_builtin_override(self):
        class Color(EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)):
            _symmetric_builtins_ = [s("name", case_fold=True)]

            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), "00ff00"
            BLUE = 3, "Azul", (0, 0, 1), "0000ff"

        self.assertEqual(Color.RED, Color("red"))
        self.assertEqual(Color.GREEN, Color("gREen"))
        self.assertEqual(Color.BLUE, Color("Blue"))

    def test_symmetric_builtin_override_wrongtype(self):
        with self.assertRaises(ValueError):

            class Color(
                EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)
            ):
                _symmetric_builtins_ = [p("name")]

                RED = 1, "Roja", (1, 0, 0), "ff0000"
                GREEN = 2, "Verde", (0, 1, 0), "00ff00"
                BLUE = 3, "Azul", (0, 0, 1), "0000ff"

    def test_symmetric_builtin_override_missing(self):
        with self.assertRaises(ValueError):

            class Color(
                EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)
            ):
                _symmetric_builtins_ = [s("does_not_exist")]

                RED = 1, "Roja", (1, 0, 0), "ff0000"
                GREEN = 2, "Verde", (0, 1, 0), "00ff00"
                BLUE = 3, "Azul", (0, 0, 1), "0000ff"

    def test_symmetric_match_none_parameter(self):
        # test default behavior
        class ColorDefault(EnumProperties, p("spanish"), s("rgb"), s("hex")):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), None
            BLUE = 3, "Azul", (0, 0, 1), None

        self.assertEqual(ColorDefault.RED, "ff0000")
        self.assertNotEqual(ColorDefault.GREEN, None)
        self.assertNotEqual(ColorDefault.BLUE, None)
        self.assertRaises(ValueError, ColorDefault, None)
        self.assertRaises(ValueError, ColorDefault, "FF0000")
        self.assertEqual(ColorDefault("ff0000"), ColorDefault.RED)
        self.assertEqual(ColorDefault((1, 0, 0)), ColorDefault.RED)
        self.assertEqual(ColorDefault((0, 1, 0)), ColorDefault.GREEN)
        self.assertEqual(ColorDefault((0, 0, 1)), ColorDefault.BLUE)

        class ColorNoMatchNone(
            EnumProperties,
            p("spanish"),
            s("rgb"),
            s("hex", case_fold=True, match_none=False),
        ):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), None
            BLUE = 3, "Azul", (0, 0, 1), None

        self.assertEqual(ColorNoMatchNone.RED, "fF0000")
        self.assertNotEqual(ColorNoMatchNone.GREEN, None)
        self.assertNotEqual(ColorNoMatchNone.BLUE, None)
        self.assertRaises(ValueError, ColorNoMatchNone, None)
        self.assertEqual(ColorNoMatchNone("Ff0000"), ColorNoMatchNone.RED)
        self.assertEqual(ColorNoMatchNone((1, 0, 0)), ColorNoMatchNone.RED)
        self.assertEqual(ColorNoMatchNone((0, 1, 0)), ColorNoMatchNone.GREEN)
        self.assertEqual(ColorNoMatchNone((0, 0, 1)), ColorNoMatchNone.BLUE)

        class ColorMatchNone(
            EnumProperties, p("spanish"), s("rgb"), s("hex", match_none=True)
        ):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), None
            BLUE = 3, "Azul", (0, 0, 1), None

        self.assertNotEqual(ColorMatchNone.RED, "FF0000")
        self.assertEqual(ColorMatchNone.RED, "ff0000")
        self.assertEqual(ColorMatchNone.GREEN, None)
        self.assertNotEqual(ColorMatchNone.BLUE, None)
        self.assertEqual(ColorMatchNone(None), ColorMatchNone.GREEN)
        self.assertEqual(ColorMatchNone("ff0000"), ColorMatchNone.RED)
        self.assertRaises(ValueError, ColorMatchNone, "FF0000")
        self.assertEqual(ColorMatchNone((1, 0, 0)), ColorMatchNone.RED)
        self.assertEqual(ColorMatchNone((0, 1, 0)), ColorMatchNone.GREEN)
        self.assertEqual(ColorMatchNone((0, 0, 1)), ColorMatchNone.BLUE)

    def test_properties_no_symmetry(self):
        """
        Tests that absence of SymmetricMixin works but w/o symmetric
        properties
        """

        class DisableSymmetryMixin(SymmetricMixin):
            @classmethod
            def _missing_(cls, value):
                return Enum._missing_(value)

        class Color(
            DisableSymmetryMixin,
            EnumProperties,
            p("spanish"),
            s("rgb"),
            s("hex", case_fold=True),
        ):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), "00ff00"
            BLUE = 3, "Azul", (0, 0, 1), "0000ff"

        self.assertRaises(ValueError, Color, (1, 0, 0))
        self.assertRaises(ValueError, Color, "ff0000")
        self.assertRaises(ValueError, Color, "FF0000")
        self.assertRaises(ValueError, Color, "RED")
        self.assertEqual(Color.RED, Color["RED"])
        self.assertEqual(Color.RED, Color(1))
        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, "Roja")
        self.assertEqual(Color.RED.hex, "ff0000")
        self.assertRaises(ValueError, Color, "Roja")
        self.assertRaises(ValueError, Color, "Red")

        self.assertRaises(ValueError, Color, (0, 1, 0))
        self.assertRaises(ValueError, Color, "00ff00")
        self.assertRaises(ValueError, Color, "00FF00")
        self.assertRaises(ValueError, Color, "GREEN")
        self.assertEqual(Color.GREEN, Color["GREEN"])
        self.assertEqual(Color.GREEN, Color(2))
        self.assertEqual(Color.GREEN.value, 2)
        self.assertEqual(Color.GREEN.spanish, "Verde")
        self.assertEqual(Color.GREEN.hex, "00ff00")
        self.assertRaises(ValueError, Color, "Verde")
        self.assertRaises(ValueError, Color, "Green")

        self.assertRaises(ValueError, Color, (0, 0, 1))
        self.assertRaises(ValueError, Color, "0000ff")
        self.assertRaises(ValueError, Color, "0000FF")
        self.assertRaises(ValueError, Color, "BLUE")
        self.assertEqual(Color.BLUE, Color["BLUE"])
        self.assertEqual(Color.BLUE, Color(3))
        self.assertEqual(Color.BLUE.value, 3)
        self.assertEqual(Color.BLUE.spanish, "Azul")
        self.assertEqual(Color.BLUE.hex, "0000ff")
        self.assertRaises(ValueError, Color, "Azul")
        self.assertRaises(ValueError, Color, "Blue")

    def test_symmetry_priorities(self):
        class Priority(EnumProperties, s("prop1"), s("prop2")):
            FIRST = 1, "3", 3
            SECOND = 2, "2", 2
            THIRD = 3, "1", 1

        self.assertEqual(Priority.FIRST, Priority(1))
        self.assertEqual(Priority.FIRST, Priority("3"))
        self.assertEqual(Priority.SECOND, Priority(2))
        self.assertEqual(Priority.SECOND, Priority("2"))
        self.assertEqual(Priority.THIRD, Priority(3))
        self.assertEqual(Priority.THIRD, Priority("1"))

    def test_symmetry_tuples(self):
        class Priority(EnumProperties, s("prop1"), s("prop2")):
            FIRST = 1, "3", [2.1, "2.3"]
            SECOND = 2, "2", [2.2, "2.2"]
            THIRD = 3, "1", [2.3, "2.1"]

        self.assertEqual(Priority.FIRST, Priority(1))
        self.assertEqual(Priority.FIRST, Priority("3"))
        self.assertEqual(Priority.SECOND, Priority(2))
        self.assertEqual(Priority.SECOND, Priority("2"))
        self.assertEqual(Priority.THIRD, Priority(3))
        self.assertEqual(Priority.THIRD, Priority("1"))

        self.assertEqual(Priority.FIRST, Priority(2.1))
        self.assertEqual(Priority.FIRST, Priority("2.3"))
        self.assertEqual(Priority.SECOND, Priority(2.2))
        self.assertEqual(Priority.SECOND, Priority("2.2"))
        self.assertEqual(Priority.THIRD, Priority(2.3))
        self.assertEqual(Priority.THIRD, Priority("2.1"))

    def test_auto(self):
        class ColorAuto(EnumProperties):
            def _generate_next_value_(name, start, count, last_values):
                return name.title()

            RED = auto()
            GREEN = auto()
            BLUE = auto()

        self.assertEqual(ColorAuto.RED, ColorAuto("Red"))
        self.assertEqual(ColorAuto.GREEN, ColorAuto("Green"))
        self.assertEqual(ColorAuto.BLUE, ColorAuto("Blue"))
        self.assertEqual(ColorAuto.RED, ColorAuto["RED"])
        self.assertEqual(ColorAuto.GREEN, ColorAuto["GREEN"])
        self.assertEqual(ColorAuto.BLUE, ColorAuto["BLUE"])

        class ColorAutoSym(
            EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)
        ):
            def _generate_next_value_(name, start, count, last_values):
                return name.title()

            RED = auto(), "Roja", (1, 0, 0), "ff0000"
            GREEN = auto(), "Verde", (0, 1, 0), "00ff00"
            BLUE = auto(), "Azul", (0, 0, 1), "0000ff"

        self.assertEqual(ColorAutoSym.RED, ColorAutoSym["RED"])
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym["GREEN"])
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym["BLUE"])
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym("Red"))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym("Green"))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym("Blue"))

        self.assertEqual(ColorAutoSym.RED, ColorAutoSym((1, 0, 0)))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym("ff0000"))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym("FF0000"))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym("RED"))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym["RED"])
        self.assertEqual(ColorAutoSym.RED.value, "Red")
        self.assertEqual(ColorAutoSym.RED.spanish, "Roja")
        self.assertEqual(ColorAutoSym.RED.hex, "ff0000")
        self.assertRaises(ValueError, ColorAutoSym, "Roja")

        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym((0, 1, 0)))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym("00ff00"))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym("00FF00"))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym("GREEN"))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym["GREEN"])
        self.assertEqual(ColorAutoSym.GREEN.value, "Green")
        self.assertEqual(ColorAutoSym.GREEN.spanish, "Verde")
        self.assertEqual(ColorAutoSym.GREEN.hex, "00ff00")
        self.assertRaises(ValueError, ColorAutoSym, "Verde")

        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym((0, 0, 1)))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym("0000ff"))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym("0000FF"))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym("BLUE"))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym["BLUE"])
        self.assertEqual(ColorAutoSym.BLUE.value, "Blue")
        self.assertEqual(ColorAutoSym.BLUE.spanish, "Azul")
        self.assertEqual(ColorAutoSym.BLUE.hex, "0000ff")
        self.assertRaises(ValueError, ColorAutoSym, "Azul")

        class ColorAutoIntSym(
            EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)
        ):
            RED = auto(), "Roja", (1, 0, 0), "ff0000"
            GREEN = auto(), "Verde", (0, 1, 0), "00ff00"
            BLUE = auto(), "Azul", (0, 0, 1), "0000ff"

        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym["RED"])
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym["GREEN"])
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym["BLUE"])
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym(1))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym(2))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym(3))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym("1"))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym("2"))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym("3"))

        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym((1, 0, 0)))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym("ff0000"))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym("FF0000"))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym("RED"))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym["RED"])
        self.assertEqual(ColorAutoIntSym.RED.value, 1)
        self.assertEqual(ColorAutoIntSym.RED.spanish, "Roja")
        self.assertEqual(ColorAutoIntSym.RED.hex, "ff0000")
        self.assertRaises(ValueError, ColorAutoIntSym, "Roja")

        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym((0, 1, 0)))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym("00ff00"))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym("00FF00"))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym("GREEN"))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym["GREEN"])
        self.assertEqual(ColorAutoIntSym.GREEN.value, 2)
        self.assertEqual(ColorAutoIntSym.GREEN.spanish, "Verde")
        self.assertEqual(ColorAutoIntSym.GREEN.hex, "00ff00")
        self.assertRaises(ValueError, ColorAutoIntSym, "Verde")

        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym((0, 0, 1)))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym("0000ff"))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym("0000FF"))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym("BLUE"))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym["BLUE"])
        self.assertEqual(ColorAutoIntSym.BLUE.value, 3)
        self.assertEqual(ColorAutoIntSym.BLUE.spanish, "Azul")
        self.assertEqual(ColorAutoIntSym.BLUE.hex, "0000ff")
        self.assertRaises(ValueError, ColorAutoIntSym, "Azul")

    def test_ignore(self):
        class Color(EnumProperties, p("spanish"), s("rgb"), s("hex", case_fold=True)):
            _ignore_ = ["BLACK", "NOT_ENOUGH_PROPS"]

            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, "Verde", (0, 1, 0), "00ff00"
            BLUE = 3, "Azul", (0, 0, 1), "0000ff"
            BLACK = 4, "Negra", (1, 1, 1), "ffffff"
            NOT_ENOUGH_PROPS = 5, "Not Enough"

        self.assertFalse(hasattr(Color, "BLACK"))
        self.assertRaises(ValueError, Color, 4)
        self.assertRaises(ValueError, Color, (1, 1, 1))
        self.assertRaises(ValueError, Color, "ffffff")

    def test_no_props(self):
        class Color(EnumProperties):
            RED = 1, 0, 0
            GREEN = 0, 1, 0
            BLUE = 0, 0, 1

        self.assertEqual(Color.RED.value, (1, 0, 0))
        self.assertEqual(Color.GREEN.value, (0, 1, 0))
        self.assertEqual(Color.BLUE.value, (0, 0, 1))

        class Color2(EnumProperties):
            RED = 1
            GREEN = 2
            BLUE = 3

        self.assertEqual(Color2.RED.value, 1)
        self.assertEqual(Color2.GREEN.value, 2)
        self.assertEqual(Color2.BLUE.value, 3)

    def test_not_enough_props(self):
        with self.assertRaises(ValueError):

            class Color(EnumProperties, p("prop1"), p("prop2")):
                RED = 1, "p1.1", "p2.1"
                GREEN = 2, "p1.2", "p2.2"
                BLUE = 3, "p1.3"

        with self.assertRaises(ValueError):

            class Color2(EnumProperties, p("prop1")):
                RED = 1, "p1.1"
                GREEN = 2
                BLUE = 3, "p1.3"  # pragma: no cover

    def test_null_props(self):
        class Color(
            EnumProperties,
            p("spanish"),
            s("rgb"),
            s("hex", case_fold=True, match_none=True),
        ):
            RED = 1, "Roja", (1, 0, 0), "ff0000"
            GREEN = 2, None, (0, 1, 0), "00ff00"
            BLUE = 3, "Azul", (0, 0, 1), "0000ff"
            BLACK = 4, "Negra", (1, 1, 1), "ffffff"
            TRANSPARENT = 5, "Transparente", None, None

        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, "Roja")
        self.assertEqual(Color.RED.rgb, (1, 0, 0))
        self.assertEqual(Color.RED.hex, "ff0000")

        self.assertEqual(Color.GREEN.value, 2)
        self.assertIsNone(Color.GREEN.spanish)
        self.assertEqual(Color.GREEN.rgb, (0, 1, 0))
        self.assertEqual(Color.GREEN.hex, "00ff00")

        self.assertEqual(Color.BLUE.value, 3)
        self.assertEqual(Color.BLUE.spanish, "Azul")
        self.assertEqual(Color.BLUE.rgb, (0, 0, 1))
        self.assertEqual(Color.BLUE.hex, "0000ff")

        self.assertEqual(Color.BLACK.value, 4)
        self.assertEqual(Color.BLACK.spanish, "Negra")
        self.assertEqual(Color.BLACK.rgb, (1, 1, 1))
        self.assertEqual(Color.BLACK.hex, "ffffff")

        self.assertEqual(Color.TRANSPARENT.value, 5)
        self.assertEqual(Color.TRANSPARENT.spanish, "Transparente")
        self.assertIsNone(Color.TRANSPARENT.rgb)
        self.assertIsNone(Color.TRANSPARENT.hex)

        self.assertEqual(Color.TRANSPARENT, Color(None))

    def test_examples(self):
        """
        Any example used in docs or readme should be tested here
        todo way to make this dry? sphinx plugin?
        """

        class Color(EnumProperties, p("rgb"), p("hex")):
            RED = auto(), (1, 0, 0), "ff0000"
            GREEN = auto(), (0, 1, 0), "00ff00"
            BLUE = auto(), (0, 0, 1), "0000ff"

        self.assertEqual(Color.RED.rgb, (1, 0, 0))
        self.assertEqual(Color.GREEN.rgb, (0, 1, 0))
        self.assertEqual(Color.BLUE.rgb, (0, 0, 1))

        self.assertEqual(Color.RED.hex, "ff0000")
        self.assertEqual(Color.GREEN.hex, "00ff00")
        self.assertEqual(Color.BLUE.hex, "0000ff")

        class Color(EnumProperties, s("rgb"), s("hex", case_fold=True)):
            RED = auto(), (1, 0, 0), "0xff0000"
            GREEN = auto(), (0, 1, 0), "0x00ff00"
            BLUE = auto(), (0, 0, 1), "0x0000ff"

        self.assertEqual(Color.RED, Color((1, 0, 0)))
        self.assertEqual(Color.GREEN, Color((0, 1, 0)))
        self.assertEqual(Color.BLUE, Color((0, 0, 1)))

        self.assertEqual(Color.RED, Color("0xff0000"))
        self.assertEqual(Color.GREEN, Color("0x00ff00"))
        self.assertEqual(Color.BLUE, Color("0x0000ff"))

        self.assertTrue(
            Color.RED
            == Color(hex(16711680))
            == hex(16711680)
            == "0xff0000"
            == Color.RED
        )
        self.assertTrue(Color.RED == (1, 0, 0))
        self.assertTrue((1, 0, 0) == Color.RED)
        self.assertTrue(Color.RED != (0, 1, 0))
        self.assertTrue((0, 1, 0) != Color.RED)
        self.assertTrue(Color.RED == "0xFF0000")
        self.assertTrue("0xFF0000" == Color.RED)

        class MapBoxStyle(EnumProperties, s("label", case_fold=True), p("version")):
            """
            https://docs.mapbox.com/api/maps/styles/
            """

            _symmetric_builtins_ = ["name", "uri"]

            STREETS = "streets", "Streets", 11
            OUTDOORS = "outdoors", "Outdoors", 11
            LIGHT = "light", "Light", 10
            DARK = "dark", "Dark", 10
            SATELLITE = "satellite", "Satellite", 9
            SATELLITE_STREETS = "satellite-streets", "Satellite Streets", 11
            NAVIGATION_DAY = "navigation-day", "Navigation Day", 1
            NAVIGATION_NIGHT = "navigation-night", "Navigation Night", 1

            @property
            def uri(self):
                return f"mapbox://styles/mapbox/{self.value}-v{self.version}"

            def __str__(self):
                return self.uri

        self.assertEqual(MapBoxStyle.STREETS.version, 11)
        self.assertEqual(MapBoxStyle.OUTDOORS.version, 11)
        self.assertEqual(MapBoxStyle.LIGHT.version, 10)
        self.assertEqual(MapBoxStyle.DARK.version, 10)
        self.assertEqual(MapBoxStyle.SATELLITE.version, 9)
        self.assertEqual(MapBoxStyle.SATELLITE_STREETS.version, 11)
        self.assertEqual(MapBoxStyle.NAVIGATION_DAY.version, 1)
        self.assertEqual(MapBoxStyle.NAVIGATION_NIGHT.version, 1)

        self.assertEqual(MapBoxStyle.STREETS.uri, "mapbox://styles/mapbox/streets-v11")
        self.assertEqual(MapBoxStyle.LIGHT.uri, "mapbox://styles/mapbox/light-v10")
        self.assertEqual(MapBoxStyle.DARK.uri, "mapbox://styles/mapbox/dark-v10")
        self.assertEqual(
            MapBoxStyle.SATELLITE.uri, "mapbox://styles/mapbox/satellite-v9"
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE_STREETS.uri,
            "mapbox://styles/mapbox/satellite-streets-v11",
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_DAY.uri, "mapbox://styles/mapbox/navigation-day-v1"
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_NIGHT.uri,
            "mapbox://styles/mapbox/navigation-night-v1",
        )

        self.assertEqual(str(MapBoxStyle.STREETS), "mapbox://styles/mapbox/streets-v11")
        self.assertEqual(str(MapBoxStyle.LIGHT), "mapbox://styles/mapbox/light-v10")
        self.assertEqual(str(MapBoxStyle.DARK), "mapbox://styles/mapbox/dark-v10")
        self.assertEqual(
            str(MapBoxStyle.SATELLITE), "mapbox://styles/mapbox/satellite-v9"
        )
        self.assertEqual(
            str(MapBoxStyle.SATELLITE_STREETS),
            "mapbox://styles/mapbox/satellite-streets-v11",
        )
        self.assertEqual(
            str(MapBoxStyle.NAVIGATION_DAY), "mapbox://styles/mapbox/navigation-day-v1"
        )
        self.assertEqual(
            str(MapBoxStyle.NAVIGATION_NIGHT),
            "mapbox://styles/mapbox/navigation-night-v1",
        )

        self.assertEqual(
            MapBoxStyle.STREETS, MapBoxStyle("mapbox://styles/mapbox/streets-v11")
        )
        self.assertEqual(
            MapBoxStyle.LIGHT, MapBoxStyle("mapbox://styles/mapbox/light-v10")
        )
        self.assertEqual(
            MapBoxStyle.DARK, MapBoxStyle("mapbox://styles/mapbox/dark-v10")
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE, MapBoxStyle("mapbox://styles/mapbox/satellite-v9")
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE_STREETS,
            MapBoxStyle("mapbox://styles/mapbox/satellite-streets-v11"),
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_DAY,
            MapBoxStyle("mapbox://styles/mapbox/navigation-day-v1"),
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_NIGHT,
            MapBoxStyle("mapbox://styles/mapbox/navigation-night-v1"),
        )

        self.assertEqual(MapBoxStyle.STREETS, MapBoxStyle("streets"))
        self.assertEqual(MapBoxStyle.LIGHT, MapBoxStyle("light"))
        self.assertEqual(MapBoxStyle.DARK, MapBoxStyle("dark"))
        self.assertEqual(MapBoxStyle.SATELLITE, MapBoxStyle("satellite"))
        self.assertEqual(
            MapBoxStyle.SATELLITE_STREETS, MapBoxStyle("satellite-streets")
        )
        self.assertEqual(MapBoxStyle.NAVIGATION_DAY, MapBoxStyle("navigation-day"))
        self.assertEqual(MapBoxStyle.NAVIGATION_NIGHT, MapBoxStyle("navigation-night"))

        class AddressRoute(
            EnumProperties, s("abbr", case_fold=True), s("alt", case_fold=True)
        ):
            _symmetric_builtins_ = [s("name", case_fold=True)]

            # name  value    abbr         alt
            ALLEY = 1, "ALY", ["ALLEE", "ALLY"]
            AVENUE = 2, "AVE", ["AV", "AVEN", "AVENU", "AVN", "AVNUE"]
            CIRCLE = 3, "CIR", ["CIRC", "CIRCL", "CRCL", "CRCLE"]

        self.assertTrue(
            AddressRoute.ALLEY
            == AddressRoute("Alley")
            == AddressRoute("aly")
            == AddressRoute("ALLee")
            == AddressRoute("ALLY")
        )

        self.assertTrue(
            AddressRoute.AVENUE
            == AddressRoute("Avenue")
            == AddressRoute("AVE")
            == AddressRoute("av")
            == AddressRoute("aven")
            == AddressRoute("AVENU")
            == AddressRoute("Avn")
            == AddressRoute("AvnUE")
        )

        self.assertTrue(
            AddressRoute.CIRCLE
            == AddressRoute("circle")
            == AddressRoute("Cir")
            == AddressRoute("CIRC")
            == AddressRoute("circl")
            == AddressRoute("crcl")
            == AddressRoute("crCle")
            == AddressRoute("crCLE")
        )

    def test_properties_conflict(self):
        """enum_properties is reserved - test that we get an exception"""

        with self.assertRaises(ValueError):

            class PropConflict(EnumProperties, p("_properties_")):
                ONE = auto(), (1, 2, 3)  # pragma: no cover
                TWO = auto(), (3, 4, 5)  # pragma: no cover

        with self.assertRaises(ValueError):

            class PropConflict(EnumProperties, p("prop")):
                _properties_ = None

                ONE = auto(), (1, 2, 3)  # pragma: no cover
                TWO = auto(), (3, 4, 5)  # pragma: no cover

    def test_precedence(self):
        class PriorityEx(EnumProperties, s("prop1"), s("prop2", case_fold=True)):
            ONE = 0, "1", [3, 4]
            TWO = 1, "2", [3, "4"]
            THREE = 2, "3", [3, 4]

        self.assertEqual(PriorityEx(0), PriorityEx.ONE)
        self.assertEqual(PriorityEx("1"), PriorityEx.ONE)
        self.assertEqual(PriorityEx(3), PriorityEx.ONE)
        self.assertEqual(PriorityEx("3"), PriorityEx.THREE)
        self.assertEqual(PriorityEx(4), PriorityEx.ONE)
        self.assertEqual(PriorityEx("4"), PriorityEx.TWO)

    def test_type_coercion_precedence(self):
        """
        test that type coercion is attempted in the same precedence order as
        value resolution.
        """

        class HashableType:
            def __init__(self, value):
                self.value = value

            def __eq__(self, other):
                return self.__class__ is other.__class__ and self.value == other.value

            def __hash__(self):
                return self.value.__hash__()

        class Type1(HashableType):
            pass

        class Type2(HashableType):
            pass

        class PriorityEx(EnumProperties, s("prop1"), s("prop2")):
            ONE = 2, Type1(0), Type2(1)
            TWO = 3, Type2(0), Type1(1)

        # coercion to Type1 should be tried before coercion to type 2
        self.assertEqual(PriorityEx(Type1(0)), PriorityEx.ONE)
        self.assertEqual(PriorityEx(Type2(0)), PriorityEx.TWO)
        self.assertEqual(PriorityEx(Type1(1)), PriorityEx.TWO)
        self.assertEqual(PriorityEx(Type2(1)), PriorityEx.ONE)

        self.assertEqual(PriorityEx(0), PriorityEx.ONE)
        self.assertEqual(PriorityEx(1), PriorityEx.TWO)

    def test_hashable_enums(self):
        class HashableEnum1(Enum):
            VAL0_1 = 0
            VAL1_1 = 1
            VAL2_1 = 2

        class HashableEnum2(Enum):
            VAL0_2 = 0
            VAL1_2 = 1
            VAL2_2 = 2

        self.assertTrue(isinstance(HashableEnum1.VAL0_1, Hashable))
        self.assertTrue(isinstance(HashableEnum2.VAL1_2, Hashable))

        class TransitiveEnum(EnumProperties, p("label"), s("pos")):
            VAL0 = 0, "Value 0", HashableEnum1.VAL0_1
            VAL1 = 1, "Value 1", HashableEnum1.VAL1_1
            VAL2 = 2, "Value 2", HashableEnum2.VAL2_2

        self.assertTrue(isinstance(TransitiveEnum.VAL2, Hashable))

        self.assertEqual(TransitiveEnum(HashableEnum1.VAL0_1), TransitiveEnum.VAL0)
        self.assertEqual(TransitiveEnum(HashableEnum1.VAL1_1), TransitiveEnum.VAL1)
        self.assertEqual(TransitiveEnum(HashableEnum2.VAL2_2), TransitiveEnum.VAL2)

        self.assertRaises(ValueError, TransitiveEnum, HashableEnum1.VAL2_1)
        self.assertRaises(ValueError, TransitiveEnum, HashableEnum2.VAL0_2)
        self.assertRaises(ValueError, TransitiveEnum, HashableEnum2.VAL1_2)

        test_dict = {
            HashableEnum1.VAL0_1: "Zero",
            HashableEnum1.VAL1_1: "One",
            HashableEnum1.VAL2_1: "Two",
            HashableEnum2.VAL0_2: "zero",
            HashableEnum2.VAL1_2: "one",
            HashableEnum2.VAL2_2: "two",
            TransitiveEnum.VAL0: "ZERO",
            TransitiveEnum.VAL1: "ONE",
            TransitiveEnum.VAL2: "TWO",
        }

        self.assertEqual(test_dict[HashableEnum1.VAL0_1], "Zero")
        self.assertEqual(test_dict[HashableEnum1.VAL1_1], "One")
        self.assertEqual(test_dict[HashableEnum1.VAL2_1], "Two")

        self.assertEqual(test_dict[HashableEnum2.VAL0_2], "zero")
        self.assertEqual(test_dict[HashableEnum2.VAL1_2], "one")
        self.assertEqual(test_dict[HashableEnum2.VAL2_2], "two")

        self.assertEqual(test_dict[TransitiveEnum.VAL0], "ZERO")
        self.assertEqual(test_dict[TransitiveEnum.VAL1], "ONE")
        self.assertEqual(test_dict[TransitiveEnum.VAL2], "TWO")
