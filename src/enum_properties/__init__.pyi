"""Type stubs for enum_properties."""

import enum
import sys
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Literal, TypeAlias, TypeVar, overload

if sys.version_info >= (3, 11):
    pass
else:
    pass

VERSION: tuple[int, int, int]
__title__: str
__version__: str
__author__: str
__license__: str
__copyright__: str

S = TypeVar("S")
_EnumMemberT = TypeVar("_EnumMemberT")
_EnumNames: TypeAlias = (
    str | Iterable[str] | Iterable[Iterable[str | Any]] | Mapping[str, Any]
)
_Signature: TypeAlias = Any

@dataclass
class Symmetric:
    case_fold: bool = False
    match_none: bool = False

class _Prop(str):
    symmetric: bool
    @classmethod
    def name(cls) -> str: ...

class _SProp(_Prop):
    symmetric: Literal[True]  # pyright: ignore[reportIncompatibleVariableOverride]
    case_fold: bool
    match_none: bool

def s(
    prop_name: str, case_fold: bool = False, match_none: bool = False
) -> type[_SProp]: ...
def p(prop_name: str) -> type[_Prop]: ...
def symmetric(
    case_fold: bool = False, match_none: bool = False
) -> Callable[[S], S]: ...
def specialize(
    *values: Any,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...

class EnumPropertiesMeta(enum.EnumMeta):
    _ep_symmetric_map_: dict[Any, enum.Enum]
    _ep_isymmetric_map_: dict[str, enum.Enum]
    _ep_coerce_types_: list[type[Any]]
    _num_sym_props_: int
    _properties_: list[_Prop]
    __first_class_members__: list[str]

    def __iter__(self: type[_EnumMemberT]) -> Iterator[_EnumMemberT]: ...
    def __reversed__(self: type[_EnumMemberT]) -> Iterator[_EnumMemberT]: ...
    def __contains__(self: type[Any], value: object) -> bool: ...
    def __getitem__(self: type[_EnumMemberT], name: str) -> _EnumMemberT: ...
    @property
    def __members__(
        self: type[_EnumMemberT],
    ) -> MappingProxyType[str, _EnumMemberT]: ...
    def __len__(self) -> int: ...
    def __bool__(self) -> Literal[True]: ...
    @overload
    def __call__(
        cls: type[_EnumMemberT], value: Any, names: None = None
    ) -> _EnumMemberT: ...

    if sys.version_info >= (3, 11):
        @overload
        def __call__(
            cls,
            value: str,
            names: _EnumNames,
            *,
            module: str | None = None,
            qualname: str | None = None,
            type: type | None = None,
            start: int = 1,
            boundary: enum.FlagBoundary | None = None,
        ) -> type[enum.Enum]: ...
    else:
        @overload
        def __call__(
            cls,
            value: str,
            names: _EnumNames,
            *,
            module: str | None = None,
            qualname: str | None = None,
            type: type | None = None,
            start: int = 1,
        ) -> type[enum.Enum]: ...

    if sys.version_info >= (3, 12):
        @overload
        def __call__(
            cls: type[_EnumMemberT], value: Any, *values: Any
        ) -> _EnumMemberT: ...
    if sys.version_info >= (3, 14):
        @property
        def __signature__(cls) -> _Signature: ...

# SymmetricMixin is a mixin class, not an enum itself.
# It provides symmetric lookup functionality to enum classes.
class SymmetricMixin:
    _ep_symmetric_map_: dict[Any, enum.Enum]
    _ep_isymmetric_map_: dict[str, enum.Enum]
    _ep_coerce_types_: list[type[Any]]
    _num_sym_props_: int
    _properties_: list[_Prop]
    __first_class_members__: list[str]
    def __eq__(self, value: Any) -> bool: ...
    def __ne__(self, value: Any) -> bool: ...
    @classmethod
    def _missing_(cls, value: Any) -> Any: ...

# DecomposeMixin provides flag decomposition functionality.
# __iter__ is intentionally not declared here to avoid conflicts with Flag.__iter__
class DecomposeMixin:
    @property
    def flagged(self) -> list[enum.Flag]: ...
    def __len__(self) -> int: ...

# Use inheritance from the actual enum types to preserve
# pyright's special enum literal inference.
# These are base classes meant to be subclassed - they don't have members themselves.
class EnumProperties(  # type: ignore[misc]
    SymmetricMixin, enum.Enum, metaclass=EnumPropertiesMeta
):
    def __init__(self, value: object = ..., *args: object) -> None: ...
    def __hash__(self) -> int: ...

class IntEnumProperties(  # type: ignore[misc]
    SymmetricMixin, enum.IntEnum, metaclass=EnumPropertiesMeta
):
    def __init__(self, value: int, *args: object) -> None: ...
    def __hash__(self) -> int: ...

if sys.version_info >= (3, 11):
    class StrEnumProperties(  # type: ignore[misc]
        SymmetricMixin, enum.StrEnum, metaclass=EnumPropertiesMeta
    ):
        def __init__(self, value: str, *args: object) -> None: ...
        def __hash__(self) -> int: ...

else:
    class StrEnumProperties(  # type: ignore[misc]
        SymmetricMixin, str, enum.Enum, metaclass=EnumPropertiesMeta
    ):
        def __init__(self, value: str, *args: object) -> None: ...
        def __hash__(self) -> int: ...
        def __str__(self) -> str: ...
        @staticmethod
        def _generate_next_value_(
            name: str, start: int, count: int, last_values: list[Any]
        ) -> str: ...

class FlagProperties(  # type: ignore[misc]
    DecomposeMixin, SymmetricMixin, enum.Flag, metaclass=EnumPropertiesMeta
):
    def __init__(self, value: object = ..., *args: object) -> None: ...
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> int: ...
    def __hash__(self) -> int: ...

class IntFlagProperties(  # type: ignore[misc]
    DecomposeMixin, SymmetricMixin, enum.IntFlag, metaclass=EnumPropertiesMeta
):
    def __init__(self, value: int, *args: object) -> None: ...
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> int: ...
    def __hash__(self) -> int: ...
