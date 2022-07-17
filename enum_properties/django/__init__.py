"""Django integration module"""
try:
    from enum_properties.django.fields import (
        EnumField,
        EnumFloatField,
        EnumCharField,
        EnumSmallIntegerField,
        EnumIntegerField,
        EnumBigIntegerField,
        EnumPositiveSmallIntegerField,
        EnumPositiveIntegerField,
        EnumPositiveBigIntegerField
    )
    from enum_properties.django.choices import (
        TextChoices,
        IntegerChoices,
        FloatChoices,
        DjangoEnumPropertiesMeta
    )
    from enum_properties.django.forms import EnumChoiceField
    from enum_properties.django.filters import (
        EnumFilter,
        FilterSet
    )
    DJANGO_SUPPORTED = True

    __all__ = [
        'EnumField',
        'EnumFloatField',
        'EnumCharField',
        'EnumSmallIntegerField',
        'EnumIntegerField',
        'EnumBigIntegerField',
        'EnumPositiveSmallIntegerField',
        'EnumPositiveIntegerField',
        'EnumPositiveBigIntegerField',
        'TextChoices',
        'IntegerChoices',
        'FloatChoices',
        'DjangoEnumPropertiesMeta',
        'DJANGO_SUPPORTED',
        'EnumFilter',
        'FilterSet',
        'EnumChoiceField'
    ]
except (ModuleNotFoundError, ImportError):  # pragma: no cover
    DJANGO_SUPPORTED = False
