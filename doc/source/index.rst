=======================
Enum Properties
=======================

Add properties to Python enumeration values in a simple declarative syntax.
`enum-properties <https://pypi.python.org/pypi/enum-properties>`_ is a lightweight extension to
Python's :class:`enum.Enum` class. Example:

.. literalinclude:: ../../tests/examples/color_example.py


Properties may also be symmetrically mapped to enumeration values using
Symmetric type annotations:

.. literalinclude:: ../../tests/examples/symmetric_example.py


Member functions may also be specialized to each enumeration value, using the ``@specialize``
decorator:

.. literalinclude:: ../../tests/examples/specialization_example.py


Please report bugs and discuss features on the
`issues page <https://github.com/bckohan/enum-properties/issues>`_.

`Contributions <https://github.com/bckohan/enum-properties/blob/main/CONTRIBUTING.md>`_ are
encouraged!

`Full documentation at read the docs. <https://enum-properties.readthedocs.io>`_

Installation
------------

1. Clone enum-properties from `GitHub <https://github.com/bckohan/enum-properties>`_ or install a
   release off `pypi <https://pypi.python.org/pypi/enum-properties>`_:

.. code:: bash

       pip install enum-properties

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howto
   tutorial
   reference
   changelog
