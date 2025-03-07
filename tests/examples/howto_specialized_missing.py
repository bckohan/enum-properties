from enum_properties import EnumProperties, specialize


class SpecializedEnum(EnumProperties):

    ONE   = 1
    TWO   = 2
    THREE = 3

    @specialize(THREE)
    def method(self):
        return 'method_three()'

assert not hasattr(SpecializedEnum.ONE, 'method')
assert not hasattr(SpecializedEnum.TWO, 'method')
assert SpecializedEnum.THREE.method() == 'method_three()'
