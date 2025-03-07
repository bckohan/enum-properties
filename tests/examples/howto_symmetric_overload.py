import typing as t
from enum_properties import IntEnumProperties, Symmetric


class PriorityEx(IntEnumProperties):

    prop1: t.Annotated[str, Symmetric()]
    prop2: t.Annotated[t.List[int | str], Symmetric(case_fold=True)]

    # <-------- Higher Precedence
    # name  value   prop1     prop2    #  ^
    ONE     = 0,     '1',    [3, 4]    #  |
    TWO     = 1,     '2',    [3, '4']  #  Higher
    THREE   = 2,     '3',    [3, 4]    #  Precedence


assert PriorityEx(0)   is PriorityEx.ONE   # order left to right
assert PriorityEx('1') is PriorityEx.ONE   # type specificity
assert PriorityEx(3)   is PriorityEx.ONE   # type specificity/order
assert PriorityEx('3') is PriorityEx.THREE # type specificity
assert PriorityEx(4)   is PriorityEx.ONE   # order left to right
assert PriorityEx('4') is PriorityEx.TWO   # type specificity
