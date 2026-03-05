"""
Tests for the functional (dynamic) API with properties.

EnumProperties("Name", {"A": ("a", True), ...}, properties=("prop",))
"""

import sys
from unittest import TestCase
from unittest.mock import patch

from enum_properties import (
    EnumProperties,
    FlagProperties,
    IntEnumProperties,
    IntFlagProperties,
    StrEnumProperties,
    p,
    s,
)


class TestFunctionalAPI(TestCase):
    def test_basic_non_symmetric(self):
        """String property names create non-symmetric properties."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"A": ("a", True), "B": ("b", False)},
            properties=("prop",),
        )
        self.assertEqual(AnEnum.A.value, "a")
        self.assertEqual(AnEnum.B.value, "b")
        self.assertTrue(AnEnum.A.prop)
        self.assertFalse(AnEnum.B.prop)

        # Non-symmetric: cannot look up by property value
        with self.assertRaises((ValueError, KeyError)):
            AnEnum(True)

    def test_multiple_non_symmetric_properties(self):
        """Multiple string property specs work in order."""
        Color = EnumProperties(
            "Color",
            {
                "RED": (1, "Roja", "ff0000"),
                "GREEN": (2, "Verde", "00ff00"),
                "BLUE": (3, "Azul", "0000ff"),
            },
            properties=("spanish", "hex"),
        )
        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, "Roja")
        self.assertEqual(Color.RED.hex, "ff0000")
        self.assertEqual(Color.GREEN.spanish, "Verde")
        self.assertEqual(Color.BLUE.hex, "0000ff")

    def test_symmetric_via_s_type(self):
        """s() types create symmetric properties."""
        Color = EnumProperties(
            "Color",
            {
                "RED": (1, (1, 0, 0)),
                "GREEN": (2, (0, 1, 0)),
                "BLUE": (3, (0, 0, 1)),
            },
            properties=(s("rgb"),),
        )
        self.assertEqual(Color.RED.rgb, (1, 0, 0))
        self.assertIs(Color((1, 0, 0)), Color.RED)
        self.assertIs(Color((0, 1, 0)), Color.GREEN)
        self.assertIs(Color((0, 0, 1)), Color.BLUE)

    def test_case_fold_symmetric(self):
        """s() with case_fold=True creates case-insensitive symmetric lookup."""
        Color = EnumProperties(
            "Color",
            {
                "RED": (1, "ff0000"),
                "GREEN": (2, "00ff00"),
                "BLUE": (3, "0000ff"),
            },
            properties=(s("hex", case_fold=True),),
        )
        self.assertEqual(Color.RED.hex, "ff0000")
        self.assertIs(Color("ff0000"), Color.RED)
        self.assertIs(Color("FF0000"), Color.RED)
        self.assertIs(Color("00ff00"), Color.GREEN)
        self.assertIs(Color("0000FF"), Color.BLUE)

    def test_mixed_symmetric_and_plain(self):
        """Mix of string and s() properties works correctly."""
        Color = EnumProperties(
            "Color",
            {
                "RED": (1, "Roja", (1, 0, 0)),
                "GREEN": (2, "Verde", (0, 1, 0)),
                "BLUE": (3, "Azul", (0, 0, 1)),
            },
            properties=("spanish", s("rgb")),
        )
        self.assertEqual(Color.RED.spanish, "Roja")
        self.assertEqual(Color.RED.rgb, (1, 0, 0))
        # rgb is symmetric
        self.assertIs(Color((1, 0, 0)), Color.RED)
        # spanish is not symmetric
        with self.assertRaises((ValueError, KeyError)):
            Color("Roja")

    def test_p_type_in_properties(self):
        """Explicit p() type in properties works like a string name."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"X": ("x", 10), "Y": ("y", 20)},
            properties=(p("score"),),
        )
        self.assertEqual(AnEnum.X.score, 10)
        self.assertEqual(AnEnum.Y.score, 20)

    def test_names_as_mapping(self):
        """Any Mapping (not just dict) is accepted for names."""
        from collections import OrderedDict
        from types import MappingProxyType

        for mapping in (
            OrderedDict([("A", ("a", 1)), ("B", ("b", 2))]),
            MappingProxyType({"A": ("a", 1), "B": ("b", 2)}),
        ):
            with self.subTest(mapping_type=type(mapping).__name__):
                AnEnum = EnumProperties("AnEnum", mapping, properties=("num",))
                self.assertEqual(AnEnum.A.value, "a")
                self.assertEqual(AnEnum.A.num, 1)
                self.assertEqual(AnEnum.B.num, 2)

    def test_list_of_pairs_format(self):
        """names as a list of (name, value) pairs is supported."""
        AnEnum = EnumProperties(
            "AnEnum",
            [("A", ("a", 1)), ("B", ("b", 2))],
            properties=("num",),
        )
        self.assertEqual(AnEnum.A.value, "a")
        self.assertEqual(AnEnum.A.num, 1)
        self.assertEqual(AnEnum.B.num, 2)

    def test_int_enum_properties(self):
        """IntEnumProperties works with the functional API."""
        Status = IntEnumProperties(
            "Status",
            {"PENDING": (1, "Pending"), "DONE": (2, "Done")},
            properties=("label",),
        )
        self.assertEqual(Status.PENDING, 1)
        self.assertEqual(Status.PENDING.label, "Pending")
        self.assertEqual(Status.DONE.label, "Done")

    def test_str_enum_properties(self):
        """StrEnumProperties works with the functional API."""
        Color = StrEnumProperties(
            "Color",
            {"RED": ("red", "#f00"), "BLUE": ("blue", "#00f")},
            properties=("hex",),
        )
        self.assertEqual(Color.RED, "red")
        self.assertEqual(Color.RED.hex, "#f00")

    def test_module_set(self):
        """The created enum's __module__ is set to the calling module."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"A": ("a", 1)},
            properties=("num",),
        )
        self.assertEqual(AnEnum.__module__, __name__)

    def test_module_explicit(self):
        """Explicit module= overrides automatic module detection."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"A": ("a", 1)},
            properties=("num",),
            module="my.module",
        )
        self.assertEqual(AnEnum.__module__, "my.module")

    def test_qualname(self):
        """Explicit qualname= is applied to the created class."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"A": ("a", 1)},
            properties=("num",),
            qualname="SomeOuter.AnEnum",
        )
        self.assertEqual(AnEnum.__qualname__, "SomeOuter.AnEnum")

    def test_invalid_property_spec_raises(self):
        """Non-string, non-p/s property raises TypeError."""
        with self.assertRaises(TypeError):
            EnumProperties(
                "AnEnum",
                {"A": ("a", 1)},
                properties=(42,),
            )

    def test_no_names_with_properties_raises(self):
        """Passing properties= without names= is not allowed."""
        with self.assertRaises(TypeError):
            EnumProperties("AnEnum", properties=("prop",))

    def test_normal_lookup_unaffected(self):
        """Ordinary value lookup still works on a class created normally."""

        class Color(EnumProperties):
            label: str

            RED = 1, "Red"
            GREEN = 2, "Green"

        self.assertIs(Color(1), Color.RED)
        self.assertIs(Color(2), Color.GREEN)

    def test_functional_members_list(self):
        """All members are accessible via iteration."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"A": ("a", 1), "B": ("b", 2), "C": ("c", 3)},
            properties=("num",),
        )
        self.assertEqual([m.name for m in AnEnum], ["A", "B", "C"])
        self.assertEqual([m.num for m in AnEnum], [1, 2, 3])

    def test_symmetric_name_lookup(self):
        """name is always symmetric on EnumProperties subclasses."""
        AnEnum = EnumProperties(
            "AnEnum",
            {"ALPHA": ("a", True), "BETA": ("b", False)},
            properties=("flag",),
        )
        self.assertIs(AnEnum("ALPHA"), AnEnum.ALPHA)
        self.assertIs(AnEnum("BETA"), AnEnum.BETA)

    def test_flag_properties(self):
        """FlagProperties works with the functional API."""
        Perm = FlagProperties(
            "Perm",
            {
                "R": (1, "read"),
                "W": (2, "write"),
                "X": (4, "execute"),
                "RWX": (7, "all"),
            },
            properties=(s("label", case_fold=True),),
        )
        self.assertEqual(Perm.R.label, "read")
        self.assertEqual(Perm.W.label, "write")
        self.assertEqual(Perm.X.label, "execute")
        self.assertEqual(Perm.RWX.label, "all")

        # Symmetric lookup by label
        self.assertIs(Perm("read"), Perm.R)
        self.assertIs(Perm("READ"), Perm.R)
        self.assertIs(Perm("write"), Perm.W)
        self.assertIs(Perm("all"), Perm.RWX)

        # Composite flag construction from iterable of members
        self.assertIs(Perm([Perm.R, Perm.W, Perm.X]), Perm.RWX)
        self.assertIs(Perm({"read", "write", "execute"}), Perm.RWX)

        # DecomposeMixin: iteration and flagged
        self.assertCountEqual(list(Perm.R | Perm.W), [Perm.R, Perm.W])
        self.assertCountEqual(Perm.RWX.flagged, [Perm.R, Perm.W, Perm.X])
        self.assertEqual(len(Perm.R | Perm.W), 2)
        self.assertEqual(len(Perm.RWX), 3)
        self.assertEqual(len(Perm.R), 1)

    def test_int_flag_properties(self):
        """IntFlagProperties works with the functional API."""
        Perm = IntFlagProperties(
            "Perm",
            {
                "R": (1, "read"),
                "W": (2, "write"),
                "X": (4, "execute"),
            },
            properties=(s("label", case_fold=True),),
        )
        self.assertEqual(Perm.R.label, "read")
        self.assertEqual(Perm.W.label, "write")
        self.assertEqual(Perm.X.label, "execute")

        # IntFlag: numeric equality
        self.assertEqual(Perm.R, 1)
        self.assertEqual(Perm.W, 2)
        self.assertEqual(Perm.X, 4)

        # Symmetric lookup
        self.assertIs(Perm("read"), Perm.R)
        self.assertIs(Perm("WRITE"), Perm.W)

        # Composite via OR
        rwx = Perm.R | Perm.W | Perm.X
        self.assertEqual(rwx, 7)
        self.assertCountEqual(rwx.flagged, [Perm.R, Perm.W, Perm.X])

    def test_flag_non_symmetric_property(self):
        """FlagProperties with a non-symmetric property works correctly."""
        Perm = FlagProperties(
            "Perm",
            {
                "R": (1, "read", "r"),
                "W": (2, "write", "w"),
                "X": (4, "execute", "x"),
            },
            properties=(s("label", case_fold=True), "short"),
        )
        self.assertEqual(Perm.R.short, "r")
        self.assertEqual(Perm.W.short, "w")
        self.assertEqual(Perm.X.short, "x")

        # label is symmetric, short is not
        self.assertIs(Perm("read"), Perm.R)
        # Python 3.10's Flag._missing_ raises TypeError for non-integer values
        with self.assertRaises((ValueError, KeyError, TypeError)):
            Perm("r")

    # ------------------------------------------------------------------
    # Branch-coverage tests for __call__
    # ------------------------------------------------------------------

    def test_standard_functional_api_no_properties(self):
        """Standard functional API (names but no properties=) is unchanged."""
        # Exercises the super().__call__(value, names, ...) delegation (line 454)
        AnEnum = EnumProperties("AnEnum", {"A": 1, "B": 2})
        self.assertEqual(AnEnum.A.value, 1)
        self.assertEqual(AnEnum.B.value, 2)
        # name is still symmetric by default
        self.assertIs(AnEnum("A"), AnEnum.A)

    def test_properties_as_string_raises(self):
        """Passing a bare string for properties= raises TypeError with a hint."""
        with self.assertRaisesRegex(TypeError, r"Did you mean properties=\("):
            EnumProperties(
                "AnEnum",
                {"A": ("a", 1)},
                properties="label",  # accidentally a string, not a tuple
            )

    def test_invalid_property_not_subclass_raises(self):
        """A class that is not a _Prop subclass raises TypeError (line 476->481)."""
        with self.assertRaises(TypeError):
            EnumProperties(
                "AnEnum",
                {"A": ("a", 1)},
                properties=(int,),  # int is a type but NOT a _Prop subclass
            )

    def test_type_mixin(self):
        """type= kwarg produces a class that also inherits from the mixin (line 491)."""
        IntColor = EnumProperties(
            "IntColor",
            {"RED": (1, "red"), "GREEN": (2, "green")},
            type=int,
            properties=("label",),
        )
        # inherits from int: numeric equality
        self.assertEqual(IntColor.RED, 1)
        self.assertEqual(IntColor.GREEN, 2)
        self.assertEqual(IntColor.RED.label, "red")
        self.assertTrue(issubclass(IntColor, int))

    def test_names_as_string(self):
        """names as a space/comma-separated string auto-assigns values (line 500)."""
        # No properties needed here; the string form produces plain names
        AnEnum = EnumProperties("AnEnum", "A B C")
        self.assertEqual([m.name for m in AnEnum], ["A", "B", "C"])
        self.assertEqual([m.value for m in AnEnum], [1, 2, 3])

    def test_names_as_string_with_properties(self):
        """names as string + properties raises because values can't carry props."""
        # The string form produces scalar values, not tuples, so property
        # extraction will raise.
        with self.assertRaises(ValueError):
            EnumProperties("AnEnum", "A B C", properties=("label",))

    def test_names_as_empty_list(self):
        """Empty list of names produces an enum with no members (line 505)."""
        AnEnum = EnumProperties("AnEnum", [], properties=("label",))
        self.assertEqual(list(AnEnum), [])

    def test_names_as_plain_list_of_strings(self):
        """List of plain strings auto-assigns sequential start values (line 508)."""
        AnEnum = EnumProperties("AnEnum", ["X", "Y", "Z"], start=10)
        self.assertEqual(AnEnum.X.value, 10)
        self.assertEqual(AnEnum.Y.value, 11)
        self.assertEqual(AnEnum.Z.value, 12)

    def test_names_as_generic_iterable(self):
        """A generator of (name, value) pairs is consumed correctly."""
        pairs = (
            (name, (i, label))
            for i, (name, label) in enumerate([("A", "alpha"), ("B", "beta")], start=1)
        )
        AnEnum = EnumProperties("AnEnum", pairs, properties=("label",))
        self.assertEqual(AnEnum.A.value, 1)
        self.assertEqual(AnEnum.A.label, "alpha")
        self.assertEqual(AnEnum.B.label, "beta")

    def test_names_as_string_generator_with_properties_raises(self):
        """Generator of plain string names + properties= raises (no property data)."""
        with self.assertRaises(ValueError):
            EnumProperties(
                "AnEnum",
                (n for n in ["A", "B"]),
                properties=("label",),
            )

    def test_module_not_set_when_getframe_fails(self):
        """When sys._getframe raises, module stays None and __module__ is unchanged
        (lines 530-531, 533->536)."""
        with patch.object(sys, "_getframe", side_effect=ValueError("no frame")):
            AnEnum = EnumProperties(
                "AnEnum",
                {"A": ("a", 1)},
                properties=("num",),
            )
        # __module__ will be whatever Python set during class construction —
        # the key assertion is that we didn't crash and module wasn't set by us.
        self.assertNotEqual(AnEnum.__module__, __name__)
