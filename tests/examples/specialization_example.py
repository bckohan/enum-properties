from enum_properties import EnumProperties as Enum, specialize


class SpecializedEnum(Enum):

    ONE   = 1
    TWO   = 2
    THREE = 3

    @specialize(ONE)
    def method(self):
        return 'method_one()'

    @specialize(TWO)
    def method(self):
        return 'method_two()'

    @specialize(THREE)
    def method(self):
        return 'method_three()'

assert SpecializedEnum.ONE.method() == 'method_one()'
assert SpecializedEnum.TWO.method() == 'method_two()'
assert SpecializedEnum.THREE.method() == 'method_three()'
