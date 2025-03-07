import typing as t
import enum
from enum_properties import EnumPropertiesMeta, SymmetricMixin, Symmetric


class Perm(
    SymmetricMixin,
    enum.IntFlag,
    metaclass=EnumPropertiesMeta
):
    label: t.Annotated[str, Symmetric(case_fold=True)]

    R = 1, 'read'
    W = 2, 'write'
    X = 4, 'execute'
    RWX = 7, 'all'


assert (Perm.R | Perm.W).flagged == [Perm.R, Perm.W]
