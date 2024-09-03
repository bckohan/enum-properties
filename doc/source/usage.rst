.. include:: refs.rst

.. _usage:

=====
Usage
=====

To add properties to an enumeration you must inherit from
:py:class:`~enum_properties.EnumProperties` or :py:class:`~enum_properties.IntEnumProperties`
instead of Enum_ and IntEnum_, list property values in a tuple with each enumeration value and let
:py:class:`~enum_properties.EnumProperties` know that your properties exist and what their names
are by adding type hints to the Enum class definition before the enumeration values. The
type hints must be in the same order as property values are listed in the value tuples:

.. note::

    A ValueError_ will be thrown if the length of any value tuple does not
    match the number of expected properties. If a given enumeration value does
    not have a property, None should be used.

For example:

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

    # The property values are accessible by name on the enumeration values:
    Color.RED.hex == 'ff0000'

.. note::

    The property type hints must be specified before the enumeration values to become properties.
    If you would like a type hint on your enumeration that are not properties, you may specify the
    hint after the value definitions.

:py:class:`~enum_properties.EnumProperties` inherits from enum and all other standard python
enumeration functionality will work. The :py:class:`~enum_properties.EnumProperties` base class is
equivalent to:

.. code:: python

    from enum_properties import EnumPropertiesMeta, p
    from enum import Enum, auto

    class Color(Enum, metaclass=EnumPropertiesMeta):
        ...


Symmetry
--------

For some enumerations it will make sense to be able to instantiate an enumeration value instance
from one of the property values. This is called property symmetry. To mark a property as symmetric,
annotate your type hint with :py:meth:`~enum_properties.Symmetric`:

.. code:: python

    from enum_properties import EnumProperties, Symmetric
    from enum import auto

    class Color(EnumProperties):

        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), '0xff0000'
        GREEN  = auto(), (0, 1, 0), '0x00ff00'
        BLUE   = auto(), (0, 0, 1), '0x0000ff'

    Color.RED == Color((1, 0, 0)) == Color('0xFF0000') == Color('0xff0000')

Symmetric string properties are by default case sensitive. To mark a property as case insensitive,
use the ``case_fold=True`` parameter on the :py:meth:`~enum_properties.Symmetric` dataclass. By
default, none values for symmetric properties will not be symmetric. To change this behavior pass:
``match_none=True`` to :py:meth:`~enum_properties.Symmetric`.

Symmetric property support is added through the :py:class:`~enum_properties.SymmetricMixin` class
which is included in the :py:class:`~enum_properties.EnumProperties` base class. The above is
equivalent to this:

.. code:: python

    from enum_properties import EnumPropertiesMeta, SymmetricMixin
    from enum import Enum, auto

    class Color(SymmetricMixin, Enum, metaclass=EnumPropertiesMeta):
        ...

.. warning::

    Any object may be a property value, but symmetric property values must be hashable. A
    ValueError_ will be thrown if they are not.

An exception to this is that symmetric property values may be a list or set of hashable values.
Each value in the list will be symmetric to the enumeration value. Tuples are hashable and are
treated as singular property values. See the ``AddressRoute`` example in :ref:`examples`.

:py:class:`~enum_properties.SymmetricMixin` tries very hard to resolve enumeration values from
objects. Type coercion to all potential value types will be attempted before giving up. For
instance, if we have a hex object that is coercible to a string hex value we could instantiate our
Color enumeration from it and perform equality comparisons:

.. code:: python

    # str(hex(16711680)) == '0xff0000'
    Color.RED == Color(hex(16711680)) == hex(16711680)
    Color.RED == (1, 0, 0)
    Color.RED != (0, 1, 0)
    Color.RED == '0xFF0000'


.. warning::

    Using symmetric properties with @verify(UNIQUE) will raise an error:

    .. code:: python

        from enum_properties import EnumProperties, Symmetric
        from enum import verify, UNIQUE

        @verify(UNIQUE)
        class Color(EnumProperties):

            label: t.Annotated[str, Symmetric()]

            RED = 1, 'red'
            GREEN = 2, 'green'
            BLUE = 3, 'blue'

        # ValueError: aliases found in <enum 'Color'>: blue -> BLUE,
        # green -> GREEN, red -> RED

Conflicts and Precedence
########################

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

.. code-block:: python

    class PriorityEx(IntEnumProperties):

        prop1: t.Annotated[str, Symmetric()]
        prop2: t.Annotated[t.List[int | str], Symmetric(case_fold=True)]

        # <-------- Higher Precedence
        # name  value   prop1     prop2    #  ^
        ONE     = 0,     '1',    [3, 4]    #  |
        TWO     = 1,     '2',    [3, '4']  #  Higher
        THREE   = 2,     '3',    [3, 4]    #  Precedence

    PriorityEx(0)   == PriorityEx.ONE   # order left to right
    PriorityEx('1') == PriorityEx.ONE   # type specificity
    PriorityEx(3)   == PriorityEx.ONE   # type specificity/order
    PriorityEx('3') == PriorityEx.THREE # type specificity
    PriorityEx(4)   == PriorityEx.ONE   # order left to right
    PriorityEx('4') == PriorityEx.TWO   # type specificity

Symmetric Builtins
##################

When extending from Enum_ or other enumeration base classes, some builtin properties are available.
`name` is available on all standard Enum_ classes. By default
:py:class:`~enum_properties.EnumProperties` will make `name` case sensitive symmetric. To override
this behavior, specify a ``_symmetric_builtins_`` list as a class member. The items may be strings
or :py:meth:`~enum_properties.s` values. For example to make name case insensitive we might:

.. code-block:: python

    class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

        _symmetric_builtins_ = [s('name', case_fold=True)]

        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'

    # now we can do this:
    Color('red') == Color.RED

You may also instead directly annotate the name property with :py:meth:`~enum_properties.Symmetric`
but the _symmetric_builtins_ attribute will also work for normal @property members. See the
``AddressRoute`` and ``MapBox`` examples in :ref:`examples`.

Specializing Member Functions
-----------------------------

Provide specialized implementations of member functions using the specialize decorator. For
example:

.. code-block:: python

        class SpecializedEnum(EnumProperties):

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

        assert SpecializedEnum.ONE.method() == 'method_one()'
        assert SpecializedEnum.TWO.method() == 'method_two()'
        assert SpecializedEnum.THREE.method() == 'method_three()'

The :py:meth:`~enum_properties.specialize` decorator works on @classmethods and @staticmethods as
well, but it must be the outermost decorator.

The undecorated method will apply to all members that lack a specialization:

.. code-block:: python

    class SpecializedEnum(EnumProperties):

        ONE   = 1
        TWO   = 2
        THREE = 3

        def method(self):
            return 'generic()'

        @specialize(THREE)
        def method(self):
            return 'method_three()'

    assert SpecializedEnum.ONE.method() == 'generic()'
    assert SpecializedEnum.TWO.method() == 'generic()'
    assert SpecializedEnum.THREE.method() == 'method_three()'


If no undecorated method or specialization for a value is found that value will
lack the method.

.. code-block:: python

    class SpecializedEnum(EnumProperties):

        ONE   = 1
        TWO   = 2
        THREE = 3

        @specialize(THREE)
        def method(self):
            return 'method_three()'

    assert not hasattr(SpecializedEnum.ONE, 'method')
    assert not hasattr(SpecializedEnum.TWO, 'method')
    assert SpecializedEnum.THREE.method() == 'method_three()'


:py:meth:`~enum_properties.specialize` will also accept a list so that multiple enumeration values
can share the same specialization.

.. code-block:: python

    class SpecializedEnum(EnumProperties):

        ONE   = 1
        TWO   = 2
        THREE = 3

        @specialize(TWO, THREE)
        def method(self):
            return 'shared()'

    assert not hasattr(SpecializedEnum.ONE, 'method')
    assert SpecializedEnum.TWO.method() == 'shared()'
    assert SpecializedEnum.THREE.method() == 'shared()'


Flags
-----

IntFlag_ and Flag_ types that support properties are also provided by the
:py:class:`~enum_properties.IntFlagProperties` and :py:class:`~enum_properties.FlagProperties`
classes. For example:

.. code-block:: python

        import typing as t
        from enum_properties import IntFlagProperties, Symmetric

        class Perm(IntFlagProperties):

            label: t.Annotated[str, Symmetric(case_fold=True)]

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

Flag enumerations can also be created from iterables and generators containing values or symmetric
values.

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

    Iterable instantiation on flags is added using the :py:class:`~enum_properties.DecomposeMixin`.
    To create a flag enumeration without the iterable extensions we can simply declare it manually
    without the mixin:

    .. code-block:: python

        class MyFlag(
            SymmetricMixin,
            enum.IntFlag,
            metaclass=EnumPropertiesMeta
        ):
            ...

As of Python 3.11 `boundary values <https://docs.python.org/3/library/enum.html#enum.FlagBoundary>`_
are supported on flags. Boundary specifiers must be supplied as named arguments:

.. code-block:: python

    from enum_properties import IntFlagProperties, Symmetric
    from enum import STRICT

        class Perm(IntFlagProperties, boundary=STRICT):

            label: t.Annotated[str, Symmetric(case_fold=True)]

            R = 1, 'read'
            W = 2, 'write'
            X = 4, 'execute'
            RWX = 7, 'all'

    Perm(8)  # raises ValueError


Nested Classes
--------------

.. note::

    In python <3.13, nested classes behave normally on enums that inherit from
    :py:class:`~enum_properties.EnumProperties` and that specify at least one
    property. In python 3.13 this behavior will remain unchanged in
    enum-properties and normal Enum_ classes will adopt it.

On enums that inherit from Enum_ in python < 3.13 nested classes become
enumeration values because types may be values and a quirk of Python makes it
difficult to determine if a type on a class is declared as a nested class
during __new__. For enums with properties we can distinguish declared classes
because values must be tuples.

Using :py:class:`~enum_properties.EnumProperties` this is possible:

.. code-block:: python

        class MyEnum(EnumProperties):

            label: str

            class Type1:
                pass

            class Type2:
                pass

            class Type3:
                pass

            VALUE1 = Type1, 'label1'
            VALUE2 = Type2, 'label2'
            VALUE3 = Type3, 'label3'

        # only the expected values become enumeration values
        assert MyEnum.Type1 == MyEnum.VALUE1.value
        assert MyEnum.Type2 == MyEnum.VALUE2.value
        assert MyEnum.Type3 == MyEnum.VALUE3.value
        assert len(MyEnum) == 3

        # nested classes behave as expected
        assert MyEnum.Type1().__class__ is MyEnum.Type1
        assert MyEnum.Type2().__class__ is MyEnum.Type2
        assert MyEnum.Type3().__class__ is MyEnum.Type3


Dataclasses
-----------

As of Python 3.12, `Enum values can be <https://docs.python.org/3.12/howto/enum.html#enum-dataclass-support>`_
Dataclasses_. At first glance this enables some behavior that is similar to adding properties. For
example:

.. code-block:: python

    @dataclass
    class CreatureDataMixin:
        size: str
        legs: int
        tail: bool = field(repr=False, default=True)

    class Creature(CreatureDataMixin, Enum):
        BEETLE = 'small', 6
        DOG = 'medium', 4

    # you can now access the dataclass fields on the enumeration values
    # as with enum properties:
    assert Creature.BEETLE.size == 'small'
    assert Creature.BEETLE.legs == 6
    assert Creature.BEETLE.tail is True

**We still recommend EnumProperties as the preferred way to add
additional attributes to a Python enumeration for the following
reasons:**

- The value of BEETLE and DOG in the above example are instances
  of the CreatureDataMixin dataclass. This can complicate interfacing
  with other systems (like databases) where it is more natural for the
  enumeration value to be a small primitive type like a character or
  integer.

- The dataclass method requires two classes where a single EnumProperties
  class will suffice.

- Dataclasses_ are not hashable by default which can complicate equality
  testing and marshalling external data into enumeration values.

- Many code bases that use duck typing and that work with Enums expect the ``value``
  attribute to be a a plain old data type and therefore serializable.

.. note::

    EnumProperties also integrates with Enum's dataclass support!
    For example we can add a symmetric property to the Creature
    enumeration like so:

.. code-block:: python

    @dataclass
    class CreatureDataMixin:
        size: str
        legs: int
        tail: bool = field(repr=False, default=True)

    class Creature(CreatureDataMixin, EnumProperties):

        kingdom: t.Annotated[str, Symmetric()]

        BEETLE = 'small', 6, False, 'insect'
        DOG = 'medium', 4, 'animal'

    # you can now access the dataclass fields on the enumeration values
    # as with enum properties:
    assert Creature.BEETLE.size == 'small'
    assert Creature.BEETLE.legs == 6
    assert Creature.BEETLE.tail is False
    assert Creature.BEETLE.kingdom == 'insect'

    # adding symmetric properties onto a dataclass enum can help with
    # marshalling external data into the enum classes!
    assert Creature('insect') is Creature.BEETLE


Hash Equivalency
----------------

The Enum_ types that inherit from primitive types IntEnum_ and StrEnum_ are hash equivalent
to their primitive types. This means that they can be used interchangeably in collections that
use hashing:

.. code-block:: python

    class MyIntEnum(IntEnum):

        ONE = 1
        TWO = 2
        THREE = 3

    assert {1: 'Found me!'}[IntEnum.ONE] == 'Found me!'

:py:class:`~enum_properties.IntEnumProperties`, :py:class:`~enum_properties.StrEnumProperties` and
:py:class:`~enum_properties.IntFlagProperties` also honor this hash equivalency. When defining your
own symmetric enumeration types if you want to keep hash equivalency to the value type you will
you will have to implement this yourself. For example, if you wanted your color enumeration to also
be an rgb tuple:


.. code-block:: python

    from enum_properties import EnumPropertiesMeta, SymmetricMixin, s
    from enum import Enum

    class Color(
        SymmetricMixin,
        tuple,
        Enum,
        metaclass=EnumPropertiesMeta
    ):
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # name   value (rgb)    hex
        RED    = (1, 0, 0), '0xff0000'
        GREEN  = (0, 1, 0), '0x00ff00'
        BLUE   = (0, 0, 1), '0x0000ff'

        def __hash__(self):  # you must add this!
            return tuple.__hash__(self)

    assert {(1, 0, 0): 'Found me!'}[Color.RED] == 'Found me!'


Type Hinting Alternative
------------------------

The legacy (1.x) way of specifying properties using :py:meth:`~enum_properties.p` and
:py:meth:`~enum_properties.s` value inheritance is still supported. If any properties
are defined this way it will take precedence over type hinting and the type hints will
not be interpreted as properties. For example:

.. code-block:: python

    from enum_properties import EnumProperties, p
    from enum import auto

    class Color(EnumProperties, p('rgb'), p('hex')):

        extra: int  # this does not become a property

        # name   value      rgb       hex
        RED    = auto(), (1, 0, 0), 'ff0000'
        GREEN  = auto(), (0, 1, 0), '00ff00'
        BLUE   = auto(), (0, 0, 1), '0000ff'
