try:
    from django_filters import ChoiceFilter
    from django_filters import filterset
    from enum_properties.django.forms import EnumChoiceField
    from enum_properties.django.fields import _EnumMixin


    class EnumFilter(ChoiceFilter):
        field_class = EnumChoiceField

        def __init__(self, *, enum, **kwargs):
            self.enum = enum
            super().__init__(enum=enum, choices=self.enum.choices, **kwargs)


    class FilterSet(filterset.FilterSet):

        @classmethod
        def filter_for_lookup(cls, field, lookup_type):
            if isinstance(field, _EnumMixin) and getattr(field, 'enum', None):
                return EnumFilter, {'enum': field.enum}
            return super().filter_for_lookup(field, lookup_type)


except (ImportError, ModuleNotFoundError):
    pass
