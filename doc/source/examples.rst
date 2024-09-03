.. include:: refs.rst

.. _examples:

========
Examples
========

Enumerations in Python can provide rich class based interfaces, well suited to many scenarios. Two
real world examples are presented here that leverage enum properties to encapsulate more
information and get our enums to do more work.

Address Route Type
__________________

The USPS maintains a `list <https://pe.usps.com/text/pub28/28apc_002.htm>`_ of valid route types
for United States addresses. We'd like to construct an address model that is searchable based on
route type. A natural (and space efficient!) choice to represent the route is an enumeration. The
USPS also maintains a list of official and common abbreviations for address routes. We'd like to
encapsulate this information and parsing logic directly into our enumeration. We might implement
it like so:

.. code-block:: python

    import typing as t
    from enum_properties import EnumProperties as Enum, Symmetric

    class AddressRoute(Enum):

        # name is a builtin property of Enum, we can override its case insensitivity
        name: t.Annotated[str, Symmetric(case_fold=True)]

        abbr: t.Annotated[str, Symmetric(case_fold=True)]
        alt: t.Annotated[t.List[str], Symmetric(case_fold=True)]

        # name  value    abbr         alt
        ALLEY   = 1,    'ALY', ['ALLEE', 'ALLY']
        AVENUE  = 2,    'AVE', ['AV', 'AVEN', 'AVENU', 'AVN', 'AVNUE']
        CIRCLE  = 3,    'CIR', ['CIRC', 'CIRCL', 'CRCL', 'CRCLE']

        # ... other types elided for brevity


The builtin ``name`` property is the long-form official name for the route. By default enum
properties does not make the ``name`` property case insensitive, so we override the default
behavior by specifying a type hint for it. We also add a case insensitive abbreviation property and
alt property. The alt property is a list of common alternative abbreviations. Now we can
instantiate our enum from any valid route name, abbreviation or common alternative like so:

.. code-block:: python

    AddressRoute('avenue') is AddressRoute('AVE') is AddressRoute('Aven') is AddressRoute.AVENUE

We use an integer literal as our enumeration values to save space if these enumerations need to be
persisted in a datastore by value. By specifying them directly instead of using ``auto()`` we
reserve the ability to add additional route types in alphabetical order without accidentally
invalidating any persisted data.

Map Box Style
_____________

`Mapbox <https://mapbox.com>`_ is a popular web mapping platform. It comes with a handful of
default map styles. An enumeration is a natural choice to represent these styles but the styles are
complicated by the fact that they are versioned and that when used as a parameter in the mapbox API
they are in a URI format that is overly verbose for a human friendly user interface.

Each mapbox style enumeration is therefore composed of 4 primary properties. A name slug used in
the URI, a human friendly label for the style, a version number for the style and the full URI
specification of the style. We might implement our style enumeration like so:

.. code-block:: python

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

We've used the style's name slug as the value of the enumeration. If storage was an issue
(e.g. database) we could have separated this out into a separate property called ``slug`` and used
a small integer or single character as the enumeration value. We've also added a symmetric case
insensitive human friendly label for each style and a version property.

The version numbers will increment over time, but we're only concerned with the most recent
versions, so we'll increment their values in this enumeration as they change. If this enumeration
is persisted by value, any version number updates exist only in code and will be picked up as those
persisted values are re-instantiated as ``MapBoxStyle`` enumerations.

The last property we've added is the ``uri`` property. We've added it as concrete property on the
class because it can be created from the slug and version. We could have specified it in the value
tuple but that would be very verbose and less
`DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_. To make this property symmetric we
added it to the ``_symmetric_builtins_`` list.

We can use our enumeration like so:

.. code-block:: python

    MapBoxStyle.LIGHT.uri == 'mapbox://styles/mapbox/light-v10'

    # uri's are symmetric
    MapBoxStyle('mapbox://styles/mapbox/light-v10') is MapBoxStyle.LIGHT

    # so are labels (also case insensitive)
    MapBoxStyle('satellite streets') is MapBoxStyle.SATELLITE_STREETS

    # when used in API calls (coerced to strings) - they "do the right thing"
    str(MapBoxStyle.DARK) == 'mapbox://styles/mapbox/dark-v10'
