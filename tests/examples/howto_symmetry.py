import typing as t
from enum_properties import EnumProperties, Symmetric
from enum import auto


class Color(EnumProperties):

    rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
    hex: t.Annotated[str, Symmetric(case_fold=True)]

    # name   value      rgb       hex
    RED    = auto(), (1, 0, 0), '0xff0000'
    GREEN  = auto(), (0, 1, 0), '0x00ff00'
    BLUE   = auto(), (0, 0, 1), '0x0000ff'


assert Color.RED is Color((1, 0, 0)) is Color('0xFF0000') is Color('0xff0000')


# str(hex(16711680)) == '0xff0000'
assert Color.RED is Color(hex(16711680)) == hex(16711680)
assert Color.RED == (1, 0, 0)
assert Color.RED != (0, 1, 0)
assert Color.RED == '0xFF0000'
