import typing as t
from enum_properties import IntFlagProperties, Symmetric
from enum import STRICT


class Perm(IntFlagProperties, boundary=STRICT):

    label: t.Annotated[str, Symmetric(case_fold=True)]

    R = 1, 'read'
    W = 2, 'write'
    X = 4, 'execute'
    RWX = 7, 'all'


Perm(8)  # raises ValueError
