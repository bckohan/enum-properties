r"""
*******************************************************************************
   ____                  ___                        __  _
  / __/__  __ ____ _    / _ \_______  ___  ___ ____/ /_(_)__ ___
 / _// _ \/ // /  ' \  / ___/ __/ _ \/ _ \/ -_) __/ __/ / -_|_-<
/___/_//_/\_,_/_/_/_/ /_/  /_/  \___/ .__/\__/_/  \__/_/\__/___/
                                   /_/
*******************************************************************************

Metaprogramming and mixin tools that implement property tuple and method
specialization support for python enumeration classes.

.. todo::
    Given how dynamic the typing is in this module, static type checking is
    awkward - revisit in the future if advances warrant it.

"""

import enum
import sys
import typing as t
import unicodedata
from collections.abc import Generator, Hashable, Iterable
from dataclasses import dataclass
from functools import cached_property

VERSION = (2, 1, 0)

__title__ = "Enum Properties"
__version__ = ".".join(str(i) for i in VERSION)
__author__ = "Brian Kohan"
__license__ = "MIT"
__copyright__ = "Copyright 2022-2025 Brian Kohan"

__all__ = [
    "VERSION",
    "EnumProperties",
    "IntEnumProperties",
    "FlagProperties",
    "IntFlagProperties",
    "EnumPropertiesMeta",
    "SymmetricMixin",
    "DecomposeMixin",
    "specialize",
    "p",
    "s",
]


T = t.TypeVar("T")


def with_typehint(baseclass: t.Type[T]) -> t.Type[T]:
    """
    This is icky but it works - revisit in future.
    """
    if t.TYPE_CHECKING:
        return baseclass  # pragma: no cover
    return object  # type: ignore


def _do_casenorm(text: str) -> str:
    """Normalize unicode text to be case agnostic."""
    return unicodedata.normalize("NFKD", text.casefold())


@dataclass
class Symmetric:
    case_fold: bool = False
    """
    If False, symmetric lookup will be case sensitive (default)
    """

    match_none: bool = False
    """
    If True, none values will be symmetric, if False (default), 
    none values for symmetric properties will not map back to
    the enumeration value.
    """


class _Prop(str):
    """Property interface - private"""

    symmetric: bool = False

    def __new__(cls):
        return super().__new__(cls, cls.name())  # type: ignore[no-untyped-call]

    @classmethod
    def name(cls):
        """the name of a property is its class name"""
        return cls.__name__


class _SProp(_Prop):
    """Symmetric property interface - private"""

    symmetric: bool = True
    case_fold: bool
    match_none: bool


def s(
    prop_name: str, case_fold: bool = False, match_none: bool = False
) -> t.Type[_SProp]:
    """
    Add a symmetric property. Enumeration values will be coercible from this
    property's values.

    :param prop_name: The name of the property
    :param case_fold: If False, symmetric lookup will be
        case sensitive (default)
    :param match_none: If True, none values will be symmetric, if False
        (default), none values for symmetric properties will not map back to
        the enumeration value.
    :return: a named symmetric property class
    """
    return type(
        prop_name,
        (_SProp,),
        {"case_fold": case_fold, "match_none": match_none},
    )


def p(prop_name: str) -> t.Type[_Prop]:
    """
    Add a property of the given name to the enumeration class by inheritance.
    Properties must be specified in the order in which they appear in the
    value tuple specification. This call works by constructing a new type with
    a classname that corresponds to the property name. The class inherits from
    str and can be instantiated as a string by calling its empty constructor.

    :param prop_name: The name of the property
    :return: a named property class
    """
    return type(prop_name, (_Prop,), {})


class _Specialized:
    """
    A member specialization identifier class - private. Used to wrap
    specialized member functions and tag them with their enum values so the
    Enum classdict can identify them.

    :param wrapped: The wrapped member function
    :param value: The value to specialize for
    """

    def __init__(self, wrapped: t.Callable[..., t.Any], values: t.Sequence[t.Any]):
        self.wrapped = wrapped
        # map to ids, because in some corner cases values might get
        # permuted (dataclasses) or not otherwise be hashable
        # this is a little bit hocus pocus but CI will catch it
        # if it breaks
        self.ids = [id(value) for value in values]


def specialize(*values):
    """
    A decorator to specialize a method for a given enumeration value.

    :param values: The enumeration value(s) to specialize
    :return: A decorated specialized member method
    """

    def specialize_decorator(method):
        return _Specialized(method, values)

    return specialize_decorator


class SymmetricMixin(with_typehint("EnumProperties")):  # type: ignore
    """
    This mixin enables symmetric Enum_ creation from properties marked
    symmetric. It is included by default in the
    :py:class:`~enum_properties.EnumProperties` base class, but can be
    disabled by overriding ``_missing_`` and explicitly skipping it.

    If an enumeration type inherits builtin properties (e.g. name), those
    properties can be made symmetric by supplying a ``_symmetric_builtins_``
    member containing a list of string property names or
    :py:meth:`~enum_properties.s` values. By default, the ``name``
    property will be a case sensitive symmetric property.
    """

    def __eq__(self, value: t.Any) -> bool:
        """Symmetric equality - try to coerce value before failure"""
        if isinstance(value, self.__class__):
            return self.value == value.value
        try:
            return self.value == self.__class__(value).value
        except (ValueError, TypeError):
            return False

    def __ne__(self, value: t.Any) -> bool:
        """Symmetric inequality is the inverse of symmetric equality"""
        return not self.__eq__(value)

    @classmethod
    def _missing_(cls, value: t.Any) -> t.Any:
        """
        Arbitrary types can be mapped to enumeration values so long as they
        are hashable. Coercion to all possible types must be attempted on
        value, in priority order before failure.

        :param value: The value (possibly wrapped) to attempt coercion to our
            enumeration type.
        :raises ValueError: if no enumeration match can be found.
        :return: A valid instance of this enumeration
        """
        if (
            issubclass(cls, enum.Flag)
            and (not isinstance(value, Hashable) and isinstance(value, Iterable))
            or isinstance(value, Generator)
        ):
            composite = None
            for val in value:
                if composite is None:
                    composite = cls(val)
                else:
                    composite |= cls(val)
            if composite is None:
                return cls(0)
            return composite

        try:
            return cls._ep_symmetric_map_[value]
        except KeyError:
            pass

        if isinstance(value, str):
            try:
                return cls._ep_isymmetric_map_[_do_casenorm(value)]
            except KeyError:
                pass

        if value is not None:
            for coerce_to in cls._ep_coerce_types_:
                try:
                    val = coerce_to(value)
                    try:
                        return cls._value2member_map_[val]
                    except KeyError:
                        pass

                    try:
                        return cls._ep_symmetric_map_[val]
                    except KeyError:
                        pass

                    if isinstance(val, str):
                        return cls._ep_isymmetric_map_[_do_casenorm(val)]

                except Exception:
                    pass

        return super()._missing_(value)


class EnumPropertiesMeta(enum.EnumMeta):
    """
    A metaclass for creating enum choices with additional named properties for
    each value. An Enum_ can be given property support simply by:

    .. code-block::

        import enum
        from enum_properties import EnumPropertiesMeta

        class MyEnum(enum.Enum, metaclass=EnumPropertiesMeta):
            ...

    To support symmetrical properties, add the SymmetricMixin:

    .. code-block::

        import enum
        from enum_properties import (
            EnumPropertiesMeta,
            SymmetricMixin
        )

        class MyEnum(SymmetricMixin, enum.Enum, metaclass=EnumPropertiesMeta):
            ...

    All Enum_ functionality is compatible with the EnumPropertiesMeta
    metaclass. This class works by stripping out the
    :py:meth:`~enum_properties.p` and :py:meth:`~enum_properties.s`
    values during ``__prepare__`` and using their class name's as expected
    property values to set the appropriate values to properties in ``__new__``.

    .. automethod:: __prepare__

    """

    # members expected to be supplied by inheriting classes
    EXPECTED = ["_symmetric_builtins_"]

    # members reserved for use by EnumProperties
    RESERVED = [
        "_properties_",
        "_ep_coerce_types_",
        "_ep_symmetric_map_",
        "_ep_isymmetric_map_",
    ]

    _ep_symmetric_map_: t.Dict[t.Any, enum.Enum]
    _ep_isymmetric_map_: t.Dict[str, enum.Enum]
    _ep_coerce_types_: t.List[t.Type[t.Any]]
    _properties_: t.List[_Prop]

    @classmethod
    def __prepare__(mcs, cls, bases, **kwargs):
        """
        Strip properties out of inheritance and record them on our class
        dictionary for per-value based assignment in ``__new__``.

        :raises ValueError: If a reserved name is present as either a property
            or a member, or if the number of specified properties does not
            match the number of listed property values in the value tuples.
        """
        bases = list(bases)
        properties: t.Dict[_Prop, t.List[t.Any]] = {}
        real_bases = []
        for base in bases:
            if issubclass(base, _Prop):
                if (
                    base.name() in EnumPropertiesMeta.RESERVED
                    or base.name() in EnumPropertiesMeta.EXPECTED
                ):
                    raise ValueError(f"{base.name()} is reserved.")
                properties[base()] = []
            else:
                real_bases.append(base)

        class_dict = super().__prepare__(cls, tuple(real_bases), **kwargs)

        class _PropertyEnumDict(class_dict.__class__):  # type: ignore[name-defined]
            """
            This wrapper class is used to strip properties off of the
            enumeration values and capture them as they are set into the class
            dictionary. Wrapping the private enumeration code and delegating
            all of the existing functionality to the delegate allows a light
            touch that should be robust to future changes in enum.
            """

            _ep_properties_ = properties
            _specialized_: t.Dict[str, t.Dict[str, _Specialized]] = {}
            _ids_: t.Dict[int, str] = {}
            _member_names: t.Union[t.List[str], t.Dict[str, t.Any]]
            _create_properties_: bool = False

            class AnnotationPropertyRecorder(dict):
                class_dict: "_PropertyEnumDict"
                create_properties: bool

                def __init__(self, class_dict: "_PropertyEnumDict"):
                    self.class_dict = class_dict
                    # we only use annotations to create properties if p/s value
                    # inheritance is not used
                    super().__init__()

                def __setitem__(self, key, value):
                    if self.class_dict._create_properties_:
                        if (
                            key not in EnumPropertiesMeta.RESERVED
                            and key not in EnumPropertiesMeta.EXPECTED
                        ):
                            prop: t.Type[_Prop]
                            if getattr(value, "__metadata__", None) and isinstance(
                                value.__metadata__[0], Symmetric
                            ):
                                prop = s(
                                    key,
                                    case_fold=value.__metadata__[0].case_fold,
                                    match_none=value.__metadata__[0].match_none,
                                )
                            else:
                                prop = p(key)
                            if key == "name" or key == "value":
                                if issubclass(prop, _SProp):
                                    if self.class_dict.__contains__(
                                        "_symmetric_builtins_"
                                    ):
                                        self.class_dict["_symmetric_builtins_"].append(
                                            prop
                                        )
                                    else:
                                        self.class_dict["_symmetric_builtins_"] = [prop]
                            else:
                                self.class_dict._ep_properties_[prop()] = []
                    super().__setitem__(key, value)

            def __init__(self):
                super().__init__()
                for attr in set(dir(class_dict)).difference(set(dir(self))):
                    setattr(self, attr, getattr(class_dict, attr))
                for item, value in class_dict.items():
                    self[item] = value
                self._create_properties_ = not self._ep_properties_

            def __setitem__(self, key, value):
                if isinstance(value, _Specialized):
                    for en_val in value.ids:
                        self._specialized_.setdefault(self._ids_[en_val], {})[key] = (
                            value
                        )
                elif key in EnumPropertiesMeta.EXPECTED:
                    dict.__setitem__(self, key, value)
                elif key in EnumPropertiesMeta.RESERVED:
                    raise ValueError(f"{key} is reserved.")
                elif self._ep_properties_:
                    member_names = getattr(class_dict, "_member_names")
                    # are we an enum value? - just kick this up to parent class
                    # logic, this code runs once on load - its fine that it's
                    # doing a little redundant work and doing it this way
                    # ensures robust fidelity to Enum behavior.
                    before = len(member_names)
                    class_dict[key] = value
                    self._create_properties_ = False  # we're done with annotations
                    remove = False
                    if (
                        len(member_names) > before
                        and
                        # base class lets nested classes through! see:
                        # https://github.com/bckohan/enum-properties/issues/29
                        # todo remove below when minimum python >= 3.13
                        not isinstance(value, type)
                    ):
                        try:
                            num_vals = len(value) - len(self._ep_properties_)
                            if num_vals < 1 or len(self._ep_properties_) != len(
                                value[num_vals:]
                            ):
                                raise ValueError(
                                    f"{key} must have "
                                    f"{len(self._ep_properties_)} property "
                                    f"values."
                                )
                            idx = num_vals
                            for values in self._ep_properties_.values():
                                values.append(value[idx])
                                idx += 1
                            if num_vals == 1:
                                value = value[0]
                            else:
                                value = value[0:num_vals]

                        except TypeError as type_err:
                            raise ValueError(
                                f"{key} must have {len(self._ep_properties_)} "
                                f"property values."
                            ) from type_err

                    elif key in member_names:
                        remove = True  # pragma: no cover

                    self._ids_[id(value)] = key
                    super().__setitem__(key, value)

                    if remove:
                        # todo remove when minimum python >= 3.13
                        # base class lets nested classes through! see:
                        # https://github.com/bckohan/enum-properties/issues/29
                        if isinstance(self._member_names, list):
                            self._member_names.remove(key)
                        else:
                            # >= python 3.11
                            del self._member_names[key]
                else:
                    self._ids_[id(value)] = key
                    if key == "__annotations__":
                        value = self.AnnotationPropertyRecorder(self)
                    before = len(self._member_names)
                    super().__setitem__(key, value)
                    if len(self._member_names) > before:
                        self._create_properties_ = False

        return _PropertyEnumDict()  # type: ignore[no-untyped-call]

    def __new__(mcs, classname, bases, classdict, **kwargs):
        """
        Enumeration class construction runs in the following stages:

        1) pass up the inheritance tree to build the initial enumeration class.
        2) Add method specializations to each class
        3) Add property value to enumeration value maps for each property and
            the property accessors that use them
        4) Add casefolded symmetric maps for any symmetric properties
        5) Add any symmetric builtin properties to our symmetric maps

        :raises ValueError: if ``_symmetric_builtins_`` is specified
            incorrectly, or if non-hashable values are provided for a
            symmetric property.
        """
        cls = super().__new__(
            mcs,
            classname,
            tuple(base for base in bases if not issubclass(base, _Prop)),
            classdict,
            **kwargs,
        )
        cls._ep_coerce_types_ = []
        cls._ep_symmetric_map_ = cls._member_map_
        cls._ep_isymmetric_map_ = {}
        cls._properties_ = list(classdict._ep_properties_.keys())

        if classdict._specialized_:
            for val in cls:  # type: ignore[var-annotated]
                val = t.cast(enum.Enum, val)
                for member_name, specialization in classdict._specialized_.get(
                    val._name_, {}
                ).items():
                    # use descriptor binding
                    setattr(val, member_name, specialization.wrapped.__get__(val))

        def add_sym_lookup(prop: _SProp, p_val: t.Any, enum_inst: enum.Enum):
            if p_val is None and not prop.match_none:
                return
            if not isinstance(p_val, Hashable):
                raise ValueError(
                    f"{cls}.{prop}:{p_val} is not hashable. Symmetrical "
                    f"enumeration properties must be hashable or a list of "
                    f"hashable values."
                )
            cls._ep_symmetric_map_[p_val] = enum_inst
            if prop.case_fold and isinstance(p_val, str):
                cls._ep_isymmetric_map_[_do_casenorm(p_val)] = enum_inst

        def add_coerce_type(typ: t.Type[t.Any]):
            if (
                typ not in cls._ep_coerce_types_
                and issubclass(typ, Hashable)
                and not issubclass(typ, cls)
            ):
                cls._ep_coerce_types_.append(typ)

        for val in cls:
            val = t.cast(enum.Enum, val)
            add_coerce_type(type(val.value))

        # set properties onto the members
        for idx, member in enumerate(cls.__members__.values()):  # type: ignore[var-annotated]
            member = t.cast(enum.Enum, member)
            for prop, values in classdict._ep_properties_.items():
                setattr(member, prop, values[idx])

        # we reverse to maintain precedence order for symmetric lookups
        member_values = t.cast(
            t.List[enum.Enum],
            list(cls._value2member_map_.values() or cls.__members__.values()),
        )
        for prop in reversed([prop for prop in cls._properties_ if prop.symmetric]):
            prop = t.cast(_SProp, prop)
            for idx, val2 in enumerate(reversed(classdict._ep_properties_[prop])):
                enum_cls = member_values[len(member_values) - 1 - idx]
                if isinstance(val2, (set, list)):
                    for val_item in val2:
                        add_coerce_type(type(val_item))
                        add_sym_lookup(prop, val_item, enum_cls)
                else:
                    add_sym_lookup(prop, val2, enum_cls)
                    add_coerce_type(type(val2))

        # add builtin symmetries
        for sym_builtin in reversed(getattr(cls, "_symmetric_builtins_", [])):
            # allow simple strings for the default case
            if isinstance(sym_builtin, str):
                sym_builtin = s(sym_builtin)()
            elif issubclass(sym_builtin, _SProp):
                sym_builtin = sym_builtin()
            else:
                raise ValueError(
                    f"_symmetric_builtins_ contained {type(sym_builtin)}, "
                    f"expected string or s() property."
                )

            for enum_val in cls:  # type: ignore[var-annotated]
                enum_val = t.cast(enum.Enum, enum_val)
                if not hasattr(enum_val, sym_builtin):
                    raise ValueError(
                        f"{cls}.{sym_builtin} does not exist, but is listed in"
                        f" _symmetric_builtins_."
                    )
                add_sym_lookup(sym_builtin, getattr(enum_val, sym_builtin), enum_val)

        return cls


class EnumProperties(SymmetricMixin, enum.Enum, metaclass=EnumPropertiesMeta):
    """
    Use this base class instead of Enum_ to enable enumeration properties.
    For example:

    .. code-block::

        class EnumType(
            EnumProperties,
            p('prop1'),
            s('prop1', case_fold=True)  # case insensitive symmetric property
        ):

            VAL1 = 1, "prop1's value1", "prop2's value1"
            VAL2 = 2, "prop1's value2", "prop2's value2"
            VAL3 = 3, "prop1's value3", "prop2's value3"

    This is a shortcut for:

    .. code-block::

        class EnumType(SymmetricMixin, Enum, metaclass=EnumPropertiesMeta):
            ...

    See :ref:`usage` for more details.
    """

    def __hash__(self):
        return enum.Enum.__hash__(self)


class IntEnumProperties(SymmetricMixin, enum.IntEnum, metaclass=EnumPropertiesMeta):
    """
    An IntEnum that supports properties.

    .. note::
        Because SymmetricMixin implements __eq__ we also need an
        implementation of __hash__ on our class to keep it hashable
        We walk the mro to find the first implementation of __hash__
        and use it - this keeps our implementation hash equivalent
        to Enum/IntEnum behavior
    """

    def __hash__(self):
        return enum.IntEnum.__hash__(self)


if sys.version_info < (3, 11):
    str_enum_bases = (str, enum.Enum)
else:
    str_enum_bases = (enum.StrEnum,)


class StrEnumProperties(
    SymmetricMixin,
    *str_enum_bases,  # type: ignore
    metaclass=EnumPropertiesMeta,
):
    """
    An StrEnum that supports properties.
    """

    def __hash__(self):
        return getattr(enum, "StrEnum", str).__hash__(self)


class DecomposeMixin(with_typehint(enum.Flag)):  # type: ignore
    """
    A mixin for Flag enumerations that decomposes composite enumeration values
    and allows us to treat composite enumeration values as iterables of
    activated flags.
    """

    # instances are immutable and this has a small penalty to compute - it is
    # therefore a great candidate for a lazily computed cached_property
    @cached_property
    def flagged(self):
        """
        Returns the list of flags that are active.
        """
        return list(flag for flag in iter(self))

    def __iter__(self):
        """
        Return a generator for the active flags.
        """
        return (
            member
            for member in self.__class__  # type: ignore[attr-defined]
            if (
                (member.value != 0)
                and
                # make sure member is a power of 2, composites are included in
                # iteration < 3.11
                ((member.value & (member.value - 1)) == 0)
                and (self.value & member.value == member.value)
            )
        )

    def __len__(self):
        """
        Returns the number of active flags.
        """
        if self.value == 0:
            return 0
        return len(self.flagged)


class FlagProperties(
    DecomposeMixin, SymmetricMixin, enum.Flag, metaclass=EnumPropertiesMeta
):
    """
    A Flag that supports properties
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Intermixed property tuples can corrupt the last_values list with
        tuples. This method ensures only ints are present in last_values and
        delegates to the super class.
        """
        return enum.Flag._generate_next_value_(
            name,
            start,
            count,
            [val[0] if isinstance(val, tuple) else val for val in last_values],
        )

    def __hash__(self):
        return enum.Flag.__hash__(self)


class IntFlagProperties(  # type: ignore[misc]
    DecomposeMixin, SymmetricMixin, enum.IntFlag, metaclass=EnumPropertiesMeta
):
    """
    An IntFlag that supports properties.
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Intermixed property tuples can corrupt the last_values list with
        tuples. This method ensures only ints are present in last_values and
        delegates to the super class.
        """
        return enum.IntFlag._generate_next_value_(
            name,
            start,
            count,
            [val[0] if isinstance(val, tuple) else val for val in last_values],
        )

    def __hash__(self):
        return enum.IntFlag.__hash__(self)
