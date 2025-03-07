import typing as t
from enum_properties import EnumProperties, Symmetric
from enum import verify, UNIQUE


@verify(UNIQUE)
class Color(EnumProperties):

    label: t.Annotated[str, Symmetric()]

    RED = 1, 'red'
    GREEN = 2, 'green'
    BLUE = 3, 'blue'

# ValueError: aliases found in <enum 'Color'>: blue -> BLUE,
# green -> GREEN, red -> RED
