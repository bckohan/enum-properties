==========
Change Log
==========

v2.0.1 (02-SEP-2024)
====================

* Misc readme/doc updates.
* Fixed `Break tests into smaller files. <https://github.com/bckohan/enum-properties/issues/71>`_

v2.0.0 (02-SEP-2024)
====================

* Implemented `Allow properties to be specified through type hints alone without s/p value inheritance <https://github.com/bckohan/enum-properties/issues/60>`_

v1.8.1 (29-AUG-2024)
====================

* Fixed `Add missing py.typed <https://github.com/bckohan/enum-properties/issues/62>`_

v1.8.0 (26-AUG-2024)
====================

* Implemented `Drop support for Python 3.7 <https://github.com/bckohan/enum-properties/issues/59>`_
* Implemented `Support Python 3.13 <https://github.com/bckohan/enum-properties/issues/58>`_
* Implemented `Move to ruff for linting and formatting. <https://github.com/bckohan/enum-properties/issues/57>`_
* Documented `Support type hinting for properties <https://github.com/bckohan/enum-properties/issues/42>`_

v1.7.0 (02-OCT-2023)
====================

* Implemented `Add a StrEnumProperties type to match StrEnum. <https://github.com/bckohan/enum-properties/issues/54>`_
* Fixed `Hash equivalency between values and enums is broken. <https://github.com/bckohan/enum-properties/issues/53>`_
* Implemented `Test mixed primitive type values. <https://github.com/bckohan/enum-properties/issues/46>`_

v1.6.0 (22-AUG-2023)
====================

* Implemented `Support dataclasses in enums along with Python 3.12 <https://github.com/bckohan/enum-properties/issues/52>`_

v1.5.2 (06-MAY-2023)
====================

* Fixed `_missing_ allows exceptions through that are not ValueError, TypeError or KeyError <https://github.com/bckohan/enum-properties/issues/47>`_

v1.5.1 (17-APR-2023)
====================

* Fixed `Symmetric string 'none' values enable coercion from None despite match_none=False <https://github.com/bckohan/enum-properties/issues/45>`_

v1.5.0 (15-APR-2023)
====================

There is one minimally impactful breaking change in the 1.5.0 release:

* Symmetric properties that are None will not map back to the enumeration value
  by default. To replicate the previous behavior, pass True as the `match_none`
  argument when instantiating the property with s().

The 1.5.0 release includes two feature improvements:

* Implemented `Configurable behavior for matching none on symmetric fields <https://github.com/bckohan/enum-properties/issues/44>`_
* Implemented `Allow @specialize to accept a list of enumeration values. <https://github.com/bckohan/enum-properties/issues/43>`_

v1.4.0 (08-APR-2023)
====================

There are some breaking changes in the 1.4.0 release:

* The `enum_properties` attribute that lists property names has been changed to
  the sunder name `_properties_`.

* Properties on combinations of flag enumerations that are not specified in
  the members list instead of being None, no longer exist. Accessing them will
  result in an AttributeError.

The 1.4.0 release includes some significant performance improvements. Property
access speed has been improved by over 5x and the memory footprint has
been reduced by about 1/3.

* Fixed `All utility members added by EnumProperties should be sunder names. <https://github.com/bckohan/enum-properties/issues/41>`_
* Fixed `auto() broken for flag enums that declare combinations as members of the enum. <https://github.com/bckohan/enum-properties/issues/40>`_
* Implemented `Performance improvements <https://github.com/bckohan/enum-properties/issues/39>`_
* Implemented `Provide a decorator to provide function overrides per enum value. <https://github.com/bckohan/enum-properties/issues/36>`_
* Fixed `Address python 3.11+ deprecation warnings. <https://github.com/bckohan/enum-properties/issues/38>`_
* Fixed `New flag behavior modifiers break IntFlagProperties in python 3.11+ <https://github.com/bckohan/enum-properties/issues/37>`_


v1.3.3 (15-FEB-2023)
====================

* Fixed `LICENSE included in source package. <https://github.com/bckohan/enum-properties/issues/30>`_


v1.3.2 (15-FEB-2023)
====================

* Fixed `Nested classes are incompatible with EnumProperties. <https://github.com/bckohan/enum-properties/issues/29>`_


v1.3.1 (25-OCT-2022)
====================

* Fixed `Remove errant print statement <https://github.com/bckohan/enum-properties/issues/20>`_


v1.3.0 (25-OCT-2022)
====================

* Fixed `Initialize Flag enum with empty iterable should resolve to Flag(0) - no selections. <https://github.com/bckohan/enum-properties/issues/19>`_
* Added `Support for python 3.11. <https://github.com/bckohan/enum-properties/issues/18>`_
* Implemented `Generally allow composite flag enumerations to be treated as iterables of active flags. <https://github.com/bckohan/enum-properties/issues/17>`_

v1.2.2 (25-OCT-2022)
====================

* Implemented `Add convenience property to decompose Flag enumeration values <https://github.com/bckohan/enum-properties/issues/16>`_

v1.2.1 (25-OCT-2022)
====================

* Implemented `Allow Flag Enumerations to be created from iterables <https://github.com/bckohan/enum-properties/issues/15>`_

v1.2.0 (17-AUG-2022)
====================

* Implemented `Drop support for < Python3.6 <https://github.com/bckohan/enum-properties/issues/6>`_
* Fixed `Add types and support for Flag and IntFlag <https://github.com/bckohan/enum-properties/issues/5>`_

v1.1.1 (24-JUL-2022)
====================

* Fixed `SymmetricMixin objects are not hashable <https://github.com/bckohan/enum-properties/issues/4>`_

v1.1.0 (23-JUL-2022)
====================

* Implemented `Provide equality comparisons for symmetric property values <https://github.com/bckohan/enum-properties/issues/3>`_

v1.0.2 (19-JUL-2022)
====================

* Fixed `Consolidate source files <https://github.com/bckohan/enum-properties/issues/1>`_

v1.0.1 (18-JUL-2022)
====================

* Include readme in package

v1.0.0 (18-JUL-2022)
====================

* Initial Release (production/stable)
