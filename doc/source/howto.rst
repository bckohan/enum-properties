.. _usage:

======
How To
======

Add Properties to an Enum
-------------------------

To add properties to an enumeration you must inherit from
:py:class:`~enum_properties.EnumProperties` or :py:class:`~enum_properties.IntEnumProperties`
instead of :class:`enum.Enum` and :class:`enum.IntEnum`, list property values in a tuple with each
enumeration value and let :py:class:`~enum_properties.EnumProperties` know that your properties
exist and what their names are by adding type hints to the Enum class definition before the
enumeration values. **The type hints must be in the same order as property values are listed in the
value tuples:**

.. warning::

    A :class:`ValueError` will be thrown if the length of any value tuple does not
    match the number of expected properties. If a given enumeration value does
    not have a property, None should be used.

For example:

.. literalinclude:: ../../tests/examples/howto_add_props.py

.. tip::

    The property type hints must be specified before the enumeration values to become properties.
    If you would like a type hint on your enumeration that are not properties, you may specify the
    hint after the value definitions.

Use a metaclass instead
~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`~enum_properties.EnumProperties` inherits from enum and all other standard python
enumeration functionality will work. The :py:class:`~enum_properties.EnumProperties` base class is
equivalent to:

.. literalinclude:: ../../tests/examples/howto_metaclass.py
    :lines: 2-7


Get Enums from their properties
-------------------------------

For some enumerations it will make sense to be able to fetch an enumeration value instance
from one of the property values. **This is called property symmetry**. To mark a property as
symmetric, annotate your type hint with :py:class:`~enum_properties.Symmetric`:

.. literalinclude:: ../../tests/examples/howto_symmetry.py

.. tip::

    Symmetric string properties are by default case sensitive. To mark a property as case
    insensitive, use the ``case_fold=True`` parameter on the :py:class:`~enum_properties.Symmetric`
    dataclass.

``case_fold`` will more than just make matching case insensitive. It will store the string using
the `unicode standard Normalization Form Compatibility Decomposition (NFKD) algorithm
<https://unicode.org/reports/tr15>`_. This breaks down characters into their canonical components.
For example, accented characters like "é" are decomposed to "e". This is particularly useful when
you want to compare strings or search text in a way that ignores differences in case and
accent/diacritic representations.

For futher reading, here's `more than you ever wanted to know about unicode
<https://tonsky.me/blog/unicode>`_.

.. tip::

    By default, none values for symmetric properties will not be symmetric. To change this behavior
    pass: ``match_none=True`` to :py:class:`~enum_properties.Symmetric`.

.. warning::

    Any object may be a property value, but symmetric property values must be hashable. A
    :class:`ValueError` will be thrown if they are not.

An exception to this is that symmetric property values may be a list or set of hashable values.
Each value in the list will be symmetric to the enumeration value. Tuples are hashable and are
treated as singular property values. See the ``AddressRoute`` example in :ref:`examples`.

:py:class:`~enum_properties.SymmetricMixin` tries very hard to resolve enumeration values from
objects. Type coercion to all potential value types will be attempted before giving up. For
instance, if we have a hex object that is coercible to a string hex value we could instantiate our
Color enumeration from it and perform equality comparisons:

.. literalinclude:: ../../tests/examples/howto_symmetry.py
    :lines: 20-24


.. warning::

    Using symmetric properties with @verify(UNIQUE) will raise an error:

    .. literalinclude:: ../../tests/examples/howto_verify_unique.py


Use a metaclass instead
~~~~~~~~~~~~~~~~~~~~~~~

Symmetric property support is added through the :py:class:`~enum_properties.SymmetricMixin` class
which is included in the :py:class:`~enum_properties.EnumProperties` base class. If you are using
the metaclass you must also inherit from :py:class:`~enum_properties.SymmetricMixin`:

.. literalinclude:: ../../tests/examples/howto_symmetric_metaclass.py
    :lines: 2-7

Handle Symmetric Overloads
--------------------------

Symmetric properties need not be unique. Resolution by value is deterministic based on the
following priority order:

1) Type Specificity
    Any value that matches a property value without a type coercion will take precedence over
    values that match after type coercion.
2) Left to right.
    Any value with a smaller tuple index will override any value with a larger tuple index
3) Nested left to right.
    Any value in a list or set of symmetric values will override values with larger indexes in
    corresponding property values.

.. literalinclude:: ../../tests/examples/howto_symmetric_overload.py


Mark ``name`` as Symmetric
--------------------------

When extending from :class:`enum.Enum` or other enumeration base classes, some builtin properties
are available. `name` is available on all standard :class:`enum.Enum` classes. By default
:py:class:`~enum_properties.EnumProperties` will make `name` case sensitive symmetric. To override
this behavior, you may add a type hint for ``name`` before your added property type hints. For
example to make name case insensitive we might:

.. literalinclude:: ../../tests/examples/howto_symmetric_builtins.py


Mark @properties as Symmetric
-----------------------------

The :py:func:`~enum_properties.symmetric` decorator may be used to mark @properties as symmetric or other members not specified
in the Enum value tuple as symmetric. For example:

.. literalinclude:: ../../tests/examples/howto_symmetric_decorator.py


Specializing Member Functions
-----------------------------

Provide specialized implementations of member functions using the specialize decorator. For
example:

.. literalinclude:: ../../tests/examples/howto_specialized.py

The :py:meth:`~enum_properties.specialize` decorator works on ``@classmethods`` and
``@staticmethods`` as well, but it must be the outermost decorator.

The undecorated method will apply to all members that lack a specialization:

.. literalinclude:: ../../tests/examples/howto_specialized_default.py

If no undecorated method or specialization for a value is found that value will
lack the method.

.. literalinclude:: ../../tests/examples/howto_specialized_missing.py

:py:meth:`~enum_properties.specialize` will also accept a list so that multiple enumeration values
can share the same specialization.

.. literalinclude:: ../../tests/examples/howto_specialized_list.py


Flags
-----

:class:`enum.IntFlag` and :class:`enum.Flag` types that support properties are also provided by the
:py:class:`~enum_properties.IntFlagProperties` and :py:class:`~enum_properties.FlagProperties`
classes. For example:

.. literalinclude:: ../../tests/examples/howto_flag.py
    :lines: 1-24

Flag enumerations can also be created from iterables and generators containing values or symmetric
values.

.. literalinclude:: ../../tests/examples/howto_flag.py
    :lines: 26-43

.. note::

    Iterable instantiation on flags is added using the :py:class:`~enum_properties.DecomposeMixin`.
    To create a flag enumeration without the iterable extensions we can simply declare it manually
    without the mixin:

    .. literalinclude:: ../../tests/examples/howto_flags_no_iterable.py
        :lines: 1-10


As of Python 3.11 `boundary values <https://docs.python.org/3/library/enum.html#enum.FlagBoundary>`_
are supported on flags. Boundary specifiers must be supplied as named arguments:

.. literalinclude:: ../../tests/examples/howto_flag_boundaries.py


Use Nested Classes as Enums
---------------------------

You can use nested classes as enumeration values. The tricky part is keeping them from becoming
values themselves.

On enums that inherit from :class:`enum.Enum` in python < 3.13 nested classes become
enumeration values because types may be values and a quirk of Python makes it
difficult to determine if a type on a class is declared as a nested class
during __new__. For enums with properties we can distinguish declared classes
because values must be tuples.

Note that on 3.13 and above you must use the nonmember/member decorators. Also note that
the position of ``label`` is important.

.. tabs::

    .. tab:: <3.13

        .. literalinclude:: ../../tests/examples/howto_nested_classes.py

    .. tab:: >=3.11 (required >=3.13)

        .. literalinclude:: ../../tests/examples/howto_nested_classes_313.py


What about dataclass Enums?
---------------------------

As of Python 3.12, `Enum values can be
<https://docs.python.org/howto/enum.html#enum-dataclass-support>`_ :mod:`python:dataclasses`. At
first glance this enables some behavior that is similar to adding properties. For example:

.. literalinclude:: ../../tests/examples/howto_dataclass.py

**We still recommend EnumProperties as the preferred way to add additional attributes to a Python
enumeration for the following reasons:**

- The value of ``BEETLE`` and ``DOG`` in the above example are instances
  of the ``CreatureDataMixin`` dataclass. This can complicate interfacing
  with other systems (like databases) where it is more natural for the
  enumeration value to be a small primitive type like a character or
  integer.

- The dataclass method requires two classes where a single ``EnumProperties``
  class will suffice.

- :mod:`python:dataclasses` are not hashable by default which can complicate equality
  testing and marshalling external data into enumeration values.

- Many code bases that use duck typing and that work with Enums expect the ``value``
  attribute to be a a plain old data type and therefore serializable.

.. note::

    EnumProperties also integrates with Enum's dataclass support!
    For example we can add a symmetric property to the Creature
    enumeration like so:

.. literalinclude:: ../../tests/examples/howto_dataclass_integration.py


Define hash equivalent enums
----------------------------

The :class:`enum.Enum` types that inherit from primitive types :class:`int` and :class:`str` are
hash equivalent to their primitive types. This means that they can be used interchangeably in
collections that use hashing:

.. literalinclude:: ../../tests/examples/howto_hash_equiv.py

:py:class:`~enum_properties.IntEnumProperties`, :py:class:`~enum_properties.StrEnumProperties` and
:py:class:`~enum_properties.IntFlagProperties` also honor this hash equivalency. When defining your
own symmetric enumeration types if you want to keep hash equivalency to the value type you will
you will have to implement this yourself. For example, if you wanted your color enumeration to also
be an rgb tuple:

.. literalinclude:: ../../tests/examples/howto_hash_equiv_def.py

Use the legacy (1.x) API
------------------------

The legacy (1.x) way of specifying properties using :py:meth:`~enum_properties.p` and
:py:meth:`~enum_properties.s` value inheritance is still supported. If any properties
are defined this way it will take precedence over type hinting and the type hints will
not be interpreted as properties. For example:

.. literalinclude:: ../../tests/examples/howto_legacy.py
