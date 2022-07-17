from django.forms.fields import ChoiceField
from django.core.exceptions import ValidationError


class EnumChoiceField(ChoiceField):

    def __init__(self, enum, *, empty_value='', choices=(), **kwargs):
        self.enum = enum
        self.empty_value = empty_value
        super().__init__(
            choices=choices or getattr(self.enum, 'choices', ()),
            **kwargs
        )

    def _coerce(self, value):
        """
        Validate that the value is coercible to the enumeration type.
        """
        if value == self.empty_value or value in self.empty_values:
            return self.empty_value
        try:
            value = self.enum(value).value
        except (ValueError, TypeError, ValidationError):
            raise ValidationError(
                f'{value} is not a valid {self.enum}.',
                code='invalid_choice',
                params={'value': value},
            )
        return value

    def clean(self, value):
        return super().clean(self._coerce(value))
