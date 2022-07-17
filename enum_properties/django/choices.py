"""
Support for symmetrical property enumeration types derived from Django choice
types. These choices types are drop in replacements for the Django
IntegerChoices and TextChoices.
"""
from enum_properties import (
    SymmetricMixin,
    EnumPropertiesMeta,
    p
)
try:

    from django.db.models import Choices
    from django.db.models import IntegerChoices as DjangoIntegerChoices
    from django.db.models import TextChoices as DjangoTextChoices
    from django.db.models.enums import ChoicesMeta

    class DjangoEnumPropertiesMeta(EnumPropertiesMeta, ChoicesMeta):
        """Derive """
        pass

    class DjangoSymmetricMixin(SymmetricMixin):
        symmetrical_builtins = ['name', 'label']

    class TextChoices(
        DjangoSymmetricMixin,
        DjangoTextChoices,
        metaclass=DjangoEnumPropertiesMeta
    ):
        pass


    class IntegerChoices(
        DjangoSymmetricMixin,
        DjangoIntegerChoices,
        metaclass=DjangoEnumPropertiesMeta
    ):
        pass


    class FloatChoices(
        DjangoSymmetricMixin,
        float,
        Choices,
        metaclass=DjangoEnumPropertiesMeta
    ):
        pass

except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
