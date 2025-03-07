from enum_properties import EnumProperties
from enum import nonmember, member


class MyEnum(EnumProperties):

    @nonmember
    class Type1:
        pass

    @nonmember
    class Type2:
        pass

    @nonmember
    class Type3:
        pass

    label: str

    VALUE1 = member(Type1), 'label1'
    VALUE2 = member(Type2), 'label2'
    VALUE3 = member(Type3), 'label3'


# only the expected values become enumeration values
assert MyEnum.Type1 == MyEnum.VALUE1
assert MyEnum.Type2 == MyEnum.VALUE2
assert MyEnum.Type3 == MyEnum.VALUE3
assert len(MyEnum) == 3, len(MyEnum)

# nested classes behave as expected
assert MyEnum.Type1().__class__ is MyEnum.Type1
assert MyEnum.Type2().__class__ is MyEnum.Type2
assert MyEnum.Type3().__class__ is MyEnum.Type3
