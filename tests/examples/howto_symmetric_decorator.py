import typing as t
from enum import auto
from enum_properties import EnumProperties, symmetric


class Color(EnumProperties):

    rgb: t.Tuple[int, int, int]
    hex: str

    # name   value      rgb       hex
    RED    = auto(), (1, 0, 0), 'ff0000'
    GREEN  = auto(), (0, 1, 0), '00ff00'
    BLUE   = auto(), (0, 0, 1), '0000ff'

    @symmetric()
    @property
    def integer(self) -> int:
        return int(self.hex, 16)

    @symmetric()
    @property
    def binary(self) -> str:
        return bin(self.integer)[2:]


# now we can do this:
assert Color(Color.RED.binary) is Color.RED
assert Color(Color.RED.integer) is Color.RED
