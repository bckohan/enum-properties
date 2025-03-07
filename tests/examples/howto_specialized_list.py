from enum_properties import EnumProperties, specialize


class SpecializedEnum(EnumProperties):

    ONE   = 1
    TWO   = 2
    THREE = 3

    @specialize(TWO, THREE)
    def method(self):
        return 'shared()'

assert not hasattr(SpecializedEnum.ONE, 'method')
assert SpecializedEnum.TWO.method() == 'shared()'
assert SpecializedEnum.THREE.method() == 'shared()'
