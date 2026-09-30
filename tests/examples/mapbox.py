import typing as t
from enum_properties import EnumProperties as Enum, s, Symmetric, symmetric


class MapBoxStyle(Enum):
    """
    https://docs.mapbox.com/api/maps/styles/
    """

    # we may also mark name symmetric by including a type hint for it
    name: t.Annotated[str, Symmetric(case_fold=True)]

    # type hints specify our additional enum instance properties
    label: t.Annotated[str, Symmetric(case_fold=True)]
    """
    The human-readable label for this style.
    """

    version: int
    """
    The most recent version of this style.
    """

    # name               value                 label           version
    STREETS           = 'streets',           'Streets',           12
    OUTDOORS          = 'outdoors',          'Outdoors',          12
    LIGHT             = 'light',             'Light',             11
    DARK              = 'dark',              'Dark',              11
    SATELLITE         = 'satellite',         'Satellite',          9
    SATELLITE_STREETS = 'satellite-streets', 'Satellite Streets', 12
    NAVIGATION_DAY    = 'navigation-day',    'Navigation Day',     1
    NAVIGATION_NIGHT  = 'navigation-night',  'Navigation Night',   1

    # we can define a normal property to produce property values based
    # off other properties! We can even use the symmetric decorator to make it symmetric
    @symmetric()
    @property
    def uri(self) -> str:
        """
        The URI identifier for this style to be used in API calls.
        """
        return f'mapbox://styles/mapbox/{self.value}-v{self.version}'

    def __str__(self):
        return self.uri


assert MapBoxStyle.LIGHT.uri == 'mapbox://styles/mapbox/light-v11'

# uri's are symmetric
assert MapBoxStyle('mapbox://styles/mapbox/light-v11') is MapBoxStyle.LIGHT

# so are labels (also case insensitive)
assert MapBoxStyle('satellite streets') is MapBoxStyle.SATELLITE_STREETS

# when used in API calls (coerced to strings) - they "do the right thing"
assert str(MapBoxStyle.DARK) == 'mapbox://styles/mapbox/dark-v11'
