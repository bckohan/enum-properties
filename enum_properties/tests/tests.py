import enum
import pickle
import sys
from collections.abc import Hashable
from enum import Enum, auto
from io import BytesIO
from unittest import TestCase

from enum_properties import (
    EnumProperties,
    FlagProperties,
    IntEnumProperties,
    IntFlagProperties,
    SymmetricMixin,
    p,
    s,
    specialize,
)


def transparent(func):
    return func  # pragma: no cover


nonmember, member = (enum.nonmember, enum.member)\
    if sys.version_info >= (3, 11) else (transparent, transparent)


class Unhashable:
    pass


class TestEnums(TestCase):

    def test_p(self):
        from enum_properties import _Prop

        prop1 = p('prop1')
        prop2 = s('prop2')
        prop3 = s('prop3', case_fold=True)
        prop4 = p('prop4')

        self.assertTrue(issubclass(prop1, _Prop))
        self.assertTrue(issubclass(prop2, _Prop))
        self.assertTrue(issubclass(prop3, _Prop))
        self.assertTrue(issubclass(prop4, _Prop))
        self.assertEqual(prop1.name(), 'prop1')
        self.assertEqual(prop2.name(), 'prop2')
        self.assertEqual(prop3.name(), 'prop3')
        self.assertEqual(prop4.name(), 'prop4')
        self.assertEqual(prop1(), 'prop1')
        self.assertEqual(prop2(), 'prop2')
        self.assertEqual(prop3(), 'prop3')
        self.assertEqual(prop4(), 'prop4')

        self.assertFalse(prop1.symmetric)
        self.assertTrue(prop2.symmetric)
        self.assertTrue(prop3.symmetric)
        self.assertFalse(prop4.symmetric)

        self.assertFalse(prop1().symmetric)
        self.assertTrue(prop2().symmetric)
        self.assertTrue(prop3().symmetric)
        self.assertFalse(prop4().symmetric)

        self.assertFalse(hasattr(prop1, 'case_fold'))
        self.assertFalse(prop2.case_fold)
        self.assertTrue(prop3.case_fold)
        self.assertFalse(hasattr(prop4, 'case_fold'))

        self.assertFalse(hasattr(prop1(), 'case_fold'))
        self.assertFalse(prop2().case_fold)
        self.assertTrue(prop3().case_fold)
        self.assertFalse(hasattr(prop4(), 'case_fold'))

    def test_unhashable_symmetry(self):
        """
        Tests that a value error is thrown when an unhashable type is used as
        a symmetric property
        """
        with self.assertRaises(ValueError):
            class BadEnum(EnumProperties, s('bad_prop')):
                VAL1 = 'E1', 'E1 Label', 'Good prop'
                VAL2 = 'E2', 'E2 Label', {'hashable': False}

    def test_unicode_casefold(self):

        class CaseAgnostic(EnumProperties, s('label', case_fold=True)):
            ONE = 1, 'ß'
            TWO = 2, 'Σίσυφος'

        self.assertEqual(CaseAgnostic.ONE, CaseAgnostic('ss'))
        self.assertEqual(CaseAgnostic.TWO, CaseAgnostic('ΣΊΣΥΦΟΣ'))

        # test that closest case matches first
        class CaseFirstMatch(EnumProperties, s('label', case_fold=True)):
            ONE = 1, 'ß'
            TWO = 2, 'Σίσυφος'
            THREE = 3, 'ss'

        self.assertEqual(CaseFirstMatch.THREE, CaseFirstMatch('ss'))
        self.assertEqual(CaseFirstMatch.ONE, CaseFirstMatch('ß'))
        self.assertEqual(CaseFirstMatch.TWO, CaseFirstMatch('ΣΊΣΥΦΟΣ'))

    def test_properties_and_symmetry(self):

        class Color(
            IntEnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):
            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'

        self.assertEqual(Color.RED, Color((1, 0, 0)))
        self.assertEqual(Color.RED, Color('ff0000'))
        self.assertEqual(Color.RED, Color('FF0000'))
        self.assertEqual(Color.RED, Color('RED'))
        self.assertEqual(Color.RED, Color['RED'])
        self.assertEqual(Color.RED, Color(1))
        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, 'Roja')
        self.assertEqual(Color.RED.hex, 'ff0000')
        self.assertRaises(ValueError, Color, 'Roja')
        self.assertRaises(ValueError, Color, 'Red')

        # test symmetric equality
        self.assertEqual(Color.RED, (1, 0, 0))
        self.assertEqual(Color.RED, 'ff0000')
        self.assertEqual(Color.RED, 'FF0000')
        self.assertEqual(Color.RED, 'RED')
        self.assertEqual(Color.RED, 1)

        self.assertTrue(Color.RED != (1, 1, 0))
        self.assertTrue(Color.RED != '00ff00')
        self.assertTrue(Color.RED != 'EE0000')
        self.assertTrue(Color.RED != 'GRAY')
        self.assertTrue(Color.RED != 3)

        self.assertFalse(Color.RED != (1, 0, 0))
        self.assertFalse(Color.RED != 'ff0000')
        self.assertFalse(Color.RED != 'FF0000')
        self.assertFalse(Color.RED != 'RED')
        self.assertFalse(Color.RED != 1)

        self.assertNotEqual(Color.RED, (1, 1, 0))
        self.assertNotEqual(Color.RED, 'EE0000')
        self.assertNotEqual(Color.RED, '00ff00')
        self.assertNotEqual(Color.RED, 'GREEN')
        self.assertNotEqual(Color.RED, 5)
        ############################

        self.assertEqual(Color.GREEN, Color((0, 1, 0)))
        self.assertEqual(Color.GREEN, Color('00ff00'))
        self.assertEqual(Color.GREEN, Color('00FF00'))
        self.assertEqual(Color.GREEN, Color('GREEN'))
        self.assertEqual(Color.GREEN, Color['GREEN'])
        self.assertEqual(Color.GREEN, Color(2))
        self.assertEqual(Color.GREEN.value, 2)
        self.assertEqual(Color.GREEN.spanish, 'Verde')
        self.assertEqual(Color.GREEN.hex, '00ff00')
        self.assertRaises(ValueError, Color, 'Verde')
        self.assertRaises(ValueError, Color, 'Green')

        # test symmetric equality
        self.assertEqual(Color.GREEN, (0, 1, 0))
        self.assertEqual(Color.GREEN, '00ff00')
        self.assertEqual(Color.GREEN, '00FF00')
        self.assertEqual(Color.GREEN, 'GREEN')
        self.assertEqual(Color.GREEN, 2)
        self.assertNotEqual(Color.GREEN, 'EE0000')

        self.assertEqual(Color.BLUE, Color((0, 0, 1)))
        self.assertEqual(Color.BLUE, Color('0000ff'))
        self.assertEqual(Color.BLUE, Color('0000FF'))
        self.assertEqual(Color.BLUE, Color('BLUE'))
        self.assertEqual(Color.BLUE, Color['BLUE'])
        self.assertEqual(Color.BLUE, Color(3))
        self.assertEqual(Color.BLUE.value, 3)
        self.assertEqual(Color.BLUE.spanish, 'Azul')
        self.assertEqual(Color.BLUE.hex, '0000ff')
        self.assertRaises(ValueError, Color, 'Azul')
        self.assertRaises(ValueError, Color, 'Blue')

        # test symmetric equality
        self.assertEqual(Color.BLUE, (0, 0, 1))
        self.assertEqual(Color.BLUE, '0000ff')
        self.assertEqual(Color.BLUE, '0000FF')
        self.assertEqual(Color.BLUE, 'BLUE')
        self.assertEqual(Color.BLUE, 3)
        self.assertNotEqual(Color.BLUE, (0, 1, 1))

    def test_property_lists(self):

        class Color(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):
            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'

        self.assertEqual(
            [prop for prop in Color._properties_ if prop.symmetric],
            ['rgb', 'hex']
        )

        self.assertEqual(
            Color._properties_,
            ['spanish', 'rgb', 'hex']
        )

    def test_symmetric_builtin_override(self):
        class Color(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):
            _symmetric_builtins_ = [s('name', case_fold=True)]

            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'

        self.assertEqual(Color.RED, Color('red'))
        self.assertEqual(Color.GREEN, Color('gREen'))
        self.assertEqual(Color.BLUE, Color('Blue'))

    def test_symmetric_builtin_override_wrongtype(self):
        with self.assertRaises(ValueError):
            class Color(
                EnumProperties,
                p('spanish'),
                s('rgb'),
                s('hex', case_fold=True)
            ):
                _symmetric_builtins_ = [p('name')]

                RED = 1, 'Roja', (1, 0, 0), 'ff0000'
                GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
                BLUE = 3, 'Azul', (0, 0, 1), '0000ff'

    def test_symmetric_builtin_override_missing(self):
        with self.assertRaises(ValueError):
            class Color(
                EnumProperties,
                p('spanish'),
                s('rgb'),
                s('hex', case_fold=True)
            ):
                _symmetric_builtins_ = [s('does_not_exist')]

                RED = 1, 'Roja', (1, 0, 0), 'ff0000'
                GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
                BLUE = 3, 'Azul', (0, 0, 1), '0000ff'

    def test_symmetric_match_none_parameter(self):

        # test default behavior
        class ColorDefault(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex')
        ):

            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), None
            BLUE = 3, 'Azul', (0, 0, 1), None

        self.assertEqual(ColorDefault.RED, 'ff0000')
        self.assertNotEqual(ColorDefault.GREEN, None)
        self.assertNotEqual(ColorDefault.BLUE, None)
        self.assertRaises(ValueError, ColorDefault, None)
        self.assertRaises(ValueError, ColorDefault, 'FF0000')
        self.assertEqual(ColorDefault('ff0000'), ColorDefault.RED)
        self.assertEqual(ColorDefault((1, 0, 0)), ColorDefault.RED)
        self.assertEqual(ColorDefault((0, 1, 0)), ColorDefault.GREEN)
        self.assertEqual(ColorDefault((0, 0, 1)), ColorDefault.BLUE)

        class ColorNoMatchNone(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True, match_none=False)
        ):

            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), None
            BLUE = 3, 'Azul', (0, 0, 1), None

        self.assertEqual(ColorNoMatchNone.RED, 'fF0000')
        self.assertNotEqual(ColorNoMatchNone.GREEN, None)
        self.assertNotEqual(ColorNoMatchNone.BLUE, None)
        self.assertRaises(ValueError, ColorNoMatchNone, None)
        self.assertEqual(ColorNoMatchNone('Ff0000'), ColorNoMatchNone.RED)
        self.assertEqual(ColorNoMatchNone((1, 0, 0)), ColorNoMatchNone.RED)
        self.assertEqual(ColorNoMatchNone((0, 1, 0)), ColorNoMatchNone.GREEN)
        self.assertEqual(ColorNoMatchNone((0, 0, 1)), ColorNoMatchNone.BLUE)

        class ColorMatchNone(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', match_none=True)
        ):

            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), None
            BLUE = 3, 'Azul', (0, 0, 1), None

        self.assertNotEqual(ColorMatchNone.RED, 'FF0000')
        self.assertEqual(ColorMatchNone.RED, 'ff0000')
        self.assertEqual(ColorMatchNone.GREEN, None)
        self.assertNotEqual(ColorMatchNone.BLUE, None)
        self.assertEqual(ColorMatchNone(None), ColorMatchNone.GREEN)
        self.assertEqual(ColorMatchNone('ff0000'), ColorMatchNone.RED)
        self.assertRaises(ValueError, ColorMatchNone, 'FF0000')
        self.assertEqual(ColorMatchNone((1, 0, 0)), ColorMatchNone.RED)
        self.assertEqual(ColorMatchNone((0, 1, 0)), ColorMatchNone.GREEN)
        self.assertEqual(ColorMatchNone((0, 0, 1)), ColorMatchNone.BLUE)

    def test_properties_no_symmetry(self):
        """
        Tests that absence of SymmetricMixin works but w/o symmetric
        properties
        """

        class DisableSymmetryMixin(SymmetricMixin):

            @classmethod
            def _missing_(cls, value):
                return Enum._missing_(value)

        class Color(
            DisableSymmetryMixin,
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):
            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'

        self.assertRaises(ValueError, Color, (1, 0, 0))
        self.assertRaises(ValueError, Color, 'ff0000')
        self.assertRaises(ValueError, Color, 'FF0000')
        self.assertRaises(ValueError, Color, 'RED')
        self.assertEqual(Color.RED, Color['RED'])
        self.assertEqual(Color.RED, Color(1))
        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, 'Roja')
        self.assertEqual(Color.RED.hex, 'ff0000')
        self.assertRaises(ValueError, Color, 'Roja')
        self.assertRaises(ValueError, Color, 'Red')

        self.assertRaises(ValueError, Color, (0, 1, 0))
        self.assertRaises(ValueError, Color, '00ff00')
        self.assertRaises(ValueError, Color, '00FF00')
        self.assertRaises(ValueError, Color, 'GREEN')
        self.assertEqual(Color.GREEN, Color['GREEN'])
        self.assertEqual(Color.GREEN, Color(2))
        self.assertEqual(Color.GREEN.value, 2)
        self.assertEqual(Color.GREEN.spanish, 'Verde')
        self.assertEqual(Color.GREEN.hex, '00ff00')
        self.assertRaises(ValueError, Color, 'Verde')
        self.assertRaises(ValueError, Color, 'Green')

        self.assertRaises(ValueError, Color, (0, 0, 1))
        self.assertRaises(ValueError, Color, '0000ff')
        self.assertRaises(ValueError, Color, '0000FF')
        self.assertRaises(ValueError, Color, 'BLUE')
        self.assertEqual(Color.BLUE, Color['BLUE'])
        self.assertEqual(Color.BLUE, Color(3))
        self.assertEqual(Color.BLUE.value, 3)
        self.assertEqual(Color.BLUE.spanish, 'Azul')
        self.assertEqual(Color.BLUE.hex, '0000ff')
        self.assertRaises(ValueError, Color, 'Azul')
        self.assertRaises(ValueError, Color, 'Blue')

    def test_symmetry_priorities(self):

        class Priority(
            EnumProperties,
            s('prop1'),
            s('prop2')
        ):
            FIRST = 1, '3', 3
            SECOND = 2, '2', 2
            THIRD = 3, '1', 1

        self.assertEqual(Priority.FIRST, Priority(1))
        self.assertEqual(Priority.FIRST, Priority('3'))
        self.assertEqual(Priority.SECOND, Priority(2))
        self.assertEqual(Priority.SECOND, Priority('2'))
        self.assertEqual(Priority.THIRD, Priority(3))
        self.assertEqual(Priority.THIRD, Priority('1'))

    def test_symmetry_tuples(self):

        class Priority(
            EnumProperties,
            s('prop1'),
            s('prop2')
        ):
            FIRST = 1, '3', [2.1, '2.3']
            SECOND = 2, '2', [2.2, '2.2']
            THIRD = 3, '1', [2.3, '2.1']

        self.assertEqual(Priority.FIRST, Priority(1))
        self.assertEqual(Priority.FIRST, Priority('3'))
        self.assertEqual(Priority.SECOND, Priority(2))
        self.assertEqual(Priority.SECOND, Priority('2'))
        self.assertEqual(Priority.THIRD, Priority(3))
        self.assertEqual(Priority.THIRD, Priority('1'))

        self.assertEqual(Priority.FIRST, Priority(2.1))
        self.assertEqual(Priority.FIRST, Priority('2.3'))
        self.assertEqual(Priority.SECOND, Priority(2.2))
        self.assertEqual(Priority.SECOND, Priority('2.2'))
        self.assertEqual(Priority.THIRD, Priority(2.3))
        self.assertEqual(Priority.THIRD, Priority('2.1'))

    def test_auto(self):

        class ColorAuto(EnumProperties):
            def _generate_next_value_(name, start, count, last_values):
                return name.title()

            RED = auto()
            GREEN = auto()
            BLUE = auto()

        self.assertEqual(ColorAuto.RED, ColorAuto('Red'))
        self.assertEqual(ColorAuto.GREEN, ColorAuto('Green'))
        self.assertEqual(ColorAuto.BLUE, ColorAuto('Blue'))
        self.assertEqual(ColorAuto.RED, ColorAuto['RED'])
        self.assertEqual(ColorAuto.GREEN, ColorAuto['GREEN'])
        self.assertEqual(ColorAuto.BLUE, ColorAuto['BLUE'])

        class ColorAutoSym(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):
            def _generate_next_value_(name, start, count, last_values):
                return name.title()

            RED = auto(), 'Roja', (1, 0, 0), 'ff0000'
            GREEN = auto(), 'Verde', (0, 1, 0), '00ff00'
            BLUE = auto(), 'Azul', (0, 0, 1), '0000ff'

        self.assertEqual(ColorAutoSym.RED, ColorAutoSym['RED'])
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym['GREEN'])
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym['BLUE'])
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym('Red'))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym('Green'))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym('Blue'))

        self.assertEqual(ColorAutoSym.RED, ColorAutoSym((1, 0, 0)))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym('ff0000'))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym('FF0000'))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym('RED'))
        self.assertEqual(ColorAutoSym.RED, ColorAutoSym['RED'])
        self.assertEqual(ColorAutoSym.RED.value, 'Red')
        self.assertEqual(ColorAutoSym.RED.spanish, 'Roja')
        self.assertEqual(ColorAutoSym.RED.hex, 'ff0000')
        self.assertRaises(ValueError, ColorAutoSym, 'Roja')

        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym((0, 1, 0)))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym('00ff00'))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym('00FF00'))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym('GREEN'))
        self.assertEqual(ColorAutoSym.GREEN, ColorAutoSym['GREEN'])
        self.assertEqual(ColorAutoSym.GREEN.value, 'Green')
        self.assertEqual(ColorAutoSym.GREEN.spanish, 'Verde')
        self.assertEqual(ColorAutoSym.GREEN.hex, '00ff00')
        self.assertRaises(ValueError, ColorAutoSym, 'Verde')

        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym((0, 0, 1)))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym('0000ff'))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym('0000FF'))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym('BLUE'))
        self.assertEqual(ColorAutoSym.BLUE, ColorAutoSym['BLUE'])
        self.assertEqual(ColorAutoSym.BLUE.value, 'Blue')
        self.assertEqual(ColorAutoSym.BLUE.spanish, 'Azul')
        self.assertEqual(ColorAutoSym.BLUE.hex, '0000ff')
        self.assertRaises(ValueError, ColorAutoSym, 'Azul')

        class ColorAutoIntSym(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):
            RED = auto(), 'Roja', (1, 0, 0), 'ff0000'
            GREEN = auto(), 'Verde', (0, 1, 0), '00ff00'
            BLUE = auto(), 'Azul', (0, 0, 1), '0000ff'

        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym['RED'])
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym['GREEN'])
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym['BLUE'])
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym(1))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym(2))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym(3))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym('1'))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym('2'))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym('3'))

        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym((1, 0, 0)))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym('ff0000'))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym('FF0000'))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym('RED'))
        self.assertEqual(ColorAutoIntSym.RED, ColorAutoIntSym['RED'])
        self.assertEqual(ColorAutoIntSym.RED.value, 1)
        self.assertEqual(ColorAutoIntSym.RED.spanish, 'Roja')
        self.assertEqual(ColorAutoIntSym.RED.hex, 'ff0000')
        self.assertRaises(ValueError, ColorAutoIntSym, 'Roja')

        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym((0, 1, 0)))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym('00ff00'))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym('00FF00'))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym('GREEN'))
        self.assertEqual(ColorAutoIntSym.GREEN, ColorAutoIntSym['GREEN'])
        self.assertEqual(ColorAutoIntSym.GREEN.value, 2)
        self.assertEqual(ColorAutoIntSym.GREEN.spanish, 'Verde')
        self.assertEqual(ColorAutoIntSym.GREEN.hex, '00ff00')
        self.assertRaises(ValueError, ColorAutoIntSym, 'Verde')

        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym((0, 0, 1)))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym('0000ff'))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym('0000FF'))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym('BLUE'))
        self.assertEqual(ColorAutoIntSym.BLUE, ColorAutoIntSym['BLUE'])
        self.assertEqual(ColorAutoIntSym.BLUE.value, 3)
        self.assertEqual(ColorAutoIntSym.BLUE.spanish, 'Azul')
        self.assertEqual(ColorAutoIntSym.BLUE.hex, '0000ff')
        self.assertRaises(ValueError, ColorAutoIntSym, 'Azul')

    def test_ignore(self):
        class Color(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True)
        ):

            _ignore_ = ['BLACK', 'NOT_ENOUGH_PROPS']

            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'
            BLACK = 4, 'Negra', (1, 1, 1), 'ffffff'
            NOT_ENOUGH_PROPS = 5, 'Not Enough'

        self.assertFalse(hasattr(Color, 'BLACK'))
        self.assertRaises(ValueError, Color, 4)
        self.assertRaises(ValueError, Color, (1, 1, 1))
        self.assertRaises(ValueError, Color, 'ffffff')

    def test_no_props(self):

        class Color(EnumProperties):
            RED = 1, 0, 0
            GREEN = 0, 1, 0
            BLUE = 0, 0, 1

        self.assertEqual(Color.RED.value, (1, 0, 0))
        self.assertEqual(Color.GREEN.value, (0, 1, 0))
        self.assertEqual(Color.BLUE.value, (0, 0, 1))

        class Color2(EnumProperties):
            RED = 1
            GREEN = 2
            BLUE = 3

        self.assertEqual(Color2.RED.value, 1)
        self.assertEqual(Color2.GREEN.value, 2)
        self.assertEqual(Color2.BLUE.value, 3)

    def test_not_enough_props(self):

        with self.assertRaises(ValueError):
            class Color(
                EnumProperties,
                p('prop1'),
                p('prop2')
            ):
                RED = 1, 'p1.1', 'p2.1'
                GREEN = 2, 'p1.2', 'p2.2'
                BLUE = 3, 'p1.3'

        with self.assertRaises(ValueError):
            class Color2(
                EnumProperties,
                p('prop1')
            ):
                RED = 1, 'p1.1'
                GREEN = 2
                BLUE = 3, 'p1.3'  # pragma: no cover

    def test_null_props(self):

        class Color(
            EnumProperties,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True, match_none=True)
        ):
            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, None, (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'
            BLACK = 4, 'Negra', (1, 1, 1), 'ffffff'
            TRANSPARENT = 5, 'Transparente', None, None

        self.assertEqual(Color.RED.value, 1)
        self.assertEqual(Color.RED.spanish, 'Roja')
        self.assertEqual(Color.RED.rgb, (1, 0, 0))
        self.assertEqual(Color.RED.hex, 'ff0000')

        self.assertEqual(Color.GREEN.value, 2)
        self.assertIsNone(Color.GREEN.spanish)
        self.assertEqual(Color.GREEN.rgb, (0, 1, 0))
        self.assertEqual(Color.GREEN.hex, '00ff00')

        self.assertEqual(Color.BLUE.value, 3)
        self.assertEqual(Color.BLUE.spanish, 'Azul')
        self.assertEqual(Color.BLUE.rgb, (0, 0, 1))
        self.assertEqual(Color.BLUE.hex, '0000ff')

        self.assertEqual(Color.BLACK.value, 4)
        self.assertEqual(Color.BLACK.spanish, 'Negra')
        self.assertEqual(Color.BLACK.rgb, (1, 1, 1))
        self.assertEqual(Color.BLACK.hex, 'ffffff')

        self.assertEqual(Color.TRANSPARENT.value, 5)
        self.assertEqual(Color.TRANSPARENT.spanish, 'Transparente')
        self.assertIsNone(Color.TRANSPARENT.rgb)
        self.assertIsNone(Color.TRANSPARENT.hex)

        self.assertEqual(Color.TRANSPARENT, Color(None))

    def test_examples(self):
        """
        Any example used in docs or readme should be tested here
        todo way to make this dry? sphinx plugin?
        """

        class Color(EnumProperties, p('rgb'), p('hex')):
            RED = auto(), (1, 0, 0), 'ff0000'
            GREEN = auto(), (0, 1, 0), '00ff00'
            BLUE = auto(), (0, 0, 1), '0000ff'

        self.assertEqual(Color.RED.rgb, (1, 0, 0))
        self.assertEqual(Color.GREEN.rgb, (0, 1, 0))
        self.assertEqual(Color.BLUE.rgb, (0, 0, 1))

        self.assertEqual(Color.RED.hex, 'ff0000')
        self.assertEqual(Color.GREEN.hex, '00ff00')
        self.assertEqual(Color.BLUE.hex, '0000ff')

        class Color(EnumProperties, s('rgb'), s('hex', case_fold=True)):

            RED = auto(), (1, 0, 0), '0xff0000'
            GREEN = auto(), (0, 1, 0), '0x00ff00'
            BLUE = auto(), (0, 0, 1), '0x0000ff'

        self.assertEqual(Color.RED, Color((1, 0, 0)))
        self.assertEqual(Color.GREEN, Color((0, 1, 0)))
        self.assertEqual(Color.BLUE, Color((0, 0, 1)))

        self.assertEqual(Color.RED, Color('0xff0000'))
        self.assertEqual(Color.GREEN, Color('0x00ff00'))
        self.assertEqual(Color.BLUE, Color('0x0000ff'))

        self.assertTrue(Color.RED == Color(hex(16711680)) == hex(16711680) == '0xff0000' == Color.RED)
        self.assertTrue(Color.RED == (1, 0, 0))
        self.assertTrue((1, 0, 0) == Color.RED)
        self.assertTrue(Color.RED != (0, 1, 0))
        self.assertTrue((0, 1, 0) != Color.RED)
        self.assertTrue(Color.RED == '0xFF0000')
        self.assertTrue('0xFF0000' == Color.RED)

        class MapBoxStyle(
            EnumProperties,
            s('label', case_fold=True),
            p('version')
        ):
            """
            https://docs.mapbox.com/api/maps/styles/
            """
            _symmetric_builtins_ = ['name', 'uri']

            STREETS = 'streets', 'Streets', 11
            OUTDOORS = 'outdoors', 'Outdoors', 11
            LIGHT = 'light', 'Light', 10
            DARK = 'dark', 'Dark', 10
            SATELLITE = 'satellite', 'Satellite', 9
            SATELLITE_STREETS = 'satellite-streets', 'Satellite Streets', 11
            NAVIGATION_DAY = 'navigation-day', 'Navigation Day', 1
            NAVIGATION_NIGHT = 'navigation-night', 'Navigation Night', 1

            @property
            def uri(self):
                return f'mapbox://styles/mapbox/{self.value}-v{self.version}'

            def __str__(self):
                return self.uri

        self.assertEqual(MapBoxStyle.STREETS.version, 11)
        self.assertEqual(MapBoxStyle.OUTDOORS.version, 11)
        self.assertEqual(MapBoxStyle.LIGHT.version, 10)
        self.assertEqual(MapBoxStyle.DARK.version, 10)
        self.assertEqual(MapBoxStyle.SATELLITE.version, 9)
        self.assertEqual(MapBoxStyle.SATELLITE_STREETS.version, 11)
        self.assertEqual(MapBoxStyle.NAVIGATION_DAY.version, 1)
        self.assertEqual(MapBoxStyle.NAVIGATION_NIGHT.version, 1)

        self.assertEqual(
            MapBoxStyle.STREETS.uri,
            'mapbox://styles/mapbox/streets-v11'
        )
        self.assertEqual(
            MapBoxStyle.LIGHT.uri,
            'mapbox://styles/mapbox/light-v10'
        )
        self.assertEqual(
            MapBoxStyle.DARK.uri,
            'mapbox://styles/mapbox/dark-v10'
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE.uri,
            'mapbox://styles/mapbox/satellite-v9'
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE_STREETS.uri,
            'mapbox://styles/mapbox/satellite-streets-v11'
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_DAY.uri,
            'mapbox://styles/mapbox/navigation-day-v1'
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_NIGHT.uri,
            'mapbox://styles/mapbox/navigation-night-v1'
        )

        self.assertEqual(
            str(MapBoxStyle.STREETS),
            'mapbox://styles/mapbox/streets-v11'
        )
        self.assertEqual(
            str(MapBoxStyle.LIGHT),
            'mapbox://styles/mapbox/light-v10'
        )
        self.assertEqual(
            str(MapBoxStyle.DARK),
            'mapbox://styles/mapbox/dark-v10'
        )
        self.assertEqual(
            str(MapBoxStyle.SATELLITE),
            'mapbox://styles/mapbox/satellite-v9'
        )
        self.assertEqual(
            str(MapBoxStyle.SATELLITE_STREETS),
            'mapbox://styles/mapbox/satellite-streets-v11'
        )
        self.assertEqual(
            str(MapBoxStyle.NAVIGATION_DAY),
            'mapbox://styles/mapbox/navigation-day-v1'
        )
        self.assertEqual(
            str(MapBoxStyle.NAVIGATION_NIGHT),
            'mapbox://styles/mapbox/navigation-night-v1'
        )

        self.assertEqual(
            MapBoxStyle.STREETS,
            MapBoxStyle('mapbox://styles/mapbox/streets-v11')
        )
        self.assertEqual(
            MapBoxStyle.LIGHT,
            MapBoxStyle('mapbox://styles/mapbox/light-v10')
        )
        self.assertEqual(
            MapBoxStyle.DARK,
            MapBoxStyle('mapbox://styles/mapbox/dark-v10')
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE,
            MapBoxStyle('mapbox://styles/mapbox/satellite-v9')
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE_STREETS,
            MapBoxStyle('mapbox://styles/mapbox/satellite-streets-v11')
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_DAY,
            MapBoxStyle('mapbox://styles/mapbox/navigation-day-v1')
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_NIGHT,
            MapBoxStyle('mapbox://styles/mapbox/navigation-night-v1')
        )

        self.assertEqual(
            MapBoxStyle.STREETS,
            MapBoxStyle('streets')
        )
        self.assertEqual(
            MapBoxStyle.LIGHT,
            MapBoxStyle('light')
        )
        self.assertEqual(
            MapBoxStyle.DARK,
            MapBoxStyle('dark')
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE,
            MapBoxStyle('satellite')
        )
        self.assertEqual(
            MapBoxStyle.SATELLITE_STREETS,
            MapBoxStyle('satellite-streets')
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_DAY,
            MapBoxStyle('navigation-day')
        )
        self.assertEqual(
            MapBoxStyle.NAVIGATION_NIGHT,
            MapBoxStyle('navigation-night')
        )

        class AddressRoute(
            EnumProperties,
            s('abbr', case_fold=True),
            s('alt', case_fold=True)
        ):
            _symmetric_builtins_ = [s('name', case_fold=True)]

            # name  value    abbr         alt
            ALLEY = 1, 'ALY', ['ALLEE', 'ALLY']
            AVENUE = 2, 'AVE', ['AV', 'AVEN', 'AVENU', 'AVN', 'AVNUE']
            CIRCLE = 3, 'CIR', ['CIRC', 'CIRCL', 'CRCL', 'CRCLE']

        self.assertTrue(
            AddressRoute.ALLEY == AddressRoute('Alley') ==
            AddressRoute('aly') == AddressRoute('ALLee') ==
            AddressRoute('ALLY')
        )

        self.assertTrue(
            AddressRoute.AVENUE == AddressRoute('Avenue') ==
            AddressRoute('AVE') == AddressRoute('av') ==
            AddressRoute('aven') == AddressRoute('AVENU') ==
            AddressRoute('Avn') == AddressRoute('AvnUE')
        )

        self.assertTrue(
            AddressRoute.CIRCLE == AddressRoute('circle') ==
            AddressRoute('Cir') == AddressRoute('CIRC') ==
            AddressRoute('circl') == AddressRoute('crcl') ==
            AddressRoute('crCle') == AddressRoute('crCLE')
        )

    def test_properties_conflict(self):
        """ enum_properties is reserved - test that we get an exception """

        with self.assertRaises(ValueError):
            class PropConflict(EnumProperties, p('_properties_')):
                ONE = auto(), (1, 2, 3)  # pragma: no cover
                TWO = auto(), (3, 4, 5)  # pragma: no cover

        with self.assertRaises(ValueError):
            class PropConflict(EnumProperties, p('prop')):
                _properties_ = None

                ONE = auto(), (1, 2, 3)  # pragma: no cover
                TWO = auto(), (3, 4, 5)  # pragma: no cover

    def test_precedence(self):

        class PriorityEx(
            EnumProperties,
            s('prop1'),
            s('prop2', case_fold=True)
        ):
            ONE = 0, '1', [3, 4]
            TWO = 1, '2', [3, '4']
            THREE = 2, '3', [3, 4]

        self.assertEqual(PriorityEx(0), PriorityEx.ONE)
        self.assertEqual(PriorityEx('1'), PriorityEx.ONE)
        self.assertEqual(PriorityEx(3), PriorityEx.ONE)
        self.assertEqual(PriorityEx('3'), PriorityEx.THREE)
        self.assertEqual(PriorityEx(4), PriorityEx.ONE)
        self.assertEqual(PriorityEx('4'), PriorityEx.TWO)

    def test_type_coercion_precedence(self):
        """
        test that type coercion is attempted in the same precedence order as
        value resolution.
        """
        class HashableType:
            def __init__(self, value):
                self.value = value

            def __eq__(self, other):
                return (
                    self.__class__ is other.__class__ and
                    self.value == other.value
                )

            def __hash__(self):
                return self.value.__hash__()

        class Type1(HashableType):
            pass

        class Type2(HashableType):
            pass

        class PriorityEx(EnumProperties, s('prop1'), s('prop2')):
            ONE = 2, Type1(0), Type2(1)
            TWO = 3, Type2(0), Type1(1)

        # coercion to Type1 should be tried before coercion to type 2
        self.assertEqual(PriorityEx(Type1(0)), PriorityEx.ONE)
        self.assertEqual(PriorityEx(Type2(0)), PriorityEx.TWO)
        self.assertEqual(PriorityEx(Type1(1)), PriorityEx.TWO)
        self.assertEqual(PriorityEx(Type2(1)), PriorityEx.ONE)

        self.assertEqual(PriorityEx(0), PriorityEx.ONE)
        self.assertEqual(PriorityEx(1), PriorityEx.TWO)

    def test_hashable_enums(self):

        class HashableEnum1(Enum):
            VAL0 = 0
            VAL1 = 1
            VAL2 = 2

        class HashableEnum2(Enum):
            VAL0 = 0
            VAL1 = 1
            VAL2 = 2

        self.assertTrue(isinstance(HashableEnum1.VAL0, Hashable))
        self.assertTrue(isinstance(HashableEnum2.VAL1, Hashable))

        class TransitiveEnum(EnumProperties, p('label'), s('pos')):
            VAL0 = 0, 'Value 0', HashableEnum1.VAL0
            VAL1 = 1, 'Value 1', HashableEnum1.VAL1
            VAL2 = 2, 'Value 2', HashableEnum2.VAL2

        self.assertTrue(isinstance(TransitiveEnum.VAL2, Hashable))

        self.assertEqual(TransitiveEnum(HashableEnum1.VAL0), TransitiveEnum.VAL0)
        self.assertEqual(TransitiveEnum(HashableEnum1.VAL1), TransitiveEnum.VAL1)
        self.assertEqual(TransitiveEnum(HashableEnum2.VAL2), TransitiveEnum.VAL2)

        self.assertRaises(ValueError, TransitiveEnum, HashableEnum1.VAL2)
        self.assertRaises(ValueError, TransitiveEnum, HashableEnum2.VAL0)
        self.assertRaises(ValueError, TransitiveEnum, HashableEnum2.VAL1)

        test_dict = {
            HashableEnum1.VAL0: 'Zero',
            HashableEnum1.VAL1: 'One',
            HashableEnum1.VAL2: 'Two',
            HashableEnum2.VAL0: 'zero',
            HashableEnum2.VAL1: 'one',
            HashableEnum2.VAL2: 'two',
            TransitiveEnum.VAL0: 'ZERO',
            TransitiveEnum.VAL1: 'ONE',
            TransitiveEnum.VAL2: 'TWO',
        }

        self.assertEqual(test_dict[HashableEnum1.VAL0], 'Zero')
        self.assertEqual(test_dict[HashableEnum1.VAL1], 'One')
        self.assertEqual(test_dict[HashableEnum1.VAL2], 'Two')

        self.assertEqual(test_dict[HashableEnum2.VAL0], 'zero')
        self.assertEqual(test_dict[HashableEnum2.VAL1], 'one')
        self.assertEqual(test_dict[HashableEnum2.VAL2], 'two')

        self.assertEqual(test_dict[TransitiveEnum.VAL0], 'ZERO')
        self.assertEqual(test_dict[TransitiveEnum.VAL1], 'ONE')
        self.assertEqual(test_dict[TransitiveEnum.VAL2], 'TWO')


class TestFlags(TestCase):

    def test_int_flag(self):

        class Perm(
            IntFlagProperties,
            s('label', case_fold=True),
        ):

            R = 1, 'read'
            W = 2, 'write'
            X = 4, 'execute'
            RWX = 7, 'all'

            @property
            def custom_prop(self):
                return self.label.upper()

        self.assertEqual(Perm.R.label, 'read')
        self.assertEqual(Perm.W.label, 'write')
        self.assertEqual(Perm.X.label, 'execute')
        self.assertEqual(Perm.RWX.label, 'all')

        self.assertTrue(Perm.R is Perm('read'))
        self.assertTrue(Perm.W is Perm('write'))
        self.assertTrue(Perm.X is Perm('execute'))
        self.assertTrue(Perm.RWX is Perm('all'))

        self.assertEqual(Perm.W.custom_prop, 'WRITE')
        self.assertEqual(Perm.RWX.custom_prop, 'ALL')

        self.assertTrue((Perm.R | Perm.W | Perm.X) is Perm('RWX'))
        self.assertTrue(Perm([Perm.R, Perm.W, Perm.X]) is Perm('RWX'))
        self.assertTrue(Perm({'read', 'write', 'execute'}) is Perm('RWX'))
        self.assertTrue(
            Perm((val for val in (Perm.R, 'write', 4))) is Perm('RWX')
        )

        self.assertEqual((Perm.R | Perm.W | Perm.X).label, 'all')
        self.assertEqual(
            (Perm('READ') | Perm('write') | Perm('X')).label,
            'all'
        )

        self.assertFalse(hasattr((Perm.R | Perm.W), 'label'))
        self.assertFalse(hasattr((Perm.W | Perm.X), 'label'))
        self.assertFalse(hasattr((Perm.R | Perm.X), 'label'))

        self.assertFalse(bool(Perm.R & Perm.X))
        self.assertFalse(hasattr((Perm.R & Perm.X), 'label'))

        self.assertCountEqual((Perm.R | Perm.W).flagged, [Perm.R, Perm.W])
        self.assertCountEqual(Perm.RWX.flagged, [Perm.R, Perm.W, Perm.X])
        self.assertEqual(Perm.R.flagged, [Perm.R])
        self.assertEqual((Perm.R & Perm.X).flagged, [])

        self.assertEqual(len((Perm.R | Perm.W)), 2)
        self.assertEqual(len(Perm.RWX), 3)
        self.assertEqual(len(Perm.R), 1)
        self.assertEqual(len((Perm.R & Perm.X)), 0)

        self.assertEqual(Perm([]), Perm(0))
        self.assertEqual(Perm({}), Perm(0))
        self.assertEqual(Perm((item for item in [])), Perm(0))

        if sys.version_info >= (3, 11):  # pragma: no cover
            from enum import show_flag_values
            self.assertEqual(show_flag_values(Perm.R | Perm.X), [1, 4])
            self.assertEqual(show_flag_values(Perm.RWX), [1, 2, 4])

    def test_flag(self):

        class Perm(
            FlagProperties,
            s('label', case_fold=True),
        ):

            R = auto(), 'read'
            W = auto(), 'write'
            X = auto(), 'execute'
            RWX = R | W | X, 'all'

            @property
            def custom_prop(self):
                return self.label.upper()


        self.assertEqual(Perm.R.label, 'read')
        self.assertEqual(Perm.W.label, 'write')
        self.assertEqual(Perm.X.label, 'execute')

        self.assertEqual(Perm.RWX.label, 'all')

        self.assertTrue(Perm.R is Perm('read'))
        self.assertTrue(Perm.W is Perm('write'))
        self.assertTrue(Perm.X is Perm('execute'))
        self.assertTrue(Perm.RWX is Perm('all'))

        self.assertEqual(Perm.W.custom_prop, 'WRITE')
        self.assertEqual(Perm.RWX.custom_prop, 'ALL')

        self.assertTrue((Perm.R | Perm.W | Perm.X) is Perm('RWX'))
        self.assertTrue(Perm([Perm.R, Perm.W, Perm.X]) is Perm('RWX'))
        self.assertTrue(Perm({'read', 'write', 'execute'}) is Perm('RWX'))
        self.assertTrue(
            Perm((val for val in (Perm.R, 'write', 4))) is Perm('RWX')
        )

        self.assertEqual((Perm.R | Perm.W | Perm.X).label, 'all')
        self.assertEqual(
            (Perm('READ') | Perm('write') | Perm('X')).label,
            'all'
        )

        self.assertFalse(hasattr((Perm.R | Perm.W), 'label'))
        self.assertFalse(hasattr((Perm.W | Perm.X), 'label'))
        self.assertFalse(hasattr((Perm.R | Perm.X), 'label'))

        self.assertFalse(bool(Perm.R & Perm.X))
        self.assertFalse(hasattr((Perm.R & Perm.X), 'label'))

        self.assertCountEqual((Perm.R | Perm.W).flagged, [Perm.R, Perm.W])
        self.assertCountEqual(Perm.RWX.flagged, [Perm.R, Perm.W, Perm.X])
        self.assertEqual(Perm.R.flagged, [Perm.R])
        self.assertEqual((Perm.R & Perm.X).flagged, [])

        self.assertEqual(len((Perm.R | Perm.W)), 2)
        self.assertEqual(len(Perm.RWX), 3)
        self.assertEqual(len(Perm.R), 1)
        self.assertEqual(len((Perm.R & Perm.X)), 0)

        self.assertEqual(Perm([]), Perm(0))
        self.assertEqual(Perm({}), Perm(0))
        self.assertEqual(Perm((item for item in [])), Perm(0))

        self.assertCountEqual(
            [perm for perm in Perm.RWX],
            [Perm.R, Perm.W, Perm.X]
        )

        self.assertCountEqual(
            [perm for perm in (Perm.R | Perm.X)],
            [Perm.R, Perm.X]
        )

        self.assertCountEqual(
            [perm for perm in Perm.R],
            [Perm.R]
        )

        self.assertCountEqual(
            [perm for perm in (Perm.R & Perm.X)],
            []
        )

    def test_flag_def_order(self):

        from enum import IntFlag

        class PermNative(IntFlag):

            R = auto()
            W = auto()
            RW = R | W
            X = auto()
            RWX = R | W | X

        self.assertEqual(PermNative.R.value, 1)
        self.assertEqual(PermNative.W.value, 2)
        self.assertEqual(PermNative.RW.value, 3)
        self.assertEqual(PermNative.X.value, 4)
        self.assertEqual(PermNative.RWX.value, 7)

        class PermProperties(FlagProperties, s('label', case_fold=True)):

            R = auto(), 'read'
            W = auto(), 'write'
            RW = R | W, 'read/write'
            X = auto(), 'execute'
            RWX = R | W | X, 'all'

        self.assertEqual(PermProperties.R.value, 1)
        self.assertEqual(PermProperties.W.value, 2)
        self.assertEqual(PermProperties.RW.value, 3)
        self.assertEqual(PermProperties.X.value, 4)
        self.assertEqual(PermProperties.RWX.value, 7)

        self.assertEqual(
            (PermProperties.R | PermProperties.W).label,
            'read/write'
        )
        self.assertFalse(
            hasattr((PermProperties.W | PermProperties.X), 'label')
        )
        self.assertFalse(
            hasattr((PermProperties.R | PermProperties.X), 'label')
        )
        self.assertEqual(
            (PermProperties.R | PermProperties.W | PermProperties.X).label,
            'all'
        )
        self.assertEqual(PermProperties.R.label, 'read')
        self.assertEqual(PermProperties.W.label, 'write')

        self.assertEqual(PermProperties.RW, PermProperties('read/write'))
        self.assertEqual(PermProperties.RW, PermProperties(['read', 'write']))
        self.assertEqual(
            (PermProperties.W | PermProperties.X),
            PermProperties(['write', 'execute'])
        )
        self.assertEqual(PermProperties.R, PermProperties('read'))
        self.assertEqual(PermProperties.W, PermProperties('write'))
        self.assertEqual(PermProperties.X, PermProperties('execute'))
        self.assertEqual(PermProperties.RWX, PermProperties('all'))

        class IntPermProperties(IntFlagProperties, s('label', case_fold=True)):
            R = auto(), 'read'
            W = auto(), 'write'
            RW = R | W, 'read/write'
            X = auto(), 'execute'
            RWX = R | W | X, 'all'

        self.assertEqual(IntPermProperties.R.value, 1)
        self.assertEqual(IntPermProperties.W.value, 2)
        self.assertEqual(IntPermProperties.RW.value, 3)
        self.assertEqual(IntPermProperties.X.value, 4)
        self.assertEqual(IntPermProperties.RWX.value, 7)

        self.assertEqual(
            (IntPermProperties.R | IntPermProperties.W).label,
            'read/write'
        )
        self.assertFalse(
            hasattr((IntPermProperties.W | IntPermProperties.X), 'label')
        )
        self.assertFalse(
            hasattr((IntPermProperties.R | IntPermProperties.X), 'label')
        )
        self.assertEqual(
            (IntPermProperties.R | IntPermProperties.W | IntPermProperties.X).label,
            'all'
        )
        self.assertEqual(IntPermProperties.R.label, 'read')
        self.assertEqual(IntPermProperties.W.label, 'write')

        self.assertEqual(IntPermProperties.RW, IntPermProperties('read/write'))
        self.assertEqual(IntPermProperties.RW, IntPermProperties(['read', 'write']))
        self.assertEqual(
            (IntPermProperties.W | IntPermProperties.X),
            IntPermProperties(['write', 'execute'])
        )
        self.assertEqual(IntPermProperties.R, IntPermProperties('read'))
        self.assertEqual(IntPermProperties.W, IntPermProperties('write'))
        self.assertEqual(IntPermProperties.X, IntPermProperties('execute'))
        self.assertEqual(IntPermProperties.RWX, IntPermProperties('all'))


    if sys.version_info >= (3, 11):  # pragma: no cover
        def test_flag_boundary_enum(self):
            """
            Test the boundary functionality introduced in 3.11
            """
            from enum import CONFORM, EJECT, KEEP, STRICT

            class StrictFlag(IntFlagProperties, p('label'), boundary=STRICT):
                RED = auto(), 'red'
                GREEN = auto(), 'green'
                BLUE = auto(), 'blue'

            with self.assertRaises(ValueError):
                StrictFlag(2 ** 2 + 2 ** 4)

            self.assertEqual(StrictFlag.BLUE.label, 'blue')
            self.assertEqual(StrictFlag.RED.label, 'red')
            self.assertEqual(StrictFlag.GREEN.label, 'green')
            self.assertFalse(hasattr((StrictFlag.BLUE | StrictFlag.RED), 'label'))

            class ConformFlag(FlagProperties, s('label'), boundary=CONFORM):
                RED = auto(), 'red'
                GREEN = auto(), 'green'
                BLUE = auto(), 'blue'

            self.assertEqual(ConformFlag.BLUE, ConformFlag(2 ** 2 + 2 ** 4))
            self.assertEqual(ConformFlag(2 ** 2 + 2 ** 4).label, 'blue')
            self.assertEqual(
                ConformFlag(2 ** 2 + 2 ** 4).label,
                ConformFlag('blue')
            )

            class EjectFlag(IntFlagProperties, s('label'), boundary=EJECT):
                RED = auto(), 'red'
                GREEN = auto(), 'green'
                BLUE = auto(), 'blue'

            self.assertEqual(EjectFlag(2 ** 2 + 2 ** 4), 20)
            self.assertFalse(hasattr(EjectFlag(2 ** 2 + 2 ** 4), 'label'))
            self.assertEqual(EjectFlag.GREEN, EjectFlag('green'))
            self.assertEqual(
                (EjectFlag.GREEN | EjectFlag.BLUE),
                EjectFlag(['blue', 'green'])
            )

            class KeepFlag(
                FlagProperties, s('label'),  p('hex'), boundary=KEEP
            ):
                RED = auto(), 'red', 0xFF0000
                GREEN = auto(), 'green', 0x00FF00
                BLUE = auto(), 'blue', 0x0000FF

            self.assertEqual(KeepFlag(2**2 + 2**4).value, 20)
            self.assertTrue(KeepFlag.BLUE in KeepFlag(2**2 + 2**4))
            self.assertFalse(hasattr(KeepFlag(2**2 + 2**4), 'label'))
            self.assertEqual(
                [flg.label for flg in KeepFlag(2**2 + 2**4)],
                ['blue']
            )

    if sys.version_info >= (3, 11):  # pragma: no cover
        def test_enum_verify(self):
            from enum import CONTINUOUS, NAMED_FLAGS, UNIQUE, verify

            with self.assertRaises(ValueError):

                @verify(UNIQUE)
                class Color(EnumProperties, s('label')):
                    RED = 1, 'red'
                    GREEN = 2, 'green'
                    BLUE = 3, 'blue'
                    CRIMSON = 1, 'crimson'

            @verify(UNIQUE)
            class Color(EnumProperties, p('label')):
                RED = 1, 'red'
                GREEN = 2, 'green'
                BLUE = 3, 'blue'
                CRIMSON = 4, 'crimson'

            self.assertEqual(Color.GREEN.label, 'green')
            self.assertEqual(Color.CRIMSON.label, 'crimson')

            with self.assertRaises(ValueError):
                # this throws an error if label is symmetric!
                @verify(UNIQUE)
                class Color(EnumProperties, s('label')):
                    RED = 1, 'red'
                    GREEN = 2, 'green'
                    BLUE = 3, 'blue'
                    CRIMSON = 4, 'crimson'

            with self.assertRaises(ValueError):
                @verify(CONTINUOUS)
                class Color(IntEnumProperties, s('label')):
                    RED = 1, 'red'
                    GREEN = 2, 'green'
                    BLUE = 5, 'blue'

            @verify(CONTINUOUS)
            class Color(IntEnumProperties, s('label')):
                RED = 1, 'red'
                GREEN = 2, 'green'
                BLUE = 3, 'blue'

            self.assertEqual(Color.BLUE.label, 'blue')
            self.assertEqual(Color.RED, Color('red'))

            with self.assertRaises(ValueError):
                @verify(NAMED_FLAGS)
                class Color(IntFlagProperties, s('label')):
                    RED = 1, 'red'
                    GREEN = 2, 'green'
                    BLUE = 4, 'blue'
                    WHITE = 15, 'white'
                    NEON = 31, 'neon'

            @verify(NAMED_FLAGS)
            class Color(IntFlagProperties, s('label')):
                RED = 1, 'red'
                GREEN = 2, 'green'
                BLUE = 4, 'blue'
                WHITE = 16, 'white'
                NEON = 32, 'neon'

            self.assertEqual(Color.BLUE | Color.NEON, Color(['blue', 'neon']))

    if sys.version_info >= (3, 11):  # pragma: no cover
        def test_enum_property(self):
            from enum import property as enum_property

            class Color(EnumProperties, s('label')):
                RED = 1, 'red'
                GREEN = 2, 'green'
                BLUE = 3, 'blue'

                @enum_property
                def blue(self):
                    return 'whatever'

            self.assertEqual(Color.BLUE.blue, 'whatever')
            self.assertEqual(Color.blue, Color.BLUE)

            # attempting to assign an enum_property to a class as an existing
            # property name should raise an AttributeError
            with self.assertRaises(AttributeError):
                class Color(EnumProperties, s('label')):
                    RED = 1, 'red'
                    GREEN = 2, 'green'
                    BLUE = 3, 'blue'

                    @enum_property
                    def label(self):
                        return 'label'


class TestPickle(TestCase):

    def do_pickle_test(self, ipt):
        buffer = BytesIO()
        pickle.dump(ipt, buffer, pickle.HIGHEST_PROTOCOL)
        buffer.seek(0)
        opt = pickle.load(buffer)
        return ipt is opt

    def test_pickle(self):
        from enum_properties.tests.pickle_enums import Color, PriorityEx
        self.assertTrue(self.do_pickle_test(PriorityEx.ONE))
        self.assertTrue(self.do_pickle_test(PriorityEx.TWO))
        self.assertTrue(self.do_pickle_test(PriorityEx.THREE))

        self.assertTrue(self.do_pickle_test(PriorityEx('1')))
        self.assertTrue(self.do_pickle_test(PriorityEx('2')))
        self.assertTrue(self.do_pickle_test(PriorityEx(3)))

        self.assertTrue(self.do_pickle_test(Color.RED))
        self.assertTrue(self.do_pickle_test(Color.GREEN))
        self.assertTrue(self.do_pickle_test(Color.BLUE))

    def test_flag_pickle(self):
        from enum_properties.tests.pickle_enums import IntPerm, Perm
        self.assertTrue(self.do_pickle_test(Perm.R))
        self.assertTrue(self.do_pickle_test(Perm.W))
        self.assertTrue(self.do_pickle_test(Perm.X))
        self.assertTrue(self.do_pickle_test(Perm.RWX))
        self.assertTrue(self.do_pickle_test(Perm.R | Perm.W | Perm.X))
        self.assertTrue(self.do_pickle_test(Perm.R | Perm.W))

        self.assertTrue(self.do_pickle_test(IntPerm.R))
        self.assertTrue(self.do_pickle_test(IntPerm.W))
        self.assertTrue(self.do_pickle_test(IntPerm.X))
        self.assertTrue(self.do_pickle_test(IntPerm.RWX))
        self.assertTrue(self.do_pickle_test(IntPerm.R | IntPerm.W | IntPerm.X))
        self.assertTrue(self.do_pickle_test(IntPerm.W | IntPerm.X))


class TestNestedClassOnEnum(TestCase):
    """
    Should be able to nest classes on Enumerations!
    """

    def test_enum_can_be_types(self):

        class Type1:
            pass

        class Type2:
            pass

        class Type3:
            pass

        class TestEnum(EnumProperties, s('label')):

            VALUE1 = Type1, 'value1'
            VALUE2 = Type2, 'value2'
            VALUE3 = Type3, 'value3'

        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )

        self.assertEqual(
            [en.label for en in TestEnum],
            [
                TestEnum.VALUE1.label,
                TestEnum.VALUE2.label,
                TestEnum.VALUE3.label
            ]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum('value1'), TestEnum('value2'), TestEnum('value3')]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum(Type1), TestEnum(Type2), TestEnum(Type3)]
        )
        self.assertEqual(
            [en.value for en in TestEnum],
            [Type1, Type2, Type3]
        )

    def test_nested_classes(self):

        class TestEnum(EnumProperties, s('label')):

            VALUE1 = auto(), 'value1'
            VALUE2 = auto(), 'value2'
            VALUE3 = auto(), 'value3'

            def function(self):
                return self.value

            @classmethod
            def default(cls):
                return cls.VALUE1

            @staticmethod
            def static_property():
                return 'static_prop'

            @nonmember
            class NestedClass:

                @property
                def prop(self):
                    return 'nested'

        self.assertEqual(TestEnum.VALUE1.function(), TestEnum.VALUE1.value)
        self.assertEqual(TestEnum.VALUE2.function(), TestEnum.VALUE2.value)
        self.assertEqual(TestEnum.VALUE3.function(), TestEnum.VALUE3.value)
        self.assertEqual(TestEnum.default(), TestEnum.VALUE1)
        self.assertEqual(TestEnum.static_property(), 'static_prop')
        self.assertEqual(TestEnum.NestedClass().prop, 'nested')
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )
        self.assertEqual(
            [en.label for en in TestEnum],
            [
                TestEnum.VALUE1.label,
                TestEnum.VALUE2.label,
                TestEnum.VALUE3.label
            ]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum('value1'), TestEnum('value2'), TestEnum('value3')]
        )

    def test_nested_classes_as_values(self):

        class TestEnum(EnumProperties, s('label')):

            @nonmember
            class Type1:
                pass

            @nonmember
            class Type2:
                pass

            @nonmember
            class Type3:
                pass

            VALUE1 = member(Type1), 'value1'
            VALUE2 = member(Type2), 'value2'
            VALUE3 = member(Type3), 'value3'

        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )

        self.assertEqual(
            [en.label for en in TestEnum],
            [
                TestEnum.VALUE1.label,
                TestEnum.VALUE2.label,
                TestEnum.VALUE3.label
            ]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum('value1'), TestEnum('value2'), TestEnum('value3')]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [
                TestEnum(TestEnum.Type1),
                TestEnum(TestEnum.Type2),
                TestEnum(TestEnum.Type3)
            ]
        )
        self.assertEqual(
            [en.value for en in TestEnum],
            [TestEnum.Type1, TestEnum.Type2, TestEnum.Type3]
        )

    def test_nested_classes_as_values_no_props(self):

        class TestEnum(EnumProperties):

            @nonmember
            class Type1:
                pass

            @nonmember
            class Type2:
                pass

            @nonmember
            class Type3:
                pass

            VALUE1 = member(Type1)
            VALUE2 = member(Type2)
            VALUE3 = member(Type3)

        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [
                TestEnum(TestEnum.Type1),
                TestEnum(TestEnum.Type2),
                TestEnum(TestEnum.Type3)
            ]
        )
        self.assertEqual(
            [en.value for en in TestEnum],
            [TestEnum.Type1, TestEnum.Type2, TestEnum.Type3]
        )

    def test_example(self):

        class MyEnum(EnumProperties, p('label')):

            @nonmember
            class Type1:
                pass

            @nonmember
            class Type2:
                pass

            @nonmember
            class Type3:
                pass

            VALUE1 = member(Type1), 'label1'
            VALUE2 = member(Type2), 'label2'
            VALUE3 = member(Type3), 'label3'

        # nested classes are usable like normal
        self.assertEqual(MyEnum.Type1, MyEnum.VALUE1.value)
        self.assertEqual(MyEnum.Type2, MyEnum.VALUE2.value)
        self.assertEqual(MyEnum.Type3, MyEnum.VALUE3.value)
        self.assertEqual(len(MyEnum), 3)
        self.assertTrue(MyEnum.Type1().__class__ is MyEnum.Type1)
        self.assertTrue(MyEnum.Type2().__class__ is MyEnum.Type2)
        self.assertTrue(MyEnum.Type3().__class__ is MyEnum.Type3)

    if sys.version_info >= (3, 11):  # pragma: no cover
        def test_nonmember_decorator(self):

            class MyEnum(EnumProperties, p('label')):

                @nonmember
                class Type1:
                    pass

                @nonmember
                class Type2:
                    pass

                @nonmember
                class Type3:
                    pass

                VALUE1 = member(Type1), 'label1'
                VALUE2 = member(Type2), 'label2'
                VALUE3 = member(Type3), 'label3'
                VALUE4 = nonmember((Type3, 'label4'))

            # nested classes are usable like normal
            self.assertEqual(MyEnum.Type1, MyEnum.VALUE1.value)
            self.assertEqual(MyEnum.Type2, MyEnum.VALUE2.value)
            self.assertEqual(MyEnum.Type3, MyEnum.VALUE3.value)
            self.assertEqual(len(MyEnum), 3)
            self.assertEqual(MyEnum.VALUE4, (MyEnum.Type3, 'label4'))
            self.assertTrue(MyEnum.Type1().__class__ is MyEnum.Type1)
            self.assertTrue(MyEnum.Type2().__class__ is MyEnum.Type2)
            self.assertTrue(MyEnum.Type3().__class__ is MyEnum.Type3)

        def test_member_decorator(self):

            with self.assertRaises(ValueError):
                class MyEnum(EnumProperties, p('label')):

                    @member
                    class Type1:
                        pass

                    @member
                    class Type2:
                        pass

                    @member
                    class Type3:
                        pass

                    VALUE1 = Type1, 'label1'
                    VALUE2 = Type2, 'label2'
                    VALUE3 = Type3, 'label3'

    def test_3_13_member_compat(self):
        class MyEnum(EnumProperties):
            @member  # this is transparent on < 3.11
            class Type1:
                pass

            @member  # this is transparent on < 3.11
            class Type2:
                pass

            @member  # this is transparent on < 3.11
            class Type3:
                pass

            VALUE1 = Type1, 'label1'
            VALUE2 = Type2, 'label2'
            VALUE3 = Type3, 'label3'

        self.assertEqual(MyEnum.Type1.value, MyEnum.VALUE1.value[0])
        self.assertEqual(MyEnum.Type2.value, MyEnum.VALUE2.value[0])
        self.assertEqual(MyEnum.Type3.value, MyEnum.VALUE3.value[0])
        self.assertEqual(len(MyEnum), 6)
        self.assertTrue(MyEnum.Type1.value().__class__ is MyEnum.Type1.value)
        self.assertTrue(MyEnum.Type2.value().__class__ is MyEnum.Type2.value)
        self.assertTrue(MyEnum.Type3.value().__class__ is MyEnum.Type3.value)


class TestGiantFlags(TestCase):

    def test_over64_flags(self):

        class BigFlags(IntFlagProperties, p('label')):

            ONE = 2**0, 'one'
            MIDDLE = 2**64, 'middle'
            MIXED = ONE | MIDDLE, 'mixed'
            LAST = 2**128, 'last'

        self.assertEqual((BigFlags.ONE | BigFlags.LAST).value, 2**128 + 1)
        self.assertEqual(
            (BigFlags.MIDDLE | BigFlags.LAST).value, 2**128 + 2**64
        )
        self.assertEqual(
            (BigFlags.MIDDLE | BigFlags.ONE).label, 'mixed'
        )


class TestSpecialize(TestCase):
    """
    Test the specialize decorator
    """

    def test_specialize(self):

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

        self.assertEqual(SpecializedEnum.ONE.method(), 'method_one()')
        self.assertEqual(SpecializedEnum.TWO.method(), 'method_two()')
        self.assertEqual(SpecializedEnum.THREE.method(), 'method_three()')

    def test_specialize_default(self):

        class SpecializedEnum(EnumProperties, s('label')):

            ONE = 1, 'one'
            TWO = 2, 'two'
            THREE = 3, 'three'

            def test(self):
                return 'test_default()'

            @specialize(THREE)
            def test(self):
                return 'test_three()'

        self.assertEqual(SpecializedEnum.ONE.test(), 'test_default()')
        self.assertEqual(SpecializedEnum.TWO.test(), 'test_default()')
        self.assertEqual(SpecializedEnum.THREE.test(), 'test_three()')
        self.assertEqual(SpecializedEnum('three').test(), 'test_three()')

    def test_specialize_no_default(self):

        class SpecializedEnum(EnumProperties, s('label')):

            ONE = 1, 'one'
            TWO = 2, 'two'
            THREE = 3, 'three'

            @specialize(TWO)
            def test(self):
                return 'test_two()'

            @specialize(THREE)
            def test(self):
                return 'test_three()'

        self.assertFalse(hasattr(SpecializedEnum.ONE, 'test'))
        self.assertFalse(hasattr(SpecializedEnum('one'), 'test'))
        self.assertEqual(SpecializedEnum.TWO.test(), 'test_two()')
        self.assertEqual(SpecializedEnum['TWO'].test(), 'test_two()')
        self.assertEqual(SpecializedEnum.THREE.test(), 'test_three()')

    def test_specialize_class_method(self):
        class SpecializedEnum(EnumProperties, s('label')):

            ONE   = 1, 'one'
            TWO   = 2, 'two'
            THREE = 3, 'three'

            @specialize(ONE)
            @classmethod
            def test(cls):
                return (1, cls)

            @specialize(TWO)
            @classmethod
            def test(cls):
                return (2, cls)

            @specialize(THREE)
            @classmethod
            def test(cls):
                return (3, cls)

        self.assertEqual(SpecializedEnum.ONE.test(), (1, SpecializedEnum))
        self.assertEqual(SpecializedEnum.TWO.test(), (2, SpecializedEnum))
        self.assertEqual(SpecializedEnum.THREE.test(), (3, SpecializedEnum))
        self.assertEqual(SpecializedEnum('two').test(), (2, SpecializedEnum))

    def test_specialize_static_method(self):

        class SpecializedEnum(EnumProperties, s('label')):

            ONE   = 1, 'one'
            TWO   = 2, 'two'
            THREE = 3, 'three'

            @specialize(ONE)
            @staticmethod
            def test():
                return 'test_one()'

            @specialize(TWO)
            @staticmethod
            def test():
                return 'test_two()'

            @specialize(THREE)
            @staticmethod
            def test():
                return 'test_three()'

        self.assertEqual(SpecializedEnum.ONE.test(), 'test_one()')
        self.assertEqual(SpecializedEnum.TWO.test(), 'test_two()')
        self.assertEqual(SpecializedEnum.THREE.test(), 'test_three()')
        self.assertEqual(SpecializedEnum('two').test(), 'test_two()')

    def test_specialize_arguments(self):

        class SpecializedEnum(EnumProperties, s('label')):

            ONE   = 1, 'one'
            TWO   = 2, 'two'
            THREE = 3, 'three'

            @specialize(ONE)
            def test(self, count=1):
                return self.label * count

            @specialize(TWO)
            def test(self, count=2):
                return self.label * count

            @specialize(THREE)
            def test(self, count=3):
                return self.label * count

        self.assertEqual(SpecializedEnum.ONE.test(), 'one')
        self.assertEqual(SpecializedEnum.TWO.test(), 'twotwo')
        self.assertEqual(SpecializedEnum.THREE.test(), 'threethreethree')
        self.assertEqual(SpecializedEnum('two').test(count=1), 'two')

    def test_specialize_multiple_lists(self):

        class SpecializedEnum(EnumProperties, s('label')):
            ONE = 1, 'one'
            TWO = 2, 'two'
            THREE = 3, 'three'

            @specialize(ONE)
            def test(self, count=1):
                return self.label * count

            @specialize(TWO, THREE)
            def test(self, count=2):
                return self.label * count

        self.assertEqual(SpecializedEnum.ONE.test(), 'one')
        self.assertEqual(SpecializedEnum.TWO.test(), 'twotwo')
        self.assertEqual(SpecializedEnum.THREE.test(), 'threethree')


class NoneCoercionTests(TestCase):

    def test_string_to_none_coercion_disabled(self):

        class EnumWithNones(EnumProperties, s('prop', match_none=True)):
            VALUE1 = 1, None
            VALUE2 = 2, 'label'

        self.assertRaises(ValueError, EnumWithNones, 'None')

        class EnumWithNones(
            EnumProperties, s('prop', case_fold=True, match_none=False)
        ):
            VALUE1 = 1, None
            VALUE2 = 2, 'label'

        self.assertRaises(ValueError, EnumWithNones, 'None')

        class EnumWithNones(EnumProperties):
            VALUE1 = None
            VALUE2 = 'label'

        self.assertRaises(ValueError, EnumWithNones, 'None')
        self.assertEqual(EnumWithNones(None), EnumWithNones.VALUE1)

    def test_none_to_string_coercion_disabled(self):

        class EnumWithNones(EnumProperties, s('prop', match_none=True)):
            VALUE1 = 1, 'None'
            VALUE2 = 2, 'label'

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones('None'), EnumWithNones.VALUE1)

        class EnumWithNones(
            EnumProperties, s('prop', case_fold=True, match_none=True)
        ):
            VALUE1 = 1, 'None'
            VALUE2 = 2, 'label'

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones('none'), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties, s('prop', match_none=False)):
            VALUE1 = 1, 'None'
            VALUE2 = 2, 'label'

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertEqual(EnumWithNones('None'), EnumWithNones.VALUE1)

        class EnumWithNones(EnumProperties):
            VALUE1 = 'None'
            VALUE2 = 'label'

        self.assertRaises(ValueError, EnumWithNones, None)
        self.assertRaises(KeyError, lambda x: EnumWithNones[x], None)
        self.assertEqual(EnumWithNones('None'), EnumWithNones.VALUE1)


class PerformanceAndMemoryChecks(TestCase):

    from enum_properties.tests.big_enum import ISOCountry

    def test_check_big_enum_size(self):
        """
        Memory benchmarks:

        v1.3.3 ISOCountry: 151966 bytes
        v1.4.0 ISOCountry: 105046 bytes
        """

        seen = {}
        total_size = 0
        for name, attr in vars(self.ISOCountry).items():
            total_size += sys.getsizeof(attr)
            seen[(id(attr))] = (name, sys.getsizeof(attr))

        for val in self.ISOCountry:
            for name, attr in vars(self.ISOCountry).items():
                if id(attr) not in seen:  # pragma: no cover
                    total_size += sys.getsizeof(attr)
                    seen[(id(attr))] = (name, sys.getsizeof(attr))

        print(
            'Total Memory footprint of ISOCountry: {} bytes'.format(total_size)
        )

    def test_property_access_time(self):
        """
        Access benchmarks:

        v1.3.3 ISOCountry: ~1.05 seconds (macbook M1 Pro)
        v1.4.0 ISOCountry: ~0.196 seconds (macbook M1 Pro) (5.3x faster)
        """

        # use perf counter to time the length of a for loop execution
        from time import perf_counter
        for_loop_time = perf_counter()
        for i in range(1000000):
            self.ISOCountry.US.full_name

        for_loop_time = perf_counter() - for_loop_time
        print('for loop time: {}'.format(for_loop_time))

    def test_symmetric_mapping(self):
        """
        Symmetric mapping benchmarks

        v1.4.0 ISOCountry: ~3 seconds (macbook M1 Pro)
        v1.4.1 ISOCountry: ~ seconds (macbook M1 Pro) (x faster)
        """
        self.assertEqual(
            self.ISOCountry(self.ISOCountry.US.full_name.lower()),
            self.ISOCountry.US
        )
        from time import perf_counter
        for_loop_time = perf_counter()
        for i in range(1000000):
            self.ISOCountry(self.ISOCountry.US.full_name.lower())

        for_loop_time = perf_counter() - for_loop_time
        print('for loop time: {}'.format(for_loop_time))
