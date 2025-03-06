# Enum Properties

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://badge.fury.io/py/enum-properties.svg)](https://pypi.python.org/pypi/enum-properties/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/enum-properties.svg)](https://pypi.python.org/pypi/enum-properties/)
[![PyPI status](https://img.shields.io/pypi/status/enum-properties.svg)](https://pypi.python.org/pypi/enum-properties)
[![Documentation Status](https://readthedocs.org/projects/enum-properties/badge/?version=latest)](http://enum-properties.readthedocs.io/?badge=latest/)
[![Code Cov](https://codecov.io/gh/bckohan/enum-properties/branch/main/graph/badge.svg?token=0IZOKN2DYL)](https://codecov.io/gh/bckohan/enum-properties)
[![Test Status](https://github.com/bckohan/django-enum/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/bckohan/enum-properties/actions/workflows/test.yml?query=branch:main)
[![Lint Status](https://github.com/bckohan/django-enum/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/bckohan/enum-properties/actions/workflows/lint.yml?query=branch:main)

Add properties to Python enumeration values with a simple declarative syntax. [Enum Properties](https://enum-properties.readthedocs.io/en/latest) is a lightweight extension to [Python's Enum class](https://docs.python.org/3/library/enum.html). Example:

```python

    import typing as t
    from enum_properties import EnumProperties as Enum
    from enum import auto

    class Color(Enum):

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

```

Properties may also be symmetrically mapped to enumeration values using annotated type hints:

```python

    import typing as t
    from enum_properties import EnumProperties as Enum, Symmetric
    from enum import auto

    class Color(Enum):

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

```

Member functions may also be specialized to each enumeration value, using the ``@specialize`` decorator.

```python

    from enum_properties import EnumProperties as Enum, specialize

    class SpecializedEnum(Enum):

        ONE   = 1
        TWO   = 2
        THREE = 3

        @specialize(ONE)
        def method(self):
            return 'method_one()'

        @specialize(TWO)
        def method(self):
            return 'method_two()'

        @specialize(THREE)
        def method(self):
            return 'method_three()'

    SpecializedEnum.ONE.method() == 'method_one()'
    SpecializedEnum.TWO.method() == 'method_two()'
    SpecializedEnum.THREE.method() == 'method_three()'

```

Please report bugs and discuss features on the [issues page](https://github.com/bckohan/enum-properties/issues).

[Contributions](https://github.com/bckohan/enum-properties/blob/main/CONTRIBUTING.rst) are encouraged!

[Full documentation at read the docs.](https://enum-properties.readthedocs.io/en/latest)

## Installation

1. Clone enum-properties from [GitHub](https://github.com/bckohan/enum-properties) or install a release off [PyPI](https://pypi.org/project/enum-properties/):

```bash
       pip install enum-properties
```
