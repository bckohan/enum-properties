import typing as t
from enum_properties import EnumProperties as Enum, s, Symmetric


class MapBoxStyle(Enum):
    """
    https://docs.mapbox.com/api/maps/styles/
    """

    # we may also mark builtins and normal properties as symmetric using
    # the _symmetric_builtins_ attribute
    _symmetric_builtins_ = [s('name', case_fold=True), 'uri']

    # type hints specify our additional enum instance properties
    label: t.Annotated[str, Symmetric(case_fold=True)]
    version: int

    # name               value                 label           version
    STREETS           = 'streets',           'Streets',           11
    OUTDOORS          = 'outdoors',          'Outdoors',          11
    LIGHT             = 'light',             'Light',             10
    DARK              = 'dark',              'Dark',              10
    SATELLITE         = 'satellite',         'Satellite',          9
    SATELLITE_STREETS = 'satellite-streets', 'Satellite Streets', 11
    NAVIGATION_DAY    = 'navigation-day',    'Navigation Day',     1
    NAVIGATION_NIGHT  = 'navigation-night',  'Navigation Night',   1

    # we can define a normal property to produce property values based
    # off other properties!
    @property
    def uri(self) -> str:
        return f'mapbox://styles/mapbox/{self.value}-v{self.version}'

    def __str__(self):
        return self.uri


assert MapBoxStyle.LIGHT.uri == 'mapbox://styles/mapbox/light-v10'

# uri's are symmetric
assert MapBoxStyle('mapbox://styles/mapbox/light-v10') is MapBoxStyle.LIGHT

# so are labels (also case insensitive)
assert MapBoxStyle('satellite streets') is MapBoxStyle.SATELLITE_STREETS

# when used in API calls (coerced to strings) - they "do the right thing"
assert str(MapBoxStyle.DARK) == 'mapbox://styles/mapbox/dark-v10'
