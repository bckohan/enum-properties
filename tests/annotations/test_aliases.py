import sys
import enum
from unittest import TestCase
from typing import Annotated

from enum_properties import (
    EnumProperties,
    FlagProperties,
    Symmetric,
    specialize,
    symmetric,
)


class TestAliases(TestCase):
    def test_enum_alias(self):
        class EnumWithAliases(EnumProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            A = 1, "a"
            B = 2, "b"
            C = 3, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

        self.assertEqual(
            EnumWithAliases.__first_class_members__, ["A", "B", "C", "X", "Y", "Z"]
        )

        class EnumWithAliasesComplex(EnumProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            A = 1, "a"
            B = 2, "b"
            C = 3, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

            @symmetric(case_fold=True)
            def x3(self) -> str:
                return self.label * 3

            @property
            def prop(self) -> str:
                return self.label * 5

            def method(self) -> str:
                return self.label * 7

            @specialize(A)
            def method(self) -> str:
                return self.label * 8

            if sys.version_info[:2] >= (3, 11):

                @enum.nonmember
                class Nested:
                    pass
            else:

                class Nested:
                    pass

        self.assertEqual(
            EnumWithAliasesComplex.__first_class_members__,
            ["A", "B", "C", "X", "Y", "Z"],
        )

        class EnumWithAliasesOverride1(EnumProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            A = 1, "a"
            B = 2, "b"
            C = 3, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

            __first_class_members__ = ["A", "B", "C", "X", "Y"]

        self.assertEqual(
            EnumWithAliasesOverride1.__first_class_members__, ["A", "B", "C", "X", "Y"]
        )

        class EnumWithAliasesOverride2(EnumProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            __first_class_members__ = ["A", "B", "C", "X"]

            A = 1, "a"
            B = 2, "b"
            C = 3, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

        self.assertEqual(
            EnumWithAliasesOverride2.__first_class_members__, ["A", "B", "C", "X"]
        )

    def test_flag_alias(self):
        class FlagWithAliases(FlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

            AB = A | B, "ab"
            AC = A | C, "ac"
            BC = B | C, "bc"
            ABC = A | B | C, "abc"

        self.assertEqual(
            FlagWithAliases.__first_class_members__,
            ["A", "B", "C", "X", "Y", "Z", "AB", "AC", "BC", "ABC"],
        )

        class FlagWithAliasesComplex(FlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

            AB = A | B, "ab"
            AC = A | C, "ac"
            BC = B | C, "bc"
            ABC = A | B | C, "abc"

            @symmetric(case_fold=True)
            def x3(self) -> str:
                return self.label * 3

            @property
            def prop(self) -> str:
                return self.label * 5

            def method(self) -> str:
                return self.label * 7

            @specialize(A)
            def method(self) -> str:
                return self.label * 8

            if sys.version_info[:2] >= (3, 11):

                @enum.nonmember
                class Nested:
                    pass
            else:

                class Nested:
                    pass

        self.assertEqual(
            FlagWithAliasesComplex.__first_class_members__,
            ["A", "B", "C", "X", "Y", "Z", "AB", "AC", "BC", "ABC"],
        )

        class FlagWithAliasesOverride1(FlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            __first_class_members__ = ["A", "B", "C", "X", "Y", "ABC"]

            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

            AB = A | B, "ab"
            AC = A | C, "ac"
            BC = B | C, "bc"
            ABC = A | B | C, "abc"

        self.assertEqual(
            FlagWithAliasesOverride1.__first_class_members__,
            ["A", "B", "C", "X", "Y", "ABC"],
        )

        class FlagWithAliasesOverride2(FlagProperties):
            label: Annotated[str, Symmetric(case_fold=True)]

            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"
            X = C, "x"
            Y = B, "y"
            Z = A, "z"

            AB = A | B, "ab"
            AC = A | C, "ac"
            BC = B | C, "bc"
            ABC = A | B | C, "abc"

            __first_class_members__ = ["A", "B", "C", "X", "Y", "ABC"]

        self.assertEqual(
            FlagWithAliasesOverride2.__first_class_members__,
            ["A", "B", "C", "X", "Y", "ABC"],
        )
