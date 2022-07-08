from django.db import models
from django_enum import EnumField
from django_enum.tests.app1.enums import *


class EnumTester(models.Model):

    small_pos_int = EnumField(SmallPosIntEnum, null=True, default=None)
    small_int = EnumField(SmallIntEnum, null=False, default=SmallIntEnum.VAL3)

    pos_int = EnumField(PosIntEnum, default=PosIntEnum.VAL3)
    int = EnumField(IntEnum, null=True)

    big_pos_int = EnumField(BigPosIntEnum, null=True, default=None)
    big_int = EnumField(BigIntEnum, default=BigIntEnum.VAL0)

    constant = EnumField(Constants, null=True, default=None)

    text = EnumField(TextEnum, null=True, default=None)
