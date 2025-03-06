.. include:: refs.rst

=======================
Enum Properties
=======================

Add properties to Python enumeration values in a simple declarative syntax.
Enum Properties is a lightweight extension to Python's Enum_ class. Example:

.. code:: python

    import typing as t
    from enum_properties import EnumProperties
    from enum import auto

    class Color(EnumProperties):

        rgb: t.Tuple[int, int, int]
        hex: str

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # the type hints on the Enum class become properties on
    # each value, matching the order in which they are specified

    Color.RED.rgb   == (1, 0, 0)
    Color.GREEN.rgb == (0, 1, 0)
    Color.BLUE.rgb  == (0, 0, 1)

    Color.RED.hex   == 'ff0000'
    Color.GREEN.hex == '00ff00'
    Color.BLUE.hex  == '0000ff'

Properties may also be symmetrically mapped to enumeration values using
Symmetric type annotations:

.. code:: python

    import typing as t
    from enum_properties import EnumProperties, Symmetric
    from enum import auto

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # Enumeration instances may be instantiated from any Symmetric property
    # values. Use case_fold for case insensitive matching

    Color((1, 0, 0)) is Color.RED
    Color((0, 1, 0)) is Color.GREEN
    Color((0, 0, 1)) is Color.BLUE

    Color('ff0000') is Color.RED
    Color('FF0000') is Color.RED  # case_fold makes mapping case insensitive
    Color('00ff00') is Color.GREEN
    Color('00FF00') is Color.GREEN
    Color('0000ff') is Color.BLUE
    Color('0000FF') is Color.BLUE

    Color.RED.hex == 'ff0000'

Please report bugs and discuss features on the
`issues page <https://github.com/bckohan/enum-properties/issues>`_.

`Contributions <https://github.com/bckohan/enum-properties/blob/main/CONTRIBUTING.rst>`_ are
encouraged!

`Full documentation at read the docs. <https://enum-properties.readthedocs.io/en/latest/>`_

Installation
------------

1. Clone enum-properties from GitHub_ or install a release off PyPI_ :

.. code:: bash

       pip install enum-properties

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   examples
   reference
   changelog
