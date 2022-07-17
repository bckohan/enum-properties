"""
Metaprogramming and mixin tools that implement property tuple support for
python enumeration classes. Symmetric lookups are supported with an additional
SymmetricMixin class.
"""
from collections.abc import Hashable
from typing import TypeVar, Type
from enum import EnumMeta, Enum
import inspect


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

P = TypeVar('P', bound=_Prop)
S = TypeVar('S', bound=_SProp)


def s(prop_name: str, case_sensitive: bool = True) -> Type[S]:
    """
    Add a symmetric property. Enumeration values will be coercible from this
    property's values.

    :param prop_name:
    :param case_sensitive: If True, symmetric lookup will be
        case sensitive (default)
    :return: a named property class
    """
    return type(
        prop_name,
        (_SProp,),
        {'symmetric': True, 'case_sensitive': case_sensitive}
    )


def p(prop_name: str) -> Type[P]:
    """
    Add a property of the given name to the enumeration class by inheritance.
    Properties must be specified in the order in which they appear in the
    value tuple specification. For instance:

    .. code-block::

        class EnumType(
            EnumProperties,
            p('prop1'),
            s('prop1', case_sensitive=False)
        ):

            VAL1 = 1, _('Value 1'), "prop1's value1", "prop2's value1"
            VAL2 = 2, _('Value 2'), "prop1's value2", "prop2's value2"
            VAL3 = 3, _('Value 3'), "prop1's value3", "prop2's value3"

        EnumType.VAL1.value == 1
        EnumType.VAL1.name == 'VAL1'
        EnumType.VAL1 == EnumType('VAL1') # auto symmetry w/ name strings
        EnumType.VAL1.label == 'Value 1'
        EnumType.VAL1.prop1 == "prop1's value1"
        EnumType.VAL1.prop2 == "prop2's value1"
        EnumType("prop1's value1") # throws ValueError b/c not symmetrical
        EnumType("prop2's value1")
            == EnumType.VAL1
            == EnumType("PRoP2'S ValUE1")

    :param prop_name: The name of the property
    :return: a named property class
    """
    return type(prop_name, (_Prop,), {'symmetric': False})


class SymmetricMixin:

    _ep_missing_map_ = {}
    _ep_symmetric_map_ = {}
    symmetrical_builtins = ['name']

    class ValueWrapper:
        """
        A wrapper classed used to recursively iterate through type coercions
        of a potential matching enumeration value in priority order
        """

        value = None
        types = []
        enum = None

        @staticmethod
        def from_value(value, typ, types, enum_cls):
            """Wrap a value in our type coercion iterator"""
            class Value(SymmetricMixin.ValueWrapper, typ):
                pass
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
                    return self.enum(
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
        The implementation of symmetrical _missing_ is necessarily complex.
        Arbitrary types can be mapped to enumeration values so long as they
        are hashable. Coercion to all possible types must be attempted on
        value, in priority order before failure.

        :param value: The value (possibly wrapped) to attempt coercion to our
            enumeration type.
        :raises ValueError: if no enumeration match can be found.
        :return:
        """

        try:
            return cls._ep_missing_map_[value]
        except KeyError:
            pass

        if isinstance(value, str):
            try:
                return cls._ep_symmetric_map_[value.upper()]
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

    @classmethod
    def __prepare__(metacls, cls, bases, **kwargs):
        bases = list(bases)
        properties = {}
        real_bases = []
        # these are properties that the enum can be instantiated from
        # i.e. MyEnum.VALUE1 is MyEnum(symmetrical property of VALUE1)
        symmetrical_properties = []
        for base in bases:
            if issubclass(base, _Prop):
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

            _ep_properties = properties
            _ep_symmetrical_properties = symmetrical_properties

            def __init__(self):
                super().__init__()
                for attr in set(dir(class_dict)).difference(set(dir(self))):
                    setattr(self, attr, getattr(class_dict, attr))
                for item, value in class_dict.items():
                    self[item] = value

            def __setitem__(self, key, value):
                # are we an enum value? - just kick this up to parent class
                # logic, this code runs once on load - its fine that it's doing
                # a little redundant work and doing it this way ensures robust
                # fidelity to Enum behavior.
                before = len(class_dict._member_names)
                class_dict[key] = value
                if len(class_dict._member_names) > before:
                    try:
                        nv = len(value) - len(self._ep_properties)
                        assert nv > 0, f'{key} must have ' \
                                       f'{len(self._ep_properties)} property' \
                                       f' values.'
                        if self._ep_properties:
                            assert (len(self._ep_properties) ==
                                    len(value[nv:])), \
                                f'{key} must have {len(self._ep_properties)}' \
                                f' property values.'
                            idx = nv
                            for prop, values in self._ep_properties.items():
                                values.append(value[idx])
                                idx += 1
                        if nv == 1:
                            value = value[0]
                        else:
                            value = value[0:nv]
                    except TypeError:
                        pass
                super().__setitem__(key, value)

        return _PropertyEnumDict()

    def __new__(metacls, classname, bases, classdict, **kwds):
        properties = getattr(classdict, '_ep_properties', {})
        cls = super().__new__(
            metacls,
            classname,
            tuple([base for base in bases if not issubclass(base, _Prop)]),
            classdict,
            **kwds
        )
        symmetric_lookup = classdict.get('_ep_missing_map_', {})
        isymmetric_lookup = {}
        symmetries = []

        def add_sym_lookup(prop, p_val, enum_inst):
            if not isinstance(p_val, Hashable):
                raise ValueError(
                    f'{cls}.{prop}:{p_val} is not hashable. Symmetrical '
                    f'enumeration properties must be hashable or a list of '
                    f'hashable values.'
                )
            symmetric_lookup[p_val] = enum_inst
            if not prop.case_sensitive and isinstance(p_val, str):
                isymmetric_lookup[p_val.upper()] = enum_inst
            if prop not in symmetries:
                symmetries.insert(0, prop)

        coerce_types = []

        def add_coerce_type(typ):
            if typ not in coerce_types and isinstance(typ, Hashable) and \
                    not issubclass(typ, cls):
                coerce_types.append(typ)

        for val in cls:
            add_coerce_type(type(val.value))

        # we reverse to maintain precedence order for symmetrical lookups
        for prop in reversed(list(properties.keys())):
            values = properties[prop]
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
                        for v in val:
                            add_coerce_type(type(v))
                            add_sym_lookup(
                                prop,
                                v,
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
        for sym_builtin in reversed(getattr(cls, 'symmetrical_builtins', [])):
            # allow simple strings for the default case
            if isinstance(sym_builtin, str):
                sym_builtin = s(sym_builtin)()
            else:
                sym_builtin = sym_builtin()

            for en in cls:
                assert hasattr(en, sym_builtin), (
                    f'{cls}.{sym_builtin} does not exist, but is listed in'
                    f' symmetrical_builtins.'
                )
                add_sym_lookup(
                    sym_builtin,
                    getattr(en, sym_builtin),
                    en
                )

        setattr(cls, '_ep_coerce_types_', coerce_types)
        setattr(cls, 'symmetries', list(symmetries))
        setattr(cls, 'properties', list(properties.keys()))
        if symmetric_lookup:
            setattr(cls, '_ep_missing_map_', symmetric_lookup)
        if isymmetric_lookup:
            setattr(cls, '_ep_symmetric_map_', isymmetric_lookup)
        return cls


class EnumProperties(SymmetricMixin, Enum, metaclass=EnumPropertiesMeta):
    pass
