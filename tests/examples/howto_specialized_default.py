from enum_properties import EnumProperties, specialize


class SpecializedEnum(EnumProperties):

    ONE   = 1
    TWO   = 2
    THREE = 3

    def method(self):
        return 'generic()'

    @specialize(THREE)
    def method(self):
        return 'method_three()'


assert SpecializedEnum.ONE.method() == 'generic()'
assert SpecializedEnum.TWO.method() == 'generic()'
assert SpecializedEnum.THREE.method() == 'method_three()'
