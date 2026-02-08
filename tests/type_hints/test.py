from __future__ import annotations

from enum import Enum, Flag, IntEnum, IntFlag, StrEnum
from typing import TYPE_CHECKING, Any, Literal
from types import MappingProxyType

try:
    # Py 3.11+
    from typing import assert_type
except ImportError:  # pragma: no cover
    # Py 3.10
    from typing_extensions import assert_type

from enum_properties import (
    EnumProperties,
    FlagProperties,
    IntEnumProperties,
    IntFlagProperties,
    StrEnumProperties,
)


def test() -> None:
    # ------------------------------------------------------------------ Enum
    class EnumTest(Enum):
        A = 1
        B = 2
        C = 3

    class EnumPropertiesTest(EnumProperties):
        A = 1
        B = 2
        C = 3

    # runtime
    _0: list[Enum] = [m for m in EnumTest]
    _1: list[Enum] = [m for m in EnumPropertiesTest]
    assert _0 and _1
    assert 1 in EnumTest
    assert 1 in EnumPropertiesTest
    assert EnumTest["A"] is EnumTest.A
    assert EnumPropertiesTest["A"] is EnumPropertiesTest.A
    assert EnumTest(1) is EnumTest.A
    assert EnumPropertiesTest(1) is EnumPropertiesTest.A

    # type-check probes
    assert_type(EnumTest.A, Literal[EnumTest.A])
    assert_type(EnumPropertiesTest.A, Literal[EnumPropertiesTest.A])
    assert_type(EnumTest["A"], Literal[EnumTest.A])
    assert_type(EnumPropertiesTest["A"], Literal[EnumPropertiesTest.A])
    assert_type(EnumTest(1), EnumTest)
    assert_type(EnumPropertiesTest(1), EnumPropertiesTest)
    assert_type(EnumTest.A.name, Literal["A"])
    assert_type(EnumPropertiesTest.A.name, Literal["A"])
    assert_type(EnumTest.A.value, Literal[1])
    assert_type(EnumPropertiesTest.A.value, Literal[1])
    assert_type(list(EnumTest), list[EnumTest])
    assert_type(list(EnumPropertiesTest), list[EnumPropertiesTest])
    assert_type(EnumTest.__members__, MappingProxyType[str, EnumTest])
    assert_type(
        EnumPropertiesTest.__members__, MappingProxyType[str, EnumPropertiesTest]
    )

    # --------------------------------------------------------------- StrEnum
    class StrEnumTest(StrEnum):
        A = "a"
        B = "b"
        C = "c"

    class StrEnumPropertiesTest(StrEnumProperties):
        A = "a"
        B = "b"
        C = "c"

    # runtime
    _2: list[str] = [m for m in StrEnumTest]
    _3: list[str] = [m for m in StrEnumPropertiesTest]
    _2r: list[Any] = [m for m in reversed(StrEnumTest)]
    _3r: list[Any] = [m for m in reversed(StrEnumPropertiesTest)]
    assert _2 and _3
    assert "a" in StrEnumTest
    assert "a" in StrEnumPropertiesTest
    _2a: StrEnumTest = StrEnumTest["A"]
    _3a: StrEnumPropertiesTest = StrEnumPropertiesTest["A"]
    assert StrEnumTest["A"] is StrEnumTest.A
    assert StrEnumPropertiesTest["A"] is StrEnumPropertiesTest.A
    assert StrEnumTest("a") is StrEnumTest.A
    assert StrEnumPropertiesTest("a") is StrEnumPropertiesTest.A

    assert len(StrEnumTest) == 3
    assert len(StrEnumPropertiesTest) == 3

    # type-check probes
    assert_type(StrEnumTest.A, Literal[StrEnumTest.A])
    assert_type(StrEnumPropertiesTest.A, Literal[StrEnumPropertiesTest.A])
    assert_type(StrEnumTest.A.value, Literal["a"])
    assert_type(StrEnumPropertiesTest.A.value, Literal["a"])
    v0: str = StrEnumTest.A  # StrEnum is also str
    v1: str = StrEnumPropertiesTest.A
    assert_type(list(StrEnumTest), list[StrEnumTest])
    assert_type(list(StrEnumPropertiesTest), list[StrEnumPropertiesTest])
    assert_type(StrEnumTest.__members__, MappingProxyType[str, StrEnumTest])
    assert_type(
        StrEnumPropertiesTest.__members__, MappingProxyType[str, StrEnumPropertiesTest]
    )

    # --------------------------------------------------------------- IntEnum
    class IntEnumTest(IntEnum):
        A = 1
        B = 2
        C = 3

    class IntEnumPropertiesTest(IntEnumProperties):
        A = 1
        B = 2
        C = 3

    # runtime
    _4: list[int] = [m for m in IntEnumTest]
    _5: list[int] = [m for m in IntEnumPropertiesTest]
    _4r: list[Any] = [m for m in reversed(IntEnumTest)]
    _5r: list[Any] = [m for m in reversed(IntEnumPropertiesTest)]
    assert _4 and _5
    assert 1 in IntEnumTest
    assert 1 in IntEnumPropertiesTest
    assert IntEnumTest["A"] is IntEnumTest.A
    assert IntEnumPropertiesTest["A"] is IntEnumPropertiesTest.A
    assert IntEnumTest(1) is IntEnumTest.A
    assert IntEnumPropertiesTest(1) is IntEnumPropertiesTest.A
    assert IntEnumTest.A + 1 == 2
    assert IntEnumPropertiesTest.A + 1 == 2

    assert len(IntEnumTest) == 3
    assert len(IntEnumPropertiesTest) == 3

    # type-check probes
    assert_type(IntEnumTest.A, Literal[IntEnumTest.A])
    assert_type(IntEnumPropertiesTest.A, Literal[IntEnumPropertiesTest.A])
    assert_type(IntEnumTest.A.value, Literal[1])
    assert_type(IntEnumPropertiesTest.A.value, Literal[1])
    _v2: int = IntEnumTest.A  # IntEnum is also int
    _v3: int = IntEnumPropertiesTest.A
    assert_type(list(IntEnumTest), list[IntEnumTest])
    assert_type(list(IntEnumPropertiesTest), list[IntEnumPropertiesTest])
    assert_type(IntEnumTest.__members__, MappingProxyType[str, IntEnumTest])
    assert_type(
        IntEnumPropertiesTest.__members__, MappingProxyType[str, IntEnumPropertiesTest]
    )

    # ------------------------------------------------------------------ Flag
    class FlagTest(Flag):
        A = 1 << 0
        B = 1 << 1
        C = 1 << 2

    class FlagPropertiesTest(FlagProperties):
        A = 1 << 0
        B = 1 << 1
        C = 1 << 2

    # runtime
    _6: list[Flag] = [m for m in FlagTest]
    _7: list[Flag] = [m for m in FlagPropertiesTest]
    assert _6 and _7
    assert 1 in FlagTest
    assert 1 in FlagPropertiesTest

    ab0 = FlagTest.A | FlagTest.B
    ab1 = FlagPropertiesTest.A | FlagPropertiesTest.B
    assert FlagTest.A in ab0
    assert FlagPropertiesTest.A in ab1
    assert (ab0 & FlagTest.A) is FlagTest.A
    assert (ab1 & FlagPropertiesTest.A) is FlagPropertiesTest.A

    # type-check probes
    assert_type(FlagTest.A, Literal[FlagTest.A])
    assert_type(FlagPropertiesTest.A, Literal[FlagPropertiesTest.A])
    assert_type(FlagTest["A"], FlagTest)
    assert_type(FlagPropertiesTest["A"], FlagPropertiesTest)
    assert_type(FlagTest(1), FlagTest)
    assert_type(FlagPropertiesTest(1), FlagPropertiesTest)
    assert_type(list(FlagTest), list[FlagTest])
    assert_type(list(FlagPropertiesTest), list[FlagPropertiesTest])
    assert_type(FlagTest.__members__, MappingProxyType[str, FlagTest])
    assert_type(
        FlagPropertiesTest.__members__, MappingProxyType[str, FlagPropertiesTest]
    )

    # combined flag results should preserve the enum type
    assert_type(FlagTest.A | FlagTest.B, FlagTest)
    assert_type(FlagPropertiesTest.A | FlagPropertiesTest.B, FlagPropertiesTest)
    assert_type(FlagTest.A & FlagTest.B, FlagTest)
    assert_type(FlagPropertiesTest.A & FlagPropertiesTest.B, FlagPropertiesTest)

    # --------------------------------------------------------------- IntFlag
    class IntFlagTest(IntFlag):
        A = 1 << 0
        B = 1 << 1
        C = 1 << 2

    class IntFlagPropertiesTest(IntFlagProperties):
        A = 1 << 0
        B = 1 << 1
        C = 1 << 2

    # runtime
    _8: list[int] = [m for m in IntFlagTest]
    _9: list[int] = [m for m in IntFlagPropertiesTest]
    assert _8 and _9
    assert 1 in IntFlagTest
    assert 1 in IntFlagPropertiesTest

    ab2 = IntFlagTest.A | IntFlagTest.B
    ab3 = IntFlagPropertiesTest.A | IntFlagPropertiesTest.B
    assert int(ab2) == 3
    assert int(ab3) == 3
    assert IntFlagTest.A in ab2
    assert IntFlagPropertiesTest.A in ab3

    # type-check probes
    assert_type(IntFlagTest.A, Literal[IntFlagTest.A])
    assert_type(IntFlagPropertiesTest.A, Literal[IntFlagPropertiesTest.A])
    assert_type(IntFlagTest.A.value, int)
    assert_type(IntFlagPropertiesTest.A.value, int)
    _v4: int = IntFlagTest.A  # IntFlag is also int
    _v5: int = IntFlagPropertiesTest.A
    assert_type(list(IntFlagTest), list[IntFlagTest])
    assert_type(list(IntFlagPropertiesTest), list[IntFlagPropertiesTest])
    assert_type(IntFlagTest.__members__, MappingProxyType[str, IntFlagTest])
    assert_type(
        IntFlagPropertiesTest.__members__, MappingProxyType[str, IntFlagPropertiesTest]
    )

    assert_type(IntFlagTest.A | IntFlagTest.B, IntFlagTest)
    assert_type(
        IntFlagPropertiesTest.A | IntFlagPropertiesTest.B, IntFlagPropertiesTest
    )
    assert_type(IntFlagTest.A & IntFlagTest.B, IntFlagTest)
    assert_type(
        IntFlagPropertiesTest.A & IntFlagPropertiesTest.B, IntFlagPropertiesTest
    )
