from unittest import TestCase
from enum import Enum, auto
from enum_properties import EnumProperties, SymmetricMixin, p


class TestNonDjangoEnums(TestCase):

    def test_properties_and_symmetry(self):

        class Color(
            SymmetricMixin,
            int,
            Enum,
            p('spanish'),
            p('rgb', symmetric=True),
            p('hex', symmetric=True, case_sensitive=False),
            metaclass=EnumProperties
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

    def test_properties_no_symmetry(self):
        """
        Tests that absense of SymmetricMixin works but w/o symmetrical
        properties
        """

        class Color(
            Enum,
            p('spanish'),
            p('rgb', symmetric=True),
            p('hex', symmetric=True, case_sensitive=False),
            metaclass=EnumProperties
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
            SymmetricMixin,
            Enum,
            p('prop1', symmetric=True),
            p('prop2', symmetric=True),
            metaclass=EnumProperties
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
            SymmetricMixin,
            Enum,
            p('prop1', symmetric=True),
            p('prop2', symmetric=True),
            metaclass=EnumProperties
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

        class ColorAuto(Enum, metaclass=EnumProperties):
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
            SymmetricMixin,
            Enum,
            p('spanish'),
            p('rgb', symmetric=True),
            p('hex', symmetric=True, case_sensitive=False),
            metaclass=EnumProperties
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
            SymmetricMixin,
            Enum,
            p('spanish'),
            p('rgb', symmetric=True),
            p('hex', symmetric=True, case_sensitive=False),
            metaclass=EnumProperties
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
            SymmetricMixin,
            Enum,
            p('spanish'),
            p('rgb', symmetric=True),
            p('hex', symmetric=True, case_sensitive=False),
            metaclass=EnumProperties
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

        class Color(
            SymmetricMixin,
            Enum,
            metaclass=EnumProperties
        ):
            RED = 1, 0, 0
            GREEN = 0, 1, 0
            BLUE = 0, 0, 1

        self.assertEqual(Color.RED.value, (1, 0, 0))
        self.assertEqual(Color.GREEN.value, (0, 1, 0))
        self.assertEqual(Color.BLUE.value, (0, 0, 1))

    def test_not_enough_props(self):

        with self.assertRaises(AssertionError):
            class Color(
                SymmetricMixin,
                Enum,
                p('prop1'),
                p('prop2'),
                metaclass=EnumProperties
            ):
                RED = 1, 'p1.1', 'p2.1'
                GREEN = 2, 'p1.2', 'p2.2'
                BLUE = 3, 'p1.3'
