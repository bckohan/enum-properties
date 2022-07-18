# pylint: skip-file

from enum import Enum, auto
from unittest import TestCase

from enum_properties import (
    EnumProperties,
    EnumPropertiesMeta,
    SymmetricMixin,
    p,
    s,
)


class TestEnums(TestCase):

    def test_p(self):
        from enum_properties.meta import _Prop

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
            SymmetricMixin,
            int,
            Enum,
            p('spanish'),
            s('rgb'),
            s('hex', case_fold=True),
            metaclass=EnumPropertiesMeta
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
            [prop for prop in Color.properties if prop.symmetric],
            ['rgb', 'hex']
        )

        self.assertEqual(
            Color.properties,
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

        with self.assertRaises(AssertionError):
            class Color(
                EnumProperties,
                p('prop1'),
                p('prop2')
            ):
                RED = 1, 'p1.1', 'p2.1'
                GREEN = 2, 'p1.2', 'p2.2'
                BLUE = 3, 'p1.3'

        with self.assertRaises(AssertionError):
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
            s('hex', case_fold=True)
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

        class Color(EnumProperties, s('rgb'), s('hex')):

            RED = auto(), (1, 0, 0), 'ff0000'
            GREEN = auto(), (0, 1, 0), '00ff00'
            BLUE = auto(), (0, 0, 1), '0000ff'

        self.assertEqual(Color.RED, Color((1, 0, 0)))
        self.assertEqual(Color.GREEN, Color((0, 1, 0)))
        self.assertEqual(Color.BLUE, Color((0, 0, 1)))

        self.assertEqual(Color.RED, Color('ff0000'))
        self.assertEqual(Color.GREEN, Color('00ff00'))
        self.assertEqual(Color.BLUE, Color('0000ff'))
