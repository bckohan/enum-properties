=======================
Enum Properties
=======================

|MIT license| |Ruff| |PyPI version fury.io| |PyPI pyversions| |PyPI status|
|PyPi Typed| |Documentation Status| |Code Cov| |Test Status| |Lint Status|


|OpenSSF Scorecard| |OpenSSF Best Practices|

.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/

.. |Ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://docs.astral.sh/ruff

.. |PyPI version fury.io| image:: https://badge.fury.io/py/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties/

.. |PyPI status| image:: https://img.shields.io/pypi/status/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties

.. |PyPI Typed| image:: https://img.shields.io/pypi/types/enum-properties.svg
   :target: https://pypi.python.org/pypi/enum-properties

.. |Documentation Status| image:: https://readthedocs.org/projects/enum-properties/badge/?version=latest
   :target: http://enum-properties.readthedocs.io/?badge=latest/

.. |Code Cov| image:: https://codecov.io/gh/bckohan/enum-properties/branch/main/graph/badge.svg?token=0IZOKN2DYL
   :target: https://codecov.io/gh/bckohan/enum-properties

.. |Test Status| image:: https://github.com/bckohan/enum-properties/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/bckohan/enum-properties/actions/workflows/test.yml

.. |Lint Status| image:: https://github.com/bckohan/enum-properties/actions/workflows/lint.yml/badge.svg
   :target: https://github.com/bckohan/enum-properties/actions/workflows/lint.yml

.. |OpenSSF Scorecard| image:: https://api.securityscorecards.dev/projects/github.com/bckohan/enum-properties/badge
   :target: https://securityscorecards.dev/viewer/?uri=github.com/bckohan/enum-properties

.. |OpenSSF Best Practices| image:: https://www.bestpractices.dev/projects/12046/badge
   :target: https://www.bestpractices.dev/projects/12046


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
