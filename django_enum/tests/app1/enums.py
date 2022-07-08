from django_enum import (
    TextChoices,
    IntegerChoices,
    FloatChoices,
    p
)
from django.utils.translation import gettext as _


class TextEnum(TextChoices, p('version'), p('help'), p('aliases', symmetric=True, case_sensitive=False)):

    VALUE1 = 'V1', 'Value1', 0, _('Some help text about value1.'), ['val1', 'v1', 'v one']
    VALUE2 = 'V22', 'Value2', 1, _('Some help text about value2.'), {'val22', 'v2', 'v two'}
    VALUE3 = 'V333', 'Value3', 2, _('Some help text about value3.'), ['val333', 'v3', 'v three']
    DEFAULT = 'D', 'Default', 3, _('Some help text about default.'), {'default', 'defacto', 'none'}


class Constants(FloatChoices, p('symbol', symmetric=True)):

    PI = 3.14159265358979323846264338327950288, 'Pi', 'π'
    e = 2.71828, "Euler's Number", 'e'
    GOLDEN_RATIO = 1.61803398874989484820458683436563811, 'Golden Ratio', 'φ'


class SmallPosIntEnum(IntegerChoices):

    VAL1 = 0, 'Value 1'
    VAL2 = 2, 'Value 2'
    VAL3 = 32767, 'Value 32767'


class SmallIntEnum(IntegerChoices):

    VALn1 = -32768, 'Value -32768'
    VAL0 = 0, 'Value 0'
    VAL1 = 1, 'Value 1'
    VAL2 = 2, 'Value 2'
    VAL3 = 32767, 'Value 32767'


class IntEnum(IntegerChoices):

    VALn1 = -2147483648, 'Value -2147483648'
    VAL0 = 0, 'Value 0'
    VAL1 = 1, 'Value 1'
    VAL2 = 2, 'Value 2'
    VAL3 = 2147483647, 'Value 2147483647'


class PosIntEnum(IntegerChoices):

    VAL0 = 0, 'Value 0'
    VAL1 = 1, 'Value 1'
    VAL2 = 2, 'Value 2'
    VAL3 = 2147483647, 'Value 2147483647'


class BigPosIntEnum(IntegerChoices):

    VAL0 = 0, 'Value 0'
    VAL1 = 1, 'Value 1'
    VAL2 = 2, 'Value 2'
    VAL3 = 2147483648, 'Value 2147483647'


class BigIntEnum(IntegerChoices, p('pos', symmetric=True), p('help')):

    VAL0 = -2147483649, 'Value -2147483649', BigPosIntEnum.VAL0, _('One less than the least regular integer.')
    VAL1 = 1, 'Value 1', BigPosIntEnum.VAL1, _('Something in the middle.')
    VAL2 = 2, 'Value 2', BigPosIntEnum.VAL2, _('Something in the middle.')
    VAL3 = 2147483648, 'Value 2147483647', BigPosIntEnum.VAL3, _('One more than the greatest regular integer.')


class PrecedenceTest(
    IntegerChoices,
    p('prop1', symmetric=True),
    p('prop2', symmetric=True),
    p('prop3', symmetric=True, case_sensitive=True),
    p('prop4', symmetric=True, case_sensitive=False)
):
    P1 = 0, 'Precedence 1', 3, 0.1, _('First'), ['0.4', 'Fourth', 1]
    P2 = 1, 'Precedence 2', 2, 0.2, _('Second'), {'0.3', 'Third', 2}
    P3 = 2, 'Precedence 3', '1', 0.3, _('Third'), [0.2, 'Second', 3]
    P4 = 3, 'Precedence 4', 0, 0.4, _('Fourth'), {0.1, 'First', 4}
