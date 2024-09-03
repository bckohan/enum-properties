from unittest import TestCase
from typing_extensions import Annotated

from enum_properties import Symmetric


class TestInterfaceEquivalency(TestCase):
    """
    Enums should hash the same as their values.
    """

    def test_hashing_example(self):
        from enum import Enum

        from enum_properties import EnumPropertiesMeta, SymmetricMixin

        class Color(
            SymmetricMixin,
            tuple,
            Enum,
            metaclass=EnumPropertiesMeta,
        ):
            hex: Annotated[str, Symmetric(case_fold=True)]

            # name   value      rgb       hex
            RED = (1, 0, 0), "0xff0000"
            GREEN = (0, 1, 0), "0x00ff00"
            BLUE = (0, 0, 1), "0x0000ff"

            def __hash__(self):
                return tuple.__hash__(self)

        assert {(1, 0, 0): "Found me!"}[Color.RED] == "Found me!"
