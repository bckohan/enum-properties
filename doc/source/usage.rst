.. _ref-usage:

=====
Usage
=====

To add properties to an enumeration you must inherit from `EnumProperties`
instead of `Enum`, list property values in a tuple with each enumeration value
and let EnumProperties know that you're properties exist and what their names
are by adding `p()` values to the base class list. The `p()` values must be in
the same order as property values are listed in the value tuples:

.. note::

    A ValueError will be thrown if the length of any value tuple does not match
    the number of expected properties. If a given enumeration value does not
    have a property, None should be used.

For example:

.. code:: python

    from enum_properties import EnumProperties, p
    from enum import auto

    class Color(EnumProperties, p('rgb'), p('hex')):

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # The property values are accessible by name on the enumeration values:
    Color.RED.hex == 'ff0000'

`EnumProperties` inherit from enum and all other standard python enumeration
functionality will also work.

The `EnumProperties` base class is equivalent to doing this:

.. code:: python

    from enum_properties import EnumPropertiesMeta, p
    from enum import Enum, auto

    class Color(Enum, p('rgb'), p('hex'), metaclass=EnumPropertiesMeta):
        ...


Symmetry
--------

For some enumerations it will make sense to be able to instantiate an
enumeration value instance from one of the property values. This is called
property symmetry. To mark a property as symmetric, use `s()` values instead
of `p()` values:

.. code:: python

    from enum_properties import EnumProperties, s
    from enum import auto

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    Color.RED == Color((1, 0, 0)) == Color('FF0000') == Color('ff0000')

Symmetric string properties are by default case sensitive. To mark a property
as case insensitive, use the `case_fold=True` parameter on the `s()` value.

Symmetric property support is added through the `SymmetricMixin` class which is
included in the `EnumProperties` base class. Thus the above is equivalent to
this:

.. code:: python

    from enum_properties import EnumPropertiesMeta, SymmetricMixin, s
    from enum import Enum, auto

    class Color(SymmetricMixin, Enum, s('rgb'), s('hex', case_fold=True), metaclass=EnumPropertiesMeta):
        ...

.. warning::

    Any object may be a property value, but symmetric property values must be
    hashable. A ValueError will be thrown if they are not.

An exception to this is that symmetric property values may be a list or set of
hashable values. Each value in the list will be symmetric to the enumeration
value. Tuples are hashable and are treated as singular property values. See the
``AddressRoute`` example in :ref:`examples`.

`SymmetricMixin` tries very hard to resolve enumeration values from objects.
Type coercion to all potential value types will be attempted before giving up.
For instance, if we have a color object that is coercible to a string hex value
we could instantiate our Color enumeration from it:


Conflicts and Precedence
########################

Symmetric properties need not be unique. Resolution by value is deterministic
based on the following priority order:

1) Type Specificity
    Any value that matches a property value without a type coercion will take
    precedence over values that match after type coercion.
2) Left to right.
    Any value with a smaller tuple index will override any value with a larger
    tuple index
3) Nested left to right.
    Any value in a list or set of symmetric values will override values with
    larger indexes in corresponding property values.

.. code-block:: python

    class PriorityEx(EnumProperties, s('prop1'), s('prop2', case_fold=True)):

        # <-------- Higher Precedence
        # name   value  prop1   prop2      #  ^
        ONE     = 0,     '1',    (3, 4)    #  |
        TWO     = 1,     '2',    (3, '4')  #  Higher
        THREE   = 2,     '3',    (3, 4)    #  Precedence

    PriorityEx(0) == PriorityEx.ONE     # order left to right
    PriorityEx('1') == PriorityEx.ONE   # type specificity
    PriorityEx(3) == PriorityEx.ONE     # type specificity/order
    PriorityEx('3') == PriorityEx.THREE # type specificity
    PriorityEx(4) == PriorityEx.ONE     # order left to right
    PriorityEx('4') == PriorityEx.TWO   # type specificity

Symmetric Builtins
##################

When extending from Enum or other Enum base classes, some builtin properties
are available. `name` is available on all standard Enum classes. By default
`EnumProperties` will make `name` case sensitive symmetric. To override this
behavior, specify a `_symmetric_builtins_` list as a class member. The items
may be strings or `s()` values. For example to make name case insensitive we
could do:


.. code-block:: python

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        _symmetric_builtins_ = [s('name', case_fold=True)]

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # now we can do this:
    Color('red') == Color.RED
