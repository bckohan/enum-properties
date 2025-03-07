import typing as t
from enum_properties import EnumProperties, Symmetric
from enum import auto


class Color(EnumProperties):

    rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
    hex: t.Annotated[str, Symmetric(case_fold=True)]

    RED    = auto(), (1, 0, 0), 'ff0000'
    GREEN  = auto(), (0, 1, 0), '00ff00'
    BLUE   = auto(), (0, 0, 1), '0000ff'

# Enumeration instances may be instantiated from any Symmetric property
# values. Use case_fold for case insensitive matching


assert Color((1, 0, 0)) is Color.RED
assert Color((0, 1, 0)) is Color.GREEN
assert Color((0, 0, 1)) is Color.BLUE

assert Color('ff0000') is Color.RED
assert Color('FF0000') is Color.RED  # case_fold makes mapping case insensitive
assert Color('00ff00') is Color.GREEN
assert Color('00FF00') is Color.GREEN
assert Color('0000ff') is Color.BLUE
assert Color('0000FF') is Color.BLUE

assert Color.RED.hex == 'ff0000'
