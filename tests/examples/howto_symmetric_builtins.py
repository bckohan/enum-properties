import typing as t
from enum import auto
from enum_properties import EnumProperties, Symmetric


class Color(EnumProperties):

    name: t.Annotated[str, Symmetric(case_fold=True)]
    rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
    hex: t.Annotated[str, Symmetric(case_fold=True)]

    # name   value      rgb       hex
    RED    = auto(), (1, 0, 0), 'ff0000'
    GREEN  = auto(), (0, 1, 0), '00ff00'
    BLUE   = auto(), (0, 0, 1), '0000ff'


# now we can do this:
assert Color('red') is Color.RED
