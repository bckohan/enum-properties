from django.db.models import (
    Choices,
    TextChoices as DjangoTextChoices,
    IntegerChoices as DjangoIntegerChoices
)
from django.db.models.enums import ChoicesMeta
from django_enum.mixins import SymmetricMixin
from collections.abc import Hashable
from collections import namedtuple
from typing import TypeVar


__all__ = [
    'p',
    'EnumProperties',
    'TextChoices',
    'IntegerChoices',
    'FloatChoices'
]


class _Prop:
    """An empty class used to identify properties"""
    pass


SymmetricProperty = namedtuple("SymmetricProperty", "name case_sensitive")

P = TypeVar('P', bound=_Prop)


def p(prop_name: str, symmetric: bool = False, case_sensitive: bool = True) -> P:
    """
    Add a property of the given name to the enumeration class by inheritance. Properties must be specified in the order
    in which they appear in the value tuple specification. For instance:

    .. code-block::

        class EnumType(IntegerChoices, p('prop1'), p('prop1', symmetric=True, case_sensitive=False)):

            VAL1 = 1, _('Value 1'), "prop1's value1", "prop2's value1"
            VAL2 = 2, _('Value 2'), "prop1's value2", "prop2's value2"
            VAL3 = 3, _('Value 3'), "prop1's value3", "prop2's value3"

        EnumType.VAL1.value == 1
        EnumType.VAL1.name == 'VAL1'
        EnumType.VAL1.label == 'Value 1'
        EnumType.VAL1.prop1 == "prop1's value1"
        EnumType.VAL1.prop2 == "prop2's value1"
        EnumType("prop1's value1") # throws ValueError
        EnumType("prop2's value1") == EnumType.VAL1 == EnumType("PRoP2'S ValUE1")

    :param prop_name: The name of the property
    :param symmetric: If true, the enumeration will be able to be instantiated from this value
    :param case_sensitive: If false and symmetric and property is a string, instantiation from this value will be case
        insensitive
    :return: a named property class
    """
    return type(prop_name, (_Prop,), {'symmetric': symmetric, 'case_sensitive': case_sensitive})


class EnumProperties(ChoicesMeta):
    """A metaclass for creating enum choices with additional named properties for each value."""

    @classmethod
    def __prepare__(metacls, cls, bases, **kwargs):
        bases = list(bases)
        properties = []
        real_bases = []
        # these are properties that the enum can be instantiated from
        # i.e. MyEnum.VALUE1 is MyEnum(symmetrical property of VALUE1)
        symmetrical_properties = []
        for base in bases:
            if issubclass(base, _Prop):
                properties.append(base.__name__)
                if getattr(base, 'symmetric', False):
                    symmetrical_properties.append(
                        SymmetricProperty(name=base.__name__, case_sensitive=getattr(base, 'case_sensitive', True))
                    )
            else:
                real_bases.append(base)
        classdict = super().__prepare__(cls, tuple(real_bases))
        classdict._djenum_properties = properties
        classdict._djenum_symmetrical_properties = symmetrical_properties
        return classdict

    def __new__(metacls, classname, bases, classdict, **kwds):
        properties = {prop: [] for prop in getattr(classdict, '_djenum_properties', [])}
        symmetrical_properties = {prop.name: prop for prop in getattr(classdict, '_djenum_symmetrical_properties', [])}
        if properties:
            for key in classdict._member_names:
                value = classdict[key]
                assert isinstance(value, (list, tuple)) and len(value) > len(properties), f'{classname} enumeration ' \
                                                                                          f'members must be lists or ' \
                                                                                          f'tuples.'
                idx = -1
                for values in reversed(list(properties.values())):
                    values.append(value[idx])
                    idx -= 1

                # Use dict.__setitem__() to suppress defenses against double
                # assignment in enum's classdict and chop off our named properties
                # before passing up the chain
                dict.__setitem__(classdict, key, value[0:-len(properties) or None])
        cls = super().__new__(
            metacls,
            classname,
            tuple([base for base in bases if not issubclass(base, _Prop)]),
            classdict,
            **kwds
        )
        symmetric_lookup = classdict.get('_missing_map_', {})

        def add_sym_lookup(prop, p_val, enum_inst, case_sensitive):
            if not isinstance(p_val, Hashable):
                raise TypeError(
                    f'{cls}.{prop}:{p_val} is not hashable. Symmetrical enumeration properties must be hashable or a '
                    f'list of hashable values.'
                )
            symmetric_lookup[p_val] = enum_inst
            if not case_sensitive and isinstance(p_val, str):
                symmetric_lookup[p_val.upper()] = enum_inst

        coerce_types = []

        def add_coerce_type(typ):
            if typ not in coerce_types and isinstance(typ, Hashable) and not issubclass(typ, cls):
                coerce_types.append(typ)

        for val in cls:
            add_coerce_type(type(val.value))

        # we reverse to maintain precedence order for symmetrical lookups
        for prop in reversed(list(properties.keys())):
            values = properties[prop]
            setattr(cls, f'_value2{prop}_map_', dict(zip(cls._value2member_map_, values)))
            setattr(cls, prop, property(lambda self, prop=prop: getattr(cls, f'_value2{prop}_map_').get(self.value)))
            if prop in symmetrical_properties:
                for idx, val in enumerate(values):
                    enum_cls = list(cls._value2member_map_.values())[idx]
                    if isinstance(val, (set, list)):
                        for v in val:
                            add_coerce_type(type(v))
                            add_sym_lookup(prop, v, enum_cls, symmetrical_properties[prop].case_sensitive)
                    else:
                        add_sym_lookup(prop, val, enum_cls, symmetrical_properties[prop].case_sensitive)
                        add_coerce_type(type(val))

        setattr(cls, '_coerce_types_', coerce_types)
        if symmetric_lookup:
            setattr(cls, '_missing_map_', symmetric_lookup)
        return cls


class TextChoices(SymmetricMixin, DjangoTextChoices, metaclass=EnumProperties):
    pass


class IntegerChoices(SymmetricMixin, DjangoIntegerChoices, metaclass=EnumProperties):
    pass


class FloatChoices(SymmetricMixin, float, Choices, metaclass=EnumProperties):
    pass
