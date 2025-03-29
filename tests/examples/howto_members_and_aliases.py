import typing as t
from enum_properties import EnumProperties, Symmetric


class MyEnum(EnumProperties):

    label: t.Annotated[str, Symmetric()]

    A = 1, "a"
    B = 2, "b"
    C = 3, "c"
    ALIAS_TO_A = A, "a"


# __first_class_members__ contains members and aliases
assert MyEnum.__first_class_members__ == ["A", "B", "C", "ALIAS_TO_A"]

# __members__ contains all members, including aliases and symmetric aliases
assert set(MyEnum.__members__.keys()) == {"A", "B", "C", "ALIAS_TO_A", "a", "b", "c"}

# iterating contains only non-alias members
assert list(MyEnum) == [MyEnum.A, MyEnum.B, MyEnum.C]
