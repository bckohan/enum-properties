.. _ref-examples:

========
Examples
========

Enumerations in Python can provide rich class based interfaces, well suited
to many scenarios. Two examples are presented here that make use of enum
properties to encapsulate more information and get our enums to do more work
for us.

Address Unit Designator
_______________________



Map Box Style
_____________

.. code-block:: python

    class MapBoxStyle(
        EnumProperties,
        s('label', case_fold=True),
        p('version')
    ):
        """
        https://docs.mapbox.com/api/maps/styles/
        """
        _symmetric_builtins_ = ['name', 'url']

        STREETS = 'streets', 'Streets', 11
        OUTDOORS = 'outdoors', 'Outdoors', 11
        LIGHT = 'light', 'Light', 10
        DARK = 'dark', 'Dark', 10
        SATELLITE = 'satellite', 'Satellite', 9
        SATELLITE_STREETS = 'satellite-streets', 'Satellite Streets', 11
        NAVIGATION_DAY = 'navigation-day', 'Navigation Day', 1
        NAVIGATION_NIGHT = 'navigation-night', 'Navigation Night', 1

        @property
        def url(self):
            return f'mapbox://styles/mapbox/{self.value}-v{self.version}'

        def __str__(self):
            return self.url
