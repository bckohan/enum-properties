from enum import auto

from enum_properties import EnumProperties, FlagProperties, IntFlagProperties, p, s


class IntPerm(
    IntFlagProperties,
    s("label", case_fold=True),
):
    R = 1, "read"
    W = 2, "write"
    X = 4, "execute"
    RWX = 7, "all"


class Perm(
    FlagProperties,
    s("label", case_fold=True),
):
    R = auto(), "read"
    W = auto(), "write"
    X = auto(), "execute"
    RWX = R | W | X, "all"


class PriorityEx(EnumProperties, s("prop1"), s("prop2", case_fold=True)):
    ONE = 0, "1", [3, 4]
    TWO = 1, "2", [3, "4"]
    THREE = 2, "3", [3, 4]


class Color(EnumProperties, p("rgb"), p("hex")):
    RED = auto(), (1, 0, 0), "ff0000"
    GREEN = auto(), (0, 1, 0), "00ff00"
    BLUE = auto(), (0, 0, 1), "0000ff"
