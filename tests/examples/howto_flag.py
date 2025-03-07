import typing as t
from enum_properties import IntFlagProperties, Symmetric

class Perm(IntFlagProperties):

    label: t.Annotated[str, Symmetric(case_fold=True)]

    R = 1, 'read'
    W = 2, 'write'
    X = 4, 'execute'
    RWX = 7, 'all'


# properties for combined flags, that are not listed will not exist
assert not hasattr((Perm.R | Perm.W), "label")

# but combined flags can be specified and given properties
assert (Perm.R | Perm.W | Perm.X) is Perm.RWX
assert (Perm.R | Perm.W | Perm.X).label == 'all'

# list the active flags:
assert (Perm.R | Perm.W).flagged == [Perm.R, Perm.W]
assert (Perm.R | Perm.W | Perm.X).flagged == [Perm.R, Perm.W, Perm.X]


assert Perm([Perm.R, Perm.W, Perm.X]) is Perm.RWX
assert Perm({'read', 'write', 'execute'}) is Perm.RWX
assert Perm(perm for perm in (1, 'write', Perm.X)) is Perm.RWX

# iterate through active flags
assert [perm for perm in Perm.RWX] == [Perm.R, Perm.W, Perm.X]

# flagged property returns list of flags
assert (Perm.R | Perm.W).flagged == [Perm.R, Perm.W]

# instantiate a Flag off an empty iterable
assert Perm(0) == Perm([])

# check number of active flags:
assert len(Perm(0)) == 0
assert len(Perm.RWX) == 3
assert len(Perm.R | Perm.X) == 2
assert len(Perm.R & Perm.X) == 0
