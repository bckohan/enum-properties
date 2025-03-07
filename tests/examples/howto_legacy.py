from enum_properties import EnumProperties, p
from enum import auto


class Color(EnumProperties, p('rgb'), p('hex')):

    extra: int  # this does not become a property

    # name   value      rgb       hex
    RED    = auto(), (1, 0, 0), 'ff0000'
    GREEN  = auto(), (0, 1, 0), '00ff00'
    BLUE   = auto(), (0, 0, 1), '0000ff'
