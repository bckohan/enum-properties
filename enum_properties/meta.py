"""
Metaprogramming and mixin tools that implement property tuple support for
python enumeration classes. Symmetric lookups are supported with an additional
SymmetricMixin class.

Given how dynamic the typing is in this code, it's not much of a value add to
add static type checking - revisit in the future if advances warrant it.
"""
# pylint: disable=protected-access
from __future__ import annotations

import unicodedata
from collections.abc import Hashable
from enum import Enum, EnumMeta


def _do_casenorm(text):
    return unicodedata.normalize('NFKD', text.casefold())


class _Prop(str):
    """ Property interface - private """

    def __new__(cls):
        return super().__new__(cls, cls.name())

    @classmethod
    def name(cls):
        """ the name of a property is its class name """
        return cls.__name__


class _SProp(_Prop):
    pass


def s(  # pylint: disable=C0103
    prop_name,
    case_fold=False
):
    """
    Add a symmetric property. Enumeration values will be coercible from this
    property's values.

    :param prop_name:
    :param case_fold: If False, symmetric lookup will be
        case sensitive (default)
    :return: a named property class
    """
    return type(
        prop_name,
        (_SProp,),
        {'symmetric': True, 'case_fold': case_fold}
    )


def p(prop_name):  # pylint: disable=C0103
    """
    Add a property of the given name to the enumeration class by inheritance.
    Properties must be specified in the order in which they appear in the
    value tuple specification.

    :param prop_name: The name of the property
    :return: a named property class
    """
    return type(prop_name, (_Prop,), {'symmetric': False})


class SymmetricMixin:  # pylint: disable=R0903
    """
    This mixin enables symmetric Enum creation from properties marked
    symmetric. It is included by default in the EnumProperties base class,
    but can be disabled by overriding _missing_ and explicitly skipping it.
    """

    _ep_symmetric_map_ = {}
    _ep_isymmetric_map_ = {}
    _symmetric_builtins_ = ['name']

    class ValueWrapper:
        """
        A wrapper classed used to recursively iterate through type coercions
        of a potential matching enumeration value in priority order
        """

        value = None
        types = []
        enum = None

        @staticmethod
        def from_value(
                value,
                typ,
                types,
                enum_cls
        ):
            """Wrap a value in our type coercion iterator"""
            class Value(SymmetricMixin.ValueWrapper, typ):
                """Wrapper class"""
            wrapped = Value(value)
            wrapped.value = value
            wrapped.types = types
            wrapped.enum = enum_cls
            return wrapped

        @property
        def type(self):
            """Get the wrapped value's type."""
            return type(self.value)

        def __next__(self):
            """
            Get the next wrapped value, coerced to the next type of highest
            priority - this will recurse with _missing_ until a match is
            found or all types are exhausted.

            :return None if no match was found, the matching enumeration
                otherwise
            """
            while self.types:
                # skip already coerced types, or types of our own Enum type
                if self.types[0] is self.type or self.types[0] is self.enum:
                    self.types.pop(0)
                    continue
                try:
                    # this will invoke _missing_ again
                    return self.enum(  # pylint: disable=E1102
                        self.from_value(
                            self.value,
                            self.types.pop(0),
                            self.types,
                            self.enum
                        )
                    )
                except (TypeError, ValueError):
                    pass
            return None

    @classmethod
    def _missing_(cls, value):
        """
        The implementation of symmetric _missing_ is necessarily complex.
        Arbitrary types can be mapped to enumeration values so long as they
        are hashable. Coercion to all possible types must be attempted on
        value, in priority order before failure.

        :param value: The value (possibly wrapped) to attempt coercion to our
            enumeration type.
        :raises ValueError: if no enumeration match can be found.
        :return: A valid instance of this enumeration
        """

        try:
            return cls._ep_symmetric_map_[value]
        except KeyError:
            pass

        if isinstance(value, str):
            try:
                return cls._ep_isymmetric_map_[_do_casenorm(value)]
            except KeyError:
                pass

        # wrap value in a ValueWrapper that keeps track of the type
        if not isinstance(value, cls.ValueWrapper):
            value = cls.ValueWrapper.from_value(
                value,
                type(value),
                getattr(cls, '_ep_coerce_types_', []).copy(),
                cls
            )

        result = next(value)
        if isinstance(result, cls):
            return result
        return super()._missing_(value)


class EnumPropertiesMeta(EnumMeta):
    """
    A metaclass for creating enum choices with additional named properties for
    each value.
    """

    EXPECTED = ['_symmetric_builtins_']
    RESERVED = [
        'enum_properties',
        '_ep_coerce_types_',
        '_ep_symmetric_map_',
        '_ep_isymmetric_map_'
    ]

    @classmethod
    def __prepare__(mcs, cls, bases):
        bases = list(bases)
        properties = {}
        real_bases = []
        # these are properties that the enum can be instantiated from
        # i.e. MyEnum.VALUE1 is MyEnum(symmetric property of VALUE1)
        symmetric_properties = []
        for base in bases:
            if issubclass(base, _Prop):
                if (
                    base.name() in EnumPropertiesMeta.RESERVED +
                    EnumPropertiesMeta.EXPECTED
                ):
                    raise ValueError(f'{base.name()} is reserved.')
                properties[base()] = []
            else:
                real_bases.append(base)

        class_dict = super().__prepare__(cls, tuple(real_bases))

        class _PropertyEnumDict(class_dict.__class__):
            """
            This wrapper class is used to strip properties off of the
            enumeration values and capture them as they are set into the class
            dictionary. Wrapping the private enumeration code and delegating
            all of the existing functionality to the delegate allows a light
            touch that should be robust to future changes in enum.
            """

            _ep_properties_ = properties
            _ep_symmetric_properties = symmetric_properties

            def __init__(self):
                super().__init__()
                for attr in set(dir(class_dict)).difference(set(dir(self))):
                    setattr(self, attr, getattr(class_dict, attr))
                for item, value in class_dict.items():
                    self[item] = value

            def __setitem__(self, key, value):
                if key in EnumPropertiesMeta.EXPECTED:
                    dict.__setitem__(self, key, value)
                elif key in EnumPropertiesMeta.RESERVED:
                    raise ValueError(f'{key} is reserved.')
                elif self._ep_properties_:
                    # are we an enum value? - just kick this up to parent class
                    # logic, this code runs once on load - its fine that it's
                    # doing a little redundant work and doing it this way
                    # ensures robust fidelity to Enum behavior.
                    before = len(class_dict._member_names)
                    class_dict[key] = value
                    if len(class_dict._member_names) > before:
                        try:
                            num_vals = len(value) - len(self._ep_properties_)
                            if (
                                num_vals < 1 or
                                len(self._ep_properties_) !=
                                len(value[num_vals:])
                            ):
                                raise ValueError(
                                    f'{key} must have '
                                    f'{len(self._ep_properties_)} property '
                                    f'values.'
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
                                f'{key} must have {len(self._ep_properties_)} '
                                f'property values.'
                            ) from type_err
                    super().__setitem__(key, value)
                else:
                    super().__setitem__(key, value)

        return _PropertyEnumDict()

    def __new__(
            mcs: EnumPropertiesMeta,
            classname,
            bases,
            classdict
    ):
        cls = super().__new__(
            mcs,
            classname,
            tuple(base for base in bases if not issubclass(base, _Prop)),
            classdict
        )
        cls._ep_coerce_types_ = []
        cls._ep_symmetric_map_ = {}
        cls._ep_isymmetric_map_ = {}
        cls.enum_properties = list(classdict._ep_properties_.keys())

        def add_sym_lookup(prop, p_val, enum_inst):
            if not isinstance(p_val, Hashable):
                raise ValueError(
                    f'{cls}.{prop}:{p_val} is not hashable. Symmetrical '
                    f'enumeration properties must be hashable or a list of '
                    f'hashable values.'
                )
            cls._ep_symmetric_map_[p_val] = enum_inst
            if prop.case_fold and isinstance(p_val, str):
                cls._ep_isymmetric_map_[_do_casenorm(p_val)] = enum_inst

        def add_coerce_type(typ):
            if (
                typ not in cls._ep_coerce_types_ and
                isinstance(typ, Hashable) and not issubclass(typ, cls)
            ):
                cls._ep_coerce_types_.append(typ)

        for val in cls:
            add_coerce_type(type(val.value))

        # we reverse to maintain precedence order for symmetric lookups
        for prop in reversed(cls.enum_properties):
            values = classdict._ep_properties_[prop]
            setattr(
                cls,
                f'_value2{prop}_map_',
                dict(zip(cls._value2member_map_, values))
            )
            setattr(
                cls,
                prop,
                property(
                    lambda self, prop=prop:
                    getattr(cls, f'_value2{prop}_map_').get(self.value)
                )
            )

            if prop.symmetric:
                for idx, val in enumerate(values):
                    enum_cls = list(cls._value2member_map_.values())[idx]
                    if isinstance(val, (set, list)):
                        for val_item in val:
                            add_coerce_type(type(val_item))
                            add_sym_lookup(
                                prop,
                                val_item,
                                enum_cls
                            )
                    else:
                        add_sym_lookup(
                            prop,
                            val,
                            enum_cls
                        )
                        add_coerce_type(type(val))

        # add builtin symmetries
        for sym_builtin in reversed(getattr(cls, '_symmetric_builtins_', [])):
            # allow simple strings for the default case
            if isinstance(sym_builtin, str):
                sym_builtin = s(sym_builtin)()
            elif issubclass(sym_builtin, _SProp):
                sym_builtin = sym_builtin()
            else:
                raise ValueError(
                    f'_symmetric_builtins_ contained {type(sym_builtin)}, '
                    f'expected string or s() property.'
                )

            for enum_val in cls:
                if not hasattr(enum_val, sym_builtin):
                    raise ValueError(
                        f'{cls}.{sym_builtin} does not exist, but is listed in'
                        f' _symmetric_builtins_.'
                    )
                add_sym_lookup(
                    sym_builtin,
                    getattr(enum_val, sym_builtin),
                    enum_val
                )

        return cls


class EnumProperties(SymmetricMixin, Enum, metaclass=EnumPropertiesMeta):
    """
    Use this base class instead of Enum to enable enumeration properties.
    For example:

    .. code-block::

        class EnumType(
            EnumProperties,
            p('prop1'), #
            s('prop1', case_fold=True)  # case insensitive symmetric property
        ):

            VAL1 = 1, "prop1's value1", "prop2's value1"
            VAL2 = 2, "prop1's value2", "prop2's value2"
            VAL3 = 3, "prop1's value3", "prop2's value3"

        EnumType.VAL1.value == 1
        EnumType.VAL1.name == 'VAL1'
        EnumType.VAL1 == EnumType('VAL1') # auto symmetry w/ name strings
        EnumType.VAL1.prop1 == "prop1's value1"
        EnumType.VAL1.prop2 == "prop2's value1"
        EnumType("prop1's value1") # throws ValueError b/c not symmetric
        EnumType("prop2's value1")
            == EnumType.VAL1
            == EnumType("PRoP2'S ValUE1")
    """
