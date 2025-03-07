from enum_properties import EnumProperties


class MyEnum(EnumProperties):

    label: str

    class Type1:
        pass

    class Type2:
        pass

    class Type3:
        pass

    VALUE1 = Type1, 'label1'
    VALUE2 = Type2, 'label2'
    VALUE3 = Type3, 'label3'


# only the expected values become enumeration values
assert MyEnum.Type1 == MyEnum.VALUE1.value
assert MyEnum.Type2 == MyEnum.VALUE2.value
assert MyEnum.Type3 == MyEnum.VALUE3.value
assert len(MyEnum) == 3

# nested classes behave as expected
assert MyEnum.Type1().__class__ is MyEnum.Type1
assert MyEnum.Type2().__class__ is MyEnum.Type2
assert MyEnum.Type3().__class__ is MyEnum.Type3
