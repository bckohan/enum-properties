"""
Support for symmetrical property enumeration types derived from Django choice
types. These choices types are drop in replacements for the Django
IntegerChoices and TextChoices.
"""
from enum_properties import (
    SymmetricMixin,
    EnumProperties
)
try:

    from django.db.models import Choices
    from django.db.models import IntegerChoices as DjangoIntegerChoices
    from django.db.models import TextChoices as DjangoTextChoices
    from django.db.models.enums import ChoicesMeta

    class DjangoEnumProperties(EnumProperties, ChoicesMeta):
        """Derive """
        pass


    class TextChoices(
        SymmetricMixin,
        DjangoTextChoices,
        metaclass=DjangoEnumProperties
    ):
        pass


    class IntegerChoices(
        SymmetricMixin,
        DjangoIntegerChoices,
        metaclass=DjangoEnumProperties
    ):
        pass


    class FloatChoices(
        SymmetricMixin,
        float,
        Choices,
        metaclass=DjangoEnumProperties
    ):
        pass

except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
