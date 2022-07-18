|MIT license| |PyPI version fury.io| |PyPI pyversions| |PyPI status| |Documentation Status|
|Code Cov| |Test Status|

.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/

.. |PyPI version fury.io| image:: https://badge.fury.io/py/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties/

.. |PyPI status| image:: https://img.shields.io/pypi/status/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties

.. |Documentation Status| image:: https://readthedocs.org/projects/enum-properties/badge/?version=latest
   :target: http://enum-properties.readthedocs.io/?badge=latest/

.. |Code Cov| image:: https://codecov.io/gh/bckohan/enum-properties/branch/main/graph/badge.svg?token=0IZOKN2DYL
   :target: https://codecov.io/gh/bckohan/enum-properties

.. |Test Status| image:: https://github.com/bckohan/enum-properties/workflows/test/badge.svg
   :target: https://github.com/bckohan/enum-properties/actions

Enum Properties
#######################

Add properties to Python enumeration values with a simple declarative syntax.
`Enum Properties <https://enum-properties.readthedocs.io/en/latest/>`_ is a
lightweight extension to
`Python's Enum class <https://docs.python.org/3/library/enum.html>`_. Example:

.. code:: python

    from enum_properties import EnumProperties, p
    from enum import auto

    class Color(EnumProperties, p('rgb'), p('hex')):

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # the named p() values in the Enum's inheritance become properties on
    # each value, matching the order in which they are specified

    Color.RED.rgb   == (1, 0, 0)
    Color.GREEN.rgb == (0, 1, 0)
    Color.BLUE.rgb  == (0, 0, 1)

    Color.RED.hex   == 'ff0000'
    Color.GREEN.hex == '00ff00'
    Color.BLUE.hex  == '0000ff'

Properties may also be symmetrically mapped to enumeration values, using
s() values:

.. code:: python

    from enum_properties import EnumProperties, s
    from enum import auto

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # any named s() values in the Enum's inheritance become properties on
    # each value, and the enumeration value may be instantiated from the
    # property's value

    Color((1, 0, 0)) == Color.RED
    Color((0, 1, 0)) == Color.GREEN
    Color((0, 0, 1)) == Color.BLUE

    Color('ff0000') == Color.RED
    Color('FF0000') == Color.RED  # case_fold makes mapping case insensitive
    Color('00ff00') == Color.GREEN
    Color('00FF00') == Color.GREEN
    Color('0000ff') == Color.BLUE
    Color('0000FF') == Color.BLUE

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


.. _GitHub: http://github.com/bckohan/enum-properties
.. _PyPI: http://pypi.python.org/pypi/enum-properties
