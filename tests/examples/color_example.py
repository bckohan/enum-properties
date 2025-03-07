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

# the type hints on the Enum class become properties on
# each value, matching the order in which they are specified


assert Color.RED.rgb   == (1, 0, 0)
assert Color.GREEN.rgb == (0, 1, 0)
assert Color.BLUE.rgb  == (0, 0, 1)

assert Color.RED.hex   == 'ff0000'
assert Color.GREEN.hex == '00ff00'
assert Color.BLUE.hex  == '0000ff'
