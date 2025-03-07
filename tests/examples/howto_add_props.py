import typing as t
from enum_properties import EnumProperties
from enum import auto


class Color(EnumProperties):

    rgb: t.Tuple[int, int, int]
    hex: str

    # name   value      rgb       hex
    RED    = auto(), (1, 0, 0), 'ff0000'
    GREEN  = auto(), (0, 1, 0), '00ff00'
    BLUE   = auto(), (0, 0, 1), '0000ff'


# The property values are accessible by name on the enumeration values:
assert Color.RED.hex == 'ff0000'
