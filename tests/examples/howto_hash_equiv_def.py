import typing as t
from enum_properties import EnumPropertiesMeta, SymmetricMixin, Symmetric
from enum import Enum


class Color(
    SymmetricMixin,
    tuple,
    Enum,
    metaclass=EnumPropertiesMeta
):
    hex: t.Annotated[str, Symmetric(case_fold=True)]

    # name   value (rgb)    hex
    RED    = (1, 0, 0), '0xff0000'
    GREEN  = (0, 1, 0), '0x00ff00'
    BLUE   = (0, 0, 1), '0x0000ff'

    def __hash__(self):  # you must add this!
        return tuple.__hash__(self)


assert {(1, 0, 0): 'Found me!'}[Color.RED] == 'Found me!'
