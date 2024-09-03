from enum import auto
import typing as t
from typing_extensions import Annotated
from enum_properties import EnumProperties, FlagProperties, IntFlagProperties, Symmetric


class IntPerm(IntFlagProperties):
    label: Annotated[str, Symmetric(case_fold=True)]

    R = 1, "read"
    W = 2, "write"
    X = 4, "execute"
    RWX = 7, "all"


class Perm(FlagProperties):
    label: Annotated[str, Symmetric(case_fold=True)]

    R = auto(), "read"
    W = auto(), "write"
    X = auto(), "execute"
    RWX = R | W | X, "all"


class PriorityEx(EnumProperties):
    prop1: Annotated[str, Symmetric()]
    prop2: Annotated[str, Symmetric(case_fold=True)]

    ONE = 0, "1", [3, 4]
    TWO = 1, "2", [3, "4"]
    THREE = 2, "3", [3, 4]


class Color(EnumProperties):
    rgb: t.Tuple[int, int, int]
    hex: str

    RED = auto(), (1, 0, 0), "ff0000"
    GREEN = auto(), (0, 1, 0), "00ff00"
    BLUE = auto(), (0, 0, 1), "0000ff"
