.. include:: refs.rst

.. _usage:

=====
Usage
=====

To add properties to an enumeration you must inherit from
:py:class:`~enum_properties.EnumProperties` or
:py:class:`~enum_properties.IntEnumProperties` instead of Enum_ and IntEnum_,
list property values in a tuple with each enumeration value and let
:py:class:`~enum_properties.EnumProperties` know that your properties
exist and what their names are by adding :py:meth:`~enum_properties.p`
values to the base class list. The :py:meth:`~enum_properties.p` values
must be in the same order as property values are listed in the value tuples:

.. note::

    A ValueError_ will be thrown if the length of any value tuple does not
    match the number of expected properties. If a given enumeration value does
    not have a property, None should be used.

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

:py:class:`~enum_properties.EnumProperties` inherits from enum and all
other standard python enumeration functionality will work.
The :py:class:`~enum_properties.EnumProperties` base class is equivalent
to:

.. code:: python

    from enum_properties import EnumPropertiesMeta, p
    from enum import Enum, auto

    class Color(Enum, p('rgb'), p('hex'), metaclass=EnumPropertiesMeta):
        ...


Symmetry
--------

For some enumerations it will make sense to be able to instantiate an
enumeration value instance from one of the property values. This is called
property symmetry. To mark a property as symmetric, use
:py:meth:`~enum_properties.s` values instead of
:py:meth:`~enum_properties.p` values:

.. code:: python

    from enum_properties import EnumProperties, s
    from enum import auto

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), '0xff0000'
        GREEN  = auto(), (0, 1, 0), '0x00ff00'
        BLUE   = auto(), (0, 0, 1), '0x0000ff'

    Color.RED == Color((1, 0, 0)) == Color('0xFF0000') == Color('0xff0000')

Symmetric string properties are by default case sensitive. To mark a property
as case insensitive, use the `case_fold=True` parameter on the
:py:meth:`~enum_properties.s` value.

Symmetric property support is added through the
:py:class:`~enum_properties.SymmetricMixin` class which is included in the
:py:class:`~enum_properties.EnumProperties` base class. The above is
equivalent to this:

.. code:: python

    from enum_properties import EnumPropertiesMeta, SymmetricMixin, s
    from enum import Enum, auto

    class Color(
        SymmetricMixin,
        Enum,
        s('rgb'),
        s('hex', case_fold=True),
        metaclass=EnumPropertiesMeta
    ):
        ...

.. warning::

    Any object may be a property value, but symmetric property values must be
    hashable. A ValueError_ will be thrown if they are not.

An exception to this is that symmetric property values may be a list or set of
hashable values. Each value in the list will be symmetric to the enumeration
value. Tuples are hashable and are treated as singular property values. See the
``AddressRoute`` example in :ref:`examples`.

:py:class:`~enum_properties.SymmetricMixin` tries very hard to resolve
enumeration values from objects. Type coercion to all potential value types
will be attempted before giving up. For instance, if we have a hex object that
is coercible to a string hex value we could instantiate our Color
enumeration from it and perform equality comparisons:

.. code:: python

    # str(hex(16711680)) == '0xff0000'
    Color.RED == Color(hex(16711680)) == hex(16711680)
    Color.RED == (1, 0, 0)
    Color.RED != (0, 1, 0)
    Color.RED == '0xFF0000'


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

    class PriorityEx(
        IntEnumProperties,
        s('prop1'),
        s('prop2', case_fold=True)
    ):

        # <-------- Higher Precedence
        # name  value   prop1     prop2    #  ^
        ONE     = 0,     '1',    (3, 4)    #  |
        TWO     = 1,     '2',    (3, '4')  #  Higher
        THREE   = 2,     '3',    (3, 4)    #  Precedence

    PriorityEx(0)   == PriorityEx.ONE   # order left to right
    PriorityEx('1') == PriorityEx.ONE   # type specificity
    PriorityEx(3)   == PriorityEx.ONE   # type specificity/order
    PriorityEx('3') == PriorityEx.THREE # type specificity
    PriorityEx(4)   == PriorityEx.ONE   # order left to right
    PriorityEx('4') == PriorityEx.TWO   # type specificity

Symmetric Builtins
##################

When extending from Enum_ or other enumeration base classes, some builtin
properties are available. `name` is available on all standard Enum_ classes. By
default :py:class:`~enum_properties.EnumProperties` will make `name` case
sensitive symmetric. To override this behavior, specify a
``_symmetric_builtins_`` list as a class member. The items may be strings or
:py:meth:`~enum_properties.s` values. For example to make name case
insensitive we might:

.. code-block:: python

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        _symmetric_builtins_ = [s('name', case_fold=True)]

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # now we can do this:
    Color('red') == Color.RED


Flags
-----

IntFlag_ and Flag_ types that support properties are also provided by the
:py:class:`~enum_properties.IntFlagProperties` and
:py:class:`~enum_properties.FlagProperties` classes. For example:

.. code-block:: python

        class Perm(
            IntFlagProperties,
            s('label', case_fold=True),
        ):

            R = 1, 'read'
            W = 2, 'write'
            X = 4, 'execute'
            RWX = 7, 'all'

        # combined flags can be specified and given properties
        assert (Perm.R | Perm.W | Perm.X).label == 'all'

        # properties for combined flags, that are not listed will be None
        assert (Perm.R | Perm.W).label is None

        # list the active flags:
        assert (Perm.R | Perm.W | Perm.X).flagged == [Perm.R, Perm.W, Perm.X]

Flag enumerations can also be created from iterables and generators containing
values or symmetric values.

.. code-block:: python

    assert Perm([Perm.R, Perm.W, Perm.X]) == Perm.RWX
    assert Perm({'read', 'write', 'execute'}) == Perm.RWX
    assert Perm((perm for perm in (1, 'write', Perm.X)) == Perm.RWX

    # iterate through active flags
    assert [perm for perm in Perm.RWX] == [Perm.R, Perm.W, Perm.X]

    # flagged property returns list of flags
    assert (Perm.R | Perm.W).flagged == [Perm.R, Perm.W]

    # instantiate a Flag off an empty iterable
    assert Perm(0) == Perm([])

    # check number of active flags:
    assert len(Perm(0)) == 0
    assert len(Perm.RWX) == 3
    assert len(Perm.R | Perm.X) == 2
    assert len(Perm.R & Perm.X) == 0


.. note::

    Iterable behavior on flags is added using the
    :py:class:`~enum_properties.DecomposeMixin`. To create a flag enumeration
    without the iterable extensions we can simply declare it manually without
    the mixin:

    .. code-block:: python

        class MyFlag(
            SymmetricMixin,
            enum.IntFlag,
            metaclass=EnumPropertiesMeta
        ):
            ...
