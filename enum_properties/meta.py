"""
Metaprogramming and mixin tools that implement property tuple support for
python enumeration classes. Symmetric lookups are supported with an additional
SymmetricMixin class.
"""
from collections import namedtuple
from collections.abc import Hashable
from typing import TypeVar, Type
from enum import EnumMeta
import types


class _Prop:
    """An empty class used to identify properties"""
    pass


SymmetricProperty = namedtuple("SymmetricProperty", "name case_sensitive")

P = TypeVar('P', bound=_Prop)


def p(
    prop_name: str,
    symmetric: bool = False,
    case_sensitive: bool = True
) -> Type[P]:
    """
    Add a property of the given name to the enumeration class by inheritance.
    Properties must be specified in the order in which they appear in the
    value tuple specification. For instance:

    .. code-block::

        class EnumType(
            SymmetricMixin,
            int,
            enum.Enum,
            p('prop1'),
            p('prop1', symmetric=True, case_sensitive=False)
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
    :param symmetric: If true, the enumeration will be able to be instantiated
     from this value
    :param case_sensitive: If false and symmetric and property is a string,
        instantiation from this value will be case insensitive
    :return: a named property class
    """
    return type(
        prop_name,
        (_Prop,),
        {'symmetric': symmetric, 'case_sensitive': case_sensitive}
    )


class SymmetricMixin:

    _ep_missing_map_ = {}
    _ep_symmetric_properties_ = {'name', 'label'}

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

        if value in cls._ep_missing_map_:
            return cls._ep_missing_map_[value]

        if isinstance(value, str):
            if value.upper() in cls._ep_missing_map_:
                return cls._ep_missing_map_[value.upper()]

        for prop in getattr(cls, '_ep_symmetric_properties_', set()):
            for en in cls:
                if hasattr(en, prop) and getattr(en, prop) == value:
                    return en

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


class EnumProperties(EnumMeta):
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
                properties[base.__name__] = []
                if getattr(base, 'symmetric', False):
                    symmetrical_properties.append(
                        SymmetricProperty(
                            name=base.__name__,
                            case_sensitive=getattr(
                                base,
                                'case_sensitive', True
                            )
                        )
                    )
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
                # are we an enum value?
                before = len(class_dict._member_names)
                class_dict[key] = value
                after = len(class_dict._member_names)
                if after > before:
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
        symmetrical_properties = {
            prop.name: prop for prop in
            getattr(classdict, '_ep_symmetrical_properties', [])
        }
        cls = super().__new__(
            metacls,
            classname,
            tuple([base for base in bases if not issubclass(base, _Prop)]),
            classdict,
            **kwds
        )
        symmetric_lookup = classdict.get('_ep_missing_map_', {})

        def add_sym_lookup(prop, p_val, enum_inst, case_sensitive):
            if not isinstance(p_val, Hashable):
                raise TypeError(
                    f'{cls}.{prop}:{p_val} is not hashable. Symmetrical '
                    f'enumeration properties must be hashable or a list of '
                    f'hashable values.'
                )
            symmetric_lookup[p_val] = enum_inst
            if not case_sensitive and isinstance(p_val, str):
                symmetric_lookup[p_val.upper()] = enum_inst

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
            if prop in symmetrical_properties:
                for idx, val in enumerate(values):
                    enum_cls = list(cls._value2member_map_.values())[idx]
                    if isinstance(val, (set, list)):
                        for v in val:
                            add_coerce_type(type(v))
                            add_sym_lookup(
                                prop,
                                v,
                                enum_cls,
                                symmetrical_properties[prop].case_sensitive
                            )
                    else:
                        add_sym_lookup(
                            prop,
                            val,
                            enum_cls,
                            symmetrical_properties[prop].case_sensitive
                        )
                        add_coerce_type(type(val))

        setattr(cls, '_ep_coerce_types_', coerce_types)
        if symmetric_lookup:
            setattr(cls, '_ep_missing_map_', symmetric_lookup)
        return cls
