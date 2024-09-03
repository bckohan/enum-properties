import sys
from enum import auto
from unittest import TestCase
from typing_extensions import Annotated

from enum_properties import (
    EnumProperties,
    FlagProperties,
    IntEnumProperties,
    IntFlagProperties,
    Symmetric,
    specialize,
)


class TestFlags(TestCase):
    def test_int_flag(self):
        class Perm(IntFlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            R = 1, "read"
            W = 2, "write"
            X = 4, "execute"
            RWX = 7, "all"

            @property
            def custom_prop(self):
                return self.label.upper()

        self.assertEqual(Perm.R.label, "read")
        self.assertEqual(Perm.W.label, "write")
        self.assertEqual(Perm.X.label, "execute")
        self.assertEqual(Perm.RWX.label, "all")

        self.assertTrue(Perm.R is Perm("read"))
        self.assertTrue(Perm.W is Perm("write"))
        self.assertTrue(Perm.X is Perm("execute"))
        self.assertTrue(Perm.RWX is Perm("all"))

        self.assertEqual(Perm.W.custom_prop, "WRITE")
        self.assertEqual(Perm.RWX.custom_prop, "ALL")

        self.assertTrue((Perm.R | Perm.W | Perm.X) is Perm("RWX"))
        self.assertTrue(Perm([Perm.R, Perm.W, Perm.X]) is Perm("RWX"))
        self.assertTrue(Perm({"read", "write", "execute"}) is Perm("RWX"))
        self.assertTrue(Perm((val for val in (Perm.R, "write", 4))) is Perm("RWX"))

        self.assertEqual((Perm.R | Perm.W | Perm.X).label, "all")
        self.assertEqual((Perm("READ") | Perm("write") | Perm("X")).label, "all")

        self.assertFalse(hasattr((Perm.R | Perm.W), "label"))
        self.assertFalse(hasattr((Perm.W | Perm.X), "label"))
        self.assertFalse(hasattr((Perm.R | Perm.X), "label"))

        self.assertFalse(bool(Perm.R & Perm.X))
        self.assertFalse(hasattr((Perm.R & Perm.X), "label"))

        self.assertCountEqual((Perm.R | Perm.W).flagged, [Perm.R, Perm.W])
        self.assertCountEqual(Perm.RWX.flagged, [Perm.R, Perm.W, Perm.X])
        self.assertEqual(Perm.R.flagged, [Perm.R])
        self.assertEqual((Perm.R & Perm.X).flagged, [])

        self.assertEqual(len((Perm.R | Perm.W)), 2)
        self.assertEqual(len(Perm.RWX), 3)
        self.assertEqual(len(Perm.R), 1)
        self.assertEqual(len((Perm.R & Perm.X)), 0)

        self.assertEqual(Perm([]), Perm(0))
        self.assertEqual(Perm({}), Perm(0))
        self.assertEqual(Perm((item for item in [])), Perm(0))

        if sys.version_info >= (3, 11):  # pragma: no cover
            from enum import show_flag_values

            self.assertEqual(show_flag_values(Perm.R | Perm.X), [1, 4])
            self.assertEqual(show_flag_values(Perm.RWX), [1, 2, 4])

    def test_flag(self):
        class Perm(FlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            R = auto(), "read"
            W = auto(), "write"
            X = auto(), "execute"
            RWX = R | W | X, "all"

            @property
            def custom_prop(self):
                return self.label.upper()

        self.assertEqual(Perm.R.label, "read")
        self.assertEqual(Perm.W.label, "write")
        self.assertEqual(Perm.X.label, "execute")

        self.assertEqual(Perm.RWX.label, "all")

        self.assertTrue(Perm.R is Perm("read"))
        self.assertTrue(Perm.W is Perm("write"))
        self.assertTrue(Perm.X is Perm("execute"))
        self.assertTrue(Perm.RWX is Perm("all"))

        self.assertEqual(Perm.W.custom_prop, "WRITE")
        self.assertEqual(Perm.RWX.custom_prop, "ALL")

        self.assertTrue((Perm.R | Perm.W | Perm.X) is Perm("RWX"))
        self.assertTrue(Perm([Perm.R, Perm.W, Perm.X]) is Perm("RWX"))
        self.assertTrue(Perm({"read", "write", "execute"}) is Perm("RWX"))
        self.assertTrue(Perm((val for val in (Perm.R, "write", 4))) is Perm("RWX"))

        self.assertEqual((Perm.R | Perm.W | Perm.X).label, "all")
        self.assertEqual((Perm("READ") | Perm("write") | Perm("X")).label, "all")

        self.assertFalse(hasattr((Perm.R | Perm.W), "label"))
        self.assertFalse(hasattr((Perm.W | Perm.X), "label"))
        self.assertFalse(hasattr((Perm.R | Perm.X), "label"))

        self.assertFalse(bool(Perm.R & Perm.X))
        self.assertFalse(hasattr((Perm.R & Perm.X), "label"))

        self.assertCountEqual((Perm.R | Perm.W).flagged, [Perm.R, Perm.W])
        self.assertCountEqual(Perm.RWX.flagged, [Perm.R, Perm.W, Perm.X])
        self.assertEqual(Perm.R.flagged, [Perm.R])
        self.assertEqual((Perm.R & Perm.X).flagged, [])

        self.assertEqual(len((Perm.R | Perm.W)), 2)
        self.assertEqual(len(Perm.RWX), 3)
        self.assertEqual(len(Perm.R), 1)
        self.assertEqual(len((Perm.R & Perm.X)), 0)

        self.assertEqual(Perm([]), Perm(0))
        self.assertEqual(Perm({}), Perm(0))
        self.assertEqual(Perm((item for item in [])), Perm(0))

        self.assertCountEqual([perm for perm in Perm.RWX], [Perm.R, Perm.W, Perm.X])

        self.assertCountEqual([perm for perm in (Perm.R | Perm.X)], [Perm.R, Perm.X])

        self.assertCountEqual([perm for perm in Perm.R], [Perm.R])

        self.assertCountEqual([perm for perm in (Perm.R & Perm.X)], [])

    def test_flag_def_order(self):
        from enum import IntFlag

        class PermNative(IntFlag):
            R = auto()
            W = auto()
            RW = R | W
            X = auto()
            RWX = R | W | X

        self.assertEqual(PermNative.R.value, 1)
        self.assertEqual(PermNative.W.value, 2)
        self.assertEqual(PermNative.RW.value, 3)
        self.assertEqual(PermNative.X.value, 4)
        self.assertEqual(PermNative.RWX.value, 7)

        class PermProperties(FlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            R = auto(), "read"
            W = auto(), "write"
            RW = R | W, "read/write"
            X = auto(), "execute"
            RWX = R | W | X, "all"

        self.assertEqual(PermProperties.R.value, 1)
        self.assertEqual(PermProperties.W.value, 2)
        self.assertEqual(PermProperties.RW.value, 3)
        self.assertEqual(PermProperties.X.value, 4)
        self.assertEqual(PermProperties.RWX.value, 7)

        self.assertEqual((PermProperties.R | PermProperties.W).label, "read/write")
        self.assertFalse(hasattr((PermProperties.W | PermProperties.X), "label"))
        self.assertFalse(hasattr((PermProperties.R | PermProperties.X), "label"))
        self.assertEqual(
            (PermProperties.R | PermProperties.W | PermProperties.X).label, "all"
        )
        self.assertEqual(PermProperties.R.label, "read")
        self.assertEqual(PermProperties.W.label, "write")

        self.assertEqual(PermProperties.RW, PermProperties("read/write"))
        self.assertEqual(PermProperties.RW, PermProperties(["read", "write"]))
        self.assertEqual(
            (PermProperties.W | PermProperties.X), PermProperties(["write", "execute"])
        )
        self.assertEqual(PermProperties.R, PermProperties("read"))
        self.assertEqual(PermProperties.W, PermProperties("write"))
        self.assertEqual(PermProperties.X, PermProperties("execute"))
        self.assertEqual(PermProperties.RWX, PermProperties("all"))

        class IntPermProperties(IntFlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            R = auto(), "read"
            W = auto(), "write"
            RW = R | W, "read/write"
            X = auto(), "execute"
            RWX = R | W | X, "all"

        self.assertEqual(IntPermProperties.R.value, 1)
        self.assertEqual(IntPermProperties.W.value, 2)
        self.assertEqual(IntPermProperties.RW.value, 3)
        self.assertEqual(IntPermProperties.X.value, 4)
        self.assertEqual(IntPermProperties.RWX.value, 7)

        self.assertEqual(
            (IntPermProperties.R | IntPermProperties.W).label, "read/write"
        )
        self.assertFalse(hasattr((IntPermProperties.W | IntPermProperties.X), "label"))
        self.assertFalse(hasattr((IntPermProperties.R | IntPermProperties.X), "label"))
        self.assertEqual(
            (IntPermProperties.R | IntPermProperties.W | IntPermProperties.X).label,
            "all",
        )
        self.assertEqual(IntPermProperties.R.label, "read")
        self.assertEqual(IntPermProperties.W.label, "write")

        self.assertEqual(IntPermProperties.RW, IntPermProperties("read/write"))
        self.assertEqual(IntPermProperties.RW, IntPermProperties(["read", "write"]))
        self.assertEqual(
            (IntPermProperties.W | IntPermProperties.X),
            IntPermProperties(["write", "execute"]),
        )
        self.assertEqual(IntPermProperties.R, IntPermProperties("read"))
        self.assertEqual(IntPermProperties.W, IntPermProperties("write"))
        self.assertEqual(IntPermProperties.X, IntPermProperties("execute"))
        self.assertEqual(IntPermProperties.RWX, IntPermProperties("all"))

    if sys.version_info >= (3, 11):  # pragma: no cover

        def test_flag_boundary_enum(self):
            """
            Test the boundary functionality introduced in 3.11
            """
            from enum import CONFORM, EJECT, KEEP, STRICT

            class StrictFlag(IntFlagProperties, boundary=STRICT):
                label: str

                RED = auto(), "red"
                GREEN = auto(), "green"
                BLUE = auto(), "blue"

            with self.assertRaises(ValueError):
                StrictFlag(2**2 + 2**4)

            self.assertEqual(StrictFlag.BLUE.label, "blue")
            self.assertEqual(StrictFlag.RED.label, "red")
            self.assertEqual(StrictFlag.GREEN.label, "green")
            self.assertFalse(hasattr((StrictFlag.BLUE | StrictFlag.RED), "label"))

            class ConformFlag(FlagProperties, boundary=CONFORM):
                label: Annotated[str, Symmetric()]

                RED = auto(), "red"
                GREEN = auto(), "green"
                BLUE = auto(), "blue"

            self.assertEqual(ConformFlag.BLUE, ConformFlag(2**2 + 2**4))
            self.assertEqual(ConformFlag(2**2 + 2**4).label, "blue")
            self.assertEqual(ConformFlag(2**2 + 2**4).label, ConformFlag("blue"))

            class EjectFlag(IntFlagProperties, boundary=EJECT):
                label: Annotated[str, Symmetric()]

                RED = auto(), "red"
                GREEN = auto(), "green"
                BLUE = auto(), "blue"

            self.assertEqual(EjectFlag(2**2 + 2**4), 20)
            self.assertFalse(hasattr(EjectFlag(2**2 + 2**4), "label"))
            self.assertEqual(EjectFlag.GREEN, EjectFlag("green"))
            self.assertEqual(
                (EjectFlag.GREEN | EjectFlag.BLUE), EjectFlag(["blue", "green"])
            )

            class KeepFlag(FlagProperties, boundary=KEEP):
                label: Annotated[str, Symmetric()]
                hex: int

                RED = auto(), "red", 0xFF0000
                GREEN = auto(), "green", 0x00FF00
                BLUE = auto(), "blue", 0x0000FF

            self.assertEqual(KeepFlag(2**2 + 2**4).value, 20)
            self.assertTrue(KeepFlag.BLUE in KeepFlag(2**2 + 2**4))
            self.assertFalse(hasattr(KeepFlag(2**2 + 2**4), "label"))
            self.assertEqual([flg.label for flg in KeepFlag(2**2 + 2**4)], ["blue"])

    if sys.version_info >= (3, 11):  # pragma: no cover

        def test_enum_verify(self):
            from enum import CONTINUOUS, NAMED_FLAGS, UNIQUE, verify

            with self.assertRaises(ValueError):

                @verify(UNIQUE)
                class Color(EnumProperties):
                    label: Annotated[str, Symmetric()]

                    RED = 1, "red"
                    GREEN = 2, "green"
                    BLUE = 3, "blue"
                    CRIMSON = 1, "crimson"

            @verify(UNIQUE)
            class Color(EnumProperties):
                label: str

                RED = 1, "red"
                GREEN = 2, "green"
                BLUE = 3, "blue"
                CRIMSON = 4, "crimson"

            self.assertEqual(Color.GREEN.label, "green")
            self.assertEqual(Color.CRIMSON.label, "crimson")

            with self.assertRaises(ValueError):
                # this throws an error if label is symmetric!
                @verify(UNIQUE)
                class Color(EnumProperties):
                    label: Annotated[str, Symmetric()]

                    RED = 1, "red"
                    GREEN = 2, "green"
                    BLUE = 3, "blue"
                    CRIMSON = 4, "crimson"

            with self.assertRaises(ValueError):

                @verify(CONTINUOUS)
                class Color(IntEnumProperties):
                    label: Annotated[str, Symmetric()]

                    RED = 1, "red"
                    GREEN = 2, "green"
                    BLUE = 5, "blue"

            @verify(CONTINUOUS)
            class Color(IntEnumProperties):
                label: Annotated[str, Symmetric()]

                RED = 1, "red"
                GREEN = 2, "green"
                BLUE = 3, "blue"

            self.assertEqual(Color.BLUE.label, "blue")
            self.assertEqual(Color.RED, Color("red"))

            with self.assertRaises(ValueError):

                @verify(NAMED_FLAGS)
                class Color(IntFlagProperties):
                    label: Annotated[str, Symmetric()]

                    RED = 1, "red"
                    GREEN = 2, "green"
                    BLUE = 4, "blue"
                    WHITE = 15, "white"
                    NEON = 31, "neon"

            @verify(NAMED_FLAGS)
            class Color(IntFlagProperties):
                label: Annotated[str, Symmetric()]

                RED = 1, "red"
                GREEN = 2, "green"
                BLUE = 4, "blue"
                WHITE = 16, "white"
                NEON = 32, "neon"

            self.assertEqual(Color.BLUE | Color.NEON, Color(["blue", "neon"]))

    if sys.version_info >= (3, 11):  # pragma: no cover

        def test_enum_property(self):
            from enum import property as enum_property

            class Color(EnumProperties):
                label: Annotated[str, Symmetric()]

                RED = 1, "red"
                GREEN = 2, "green"
                BLUE = 3, "blue"

                @enum_property
                def blue(self):
                    return "whatever"

            self.assertEqual(Color.BLUE.blue, "whatever")

            # attempting to assign an enum_property to a class as an existing
            # property name should raise an AttributeError
            with self.assertRaises(AttributeError):

                class Color(EnumProperties):
                    label: Annotated[str, Symmetric()]

                    RED = 1, "red"
                    GREEN = 2, "green"
                    BLUE = 3, "blue"

                    @enum_property
                    def label(self):
                        return "label"

    if sys.version_info >= (3, 12):  # pragma: no cover

        def test_enum_dataclass_support(self):
            """
            In 3.12, Enum added support for dataclass inheritance which offers similar functionality
            to enum-properties. This tests evaluates how these step on each other's toes.

            From the std lib docs example:
            """
            from dataclasses import dataclass, field

            @dataclass
            class CreatureDataMixin:
                size: str
                legs: int
                tail: bool = field(repr=False, default=True)

            @dataclass(eq=True, frozen=True)
            class CreatureDataHashableMixin:
                size: str
                legs: int
                tail: bool = field(repr=False, default=True)

            class CreatureHybrid(CreatureDataMixin, EnumProperties):
                kingdom: Annotated[str, Symmetric()]

                BEETLE = "small", 6, False, "insect"
                DOG = (
                    (
                        "medium",
                        4,
                    ),
                    "mammal",
                )

            self.assertEqual(CreatureHybrid.BEETLE.size, "small")
            self.assertEqual(CreatureHybrid.BEETLE.legs, 6)
            self.assertEqual(CreatureHybrid.BEETLE.tail, False)
            self.assertEqual(CreatureHybrid.BEETLE.kingdom, "insect")

            self.assertEqual(CreatureHybrid.DOG.size, "medium")
            self.assertEqual(CreatureHybrid.DOG.legs, 4)
            self.assertEqual(CreatureHybrid.DOG.tail, True)
            self.assertEqual(CreatureHybrid.DOG.kingdom, "mammal")

            self.assertEqual(CreatureHybrid("mammal"), CreatureHybrid.DOG)
            self.assertEqual(CreatureHybrid("insect"), CreatureHybrid.BEETLE)

            class CreatureHybridSpecialized(CreatureDataMixin, EnumProperties):
                kingdom: Annotated[str, Symmetric()]

                BEETLE = "small", 6, "insect"
                DOG = ("medium", 4, False), "mammal"

                @specialize(BEETLE)
                def function(self):
                    return "function(beetle)"

                @specialize(DOG)
                def function(self):
                    return "function(dog)"

            self.assertEqual(CreatureHybridSpecialized.BEETLE.size, "small")
            self.assertEqual(CreatureHybridSpecialized.BEETLE.legs, 6)
            self.assertEqual(CreatureHybridSpecialized.BEETLE.tail, True)
            self.assertEqual(CreatureHybridSpecialized.BEETLE.kingdom, "insect")

            self.assertEqual(CreatureHybridSpecialized.DOG.size, "medium")
            self.assertEqual(CreatureHybridSpecialized.DOG.legs, 4)
            self.assertEqual(CreatureHybridSpecialized.DOG.tail, False)
            self.assertEqual(CreatureHybridSpecialized.DOG.kingdom, "mammal")

            self.assertEqual(
                CreatureHybridSpecialized("mammal"), CreatureHybridSpecialized.DOG
            )
            self.assertEqual(
                CreatureHybridSpecialized("insect"), CreatureHybridSpecialized.BEETLE
            )

            self.assertEqual(CreatureHybridSpecialized.DOG.function(), "function(dog)")
            self.assertEqual(
                CreatureHybridSpecialized.BEETLE.function(), "function(beetle)"
            )

            class CreatureHybridSpecialized(CreatureDataHashableMixin, EnumProperties):
                kingdom: Annotated[str, Symmetric()]

                BEETLE = "small", 6, "insect"
                DOG = (
                    (
                        "medium",
                        4,
                    ),
                    "mammal",
                )

                @specialize(BEETLE)
                def function(self):
                    return "function(beetle)"

                @specialize(DOG)
                def function(self):
                    return "function(dog)"

            self.assertEqual(CreatureHybridSpecialized.BEETLE.size, "small")
            self.assertEqual(CreatureHybridSpecialized.BEETLE.legs, 6)
            self.assertEqual(CreatureHybridSpecialized.BEETLE.tail, True)
            self.assertEqual(CreatureHybridSpecialized.BEETLE.kingdom, "insect")

            self.assertEqual(CreatureHybridSpecialized.DOG.size, "medium")
            self.assertEqual(CreatureHybridSpecialized.DOG.legs, 4)
            self.assertEqual(CreatureHybridSpecialized.DOG.tail, True)
            self.assertEqual(CreatureHybridSpecialized.DOG.kingdom, "mammal")

            self.assertEqual(
                CreatureHybridSpecialized("mammal"), CreatureHybridSpecialized.DOG
            )
            self.assertEqual(
                CreatureHybridSpecialized("insect"), CreatureHybridSpecialized.BEETLE
            )

            self.assertEqual(CreatureHybridSpecialized.DOG.function(), "function(dog)")
            self.assertEqual(
                CreatureHybridSpecialized.BEETLE.function(), "function(beetle)"
            )


class TestGiantFlags(TestCase):
    def test_over64_flags(self):
        class BigFlags(IntFlagProperties):
            label: str

            ONE = 2**0, "one"
            MIDDLE = 2**64, "middle"
            MIXED = ONE | MIDDLE, "mixed"
            LAST = 2**128, "last"

        self.assertEqual((BigFlags.ONE | BigFlags.LAST).value, 2**128 + 1)
        self.assertEqual((BigFlags.MIDDLE | BigFlags.LAST).value, 2**128 + 2**64)
        self.assertEqual((BigFlags.MIDDLE | BigFlags.ONE).label, "mixed")
