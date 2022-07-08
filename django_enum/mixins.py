
class SymmetricMixin:

    _missing_map_ = {}
    _symmetric_properties_ = {'name', 'label'}

    @classmethod
    def _missing_(cls, value):

        if value in cls._missing_map_:
            return cls._missing_map_[value]

        if isinstance(value, str):
            if value.upper() in cls._missing_map_:
                return cls._missing_map_[value.upper()]

        for prop in getattr(cls, '_symmetric_properties_', set()):
            for en in cls:
                if hasattr(en, prop) and getattr(en, prop) == value:
                    return en

        for typ in getattr(cls, '_coerce_types_', []):
            if typ is not type(value) and typ is not cls:
                try:
                    return cls(typ(value))
                except ValueError:
                    pass

        return super()._missing_(value)
