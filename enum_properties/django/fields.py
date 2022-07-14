"""
Support for Django model fields built from enumeration types.
"""
try:
    from django.core.exceptions import ValidationError
    from django.db.models import (
        BigIntegerField,
        CharField,
        Choices,
        FloatField,
        IntegerField,
        PositiveBigIntegerField,
        PositiveIntegerField,
        PositiveSmallIntegerField,
        SmallIntegerField,
    )

    class _EnumMixin:

        enum = None

        def __init__(self, *args, enum, **kwargs):
            self.enum = enum
            kwargs.setdefault('choices', self.enum.choices)
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs['enum'] = self.enum
            return name, path, args, kwargs

        def get_prep_value(self, value):
            if value is not None:
                if not isinstance(value, self.enum):
                    try:
                        value = self.enum(value).value
                    except (TypeError, ValueError) as e:
                        raise ValueError(
                            f"Field '{self.name}' expected a "
                            f"'{self.enum.__name__}' but got '{value}'.",
                        ) from e
                else:
                    value = value.value
            return super().get_prep_value(value)

        def get_db_prep_value(self, value, connection, prepared=False):
            if value is not None:
                if not isinstance(value, self.enum):
                    try:
                        value = self.enum(value).value
                    except (TypeError, ValueError) as e:
                        raise ValueError(
                            f"Field '{self.name}' expected a "
                            f"'{self.enum.__name__}' but got '{value}'.",
                        ) from e
                else:
                    value = value.value
            return super().get_db_prep_value(
                value,
                connection,
                prepared
            )

        def from_db_value(self, value, expression, connection):
            if value is None:  # pragma: no cover
                return value
            return self.enum(value)

        def to_python(self, value):
            if isinstance(value, self.enum) or value is None:
                return value

            try:
                return self.enum(value)
            except (TypeError, ValueError) as ve:
                raise ValidationError(
                    f"'{value}' is not a valid {self.enum.__name__}."
                )

        def validate(self, value, model_instance):
            try:
                super().validate(value, model_instance)
            except ValidationError as ve:
                if ve.code != 'invalid_choice':
                    raise ve
            try:
                self.to_python(value)
            except ValidationError as ve:
                raise ValidationError(
                    ve.message,
                    code='invalid_choice',
                    params={'value': value}
                )


    class EnumCharField(_EnumMixin, CharField):

        def __init__(self, *args, enum, **kwargs):
            kwargs.setdefault(
                'max_length',
                max([len(define.value) for define in enum])
            )
            super().__init__(*args, enum=enum, **kwargs)


    class EnumFloatField(_EnumMixin, FloatField):
        pass


    class EnumSmallIntegerField(_EnumMixin, SmallIntegerField):
        pass


    class EnumPositiveSmallIntegerField(_EnumMixin, PositiveSmallIntegerField):
        pass


    class EnumPositiveIntegerField(_EnumMixin, PositiveIntegerField):
        pass


    class EnumPositiveBigIntegerField(_EnumMixin, PositiveBigIntegerField):
        pass


    class EnumIntegerField(_EnumMixin, IntegerField):
        pass


    class EnumBigIntegerField(_EnumMixin, BigIntegerField):
        pass


    class _EnumFieldMetaClass(type):

        SUPPORTED_PRIMITIVES = {int, str, float}

        def __new__(cls, enum):
            """
            Construct a new Django Field class given the Enumeration class. The
            correct Django field class to inherit from is determined based on the
            primitive type seen in the Enumeration class's inheritance tree.

            :param enum: The class of the Enumeration to build a field class for
            """
            assert issubclass(enum, Choices), \
                f'{enum} must inherit from {Choices}!'
            primitive = cls.SUPPORTED_PRIMITIVES.intersection(set(enum.__mro__))
            assert len(primitive) == 1, f'{enum} must inherit from exactly one ' \
                                        f'supported primitive type ' \
                                        f'{cls.SUPPORTED_PRIMITIVES}'

            primitive = list(primitive)[0]

            if primitive is float:
                return EnumFloatField
            elif primitive is int:
                values = [define.value for define in enum]
                min_value = min(values)
                max_value = max(values)
                if min_value < 0:
                    if min_value < -2147483648 or max_value > 2147483647:
                        return EnumBigIntegerField
                    elif min_value < -32768 or max_value > 32767:
                        return EnumIntegerField
                    else:
                        return EnumSmallIntegerField
                else:
                    if max_value > 2147483647:
                        return EnumPositiveBigIntegerField
                    elif max_value > 32767:
                        return EnumPositiveIntegerField
                    else:
                        return EnumPositiveSmallIntegerField

            return EnumCharField


    def EnumField(enum, **field_kwargs):
        """
        Some syntactic sugar that wraps the enum field metaclass so that we can
        cleanly create enums like so:

        .. code-block::

        class MyModel(models.Model):

            class EnumType(IntegerChoices):

                VAL1 = 1, _('Value 1')
                VAL2 = 2, _('Value 2')
                VAL3 = 3, _('Value 3')

            field_name = EnumField(EnumType)

        :param enum: The class of the enumeration.
        :param field_kwargs: Any standard
        :return: An object of the appropriate enum field type
        """
        return _EnumFieldMetaClass(enum)(enum=enum, **field_kwargs)

except (ImportError, ModuleNotFoundError):
    pass
