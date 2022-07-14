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
        DjangoEnumProperties
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
        'DjangoEnumProperties',
        'DJANGO_SUPPORTED'
    ]
except (ModuleNotFoundError, ImportError):  # pragma: no cover
    DJANGO_SUPPORTED = False
