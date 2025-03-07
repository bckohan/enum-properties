from enum import IntEnum


class MyIntEnum(IntEnum):

    ONE = 1
    TWO = 2
    THREE = 3


assert {1: 'Found me!'}[MyIntEnum.ONE] == 'Found me!'
