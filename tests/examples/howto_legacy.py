from enum_properties import EnumProperties, p, s
from enum import auto


# we use p and s values to define properties in the order they appear in the value tuple
class Color(EnumProperties, p('rgb'), s('hex')):

    extra: int  # this does not become a property

    # non-value tuple properties are marked symmetric using the _symmetric_builtins_
    # class attribute
    _symmetric_builtins_ = [s("name", case_fold=True), "binary"]

    # name   value      rgb       hex
    RED    = auto(), (1, 0, 0), 'ff0000'
    GREEN  = auto(), (0, 1, 0), '00ff00'
    BLUE   = auto(), (0, 0, 1), '0000ff'

    @property
    def binary(self) -> str:
        return bin(int(self.hex, 16))[2:]


assert Color('red') is Color.RED
assert Color('111111110000000000000000') is Color.RED

assert Color.RED.rgb == (1, 0, 0)
assert Color.RED.hex == 'ff0000'
assert Color.RED.binary == '111111110000000000000000'
