from pathlib import Path

from bs4 import BeautifulSoup as Soup
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import Client, TestCase
from django.urls import reverse
from enum_properties.django import TextChoices
from enum_properties import p
from enum_properties.tests.django.app1.enums import (
    BigIntEnum,
    BigPosIntEnum,
    Constants,
    IntEnum,
    PosIntEnum,
    PrecedenceTest,
    SmallIntEnum,
    SmallPosIntEnum,
    TextEnum,
)
from enum_properties.tests.django.app1.models import EnumTester

APP1_DIR = Path(__file__).parent / 'app1'  # this dir does not exist and must be cleaned up


class TestDjangoEnums(TestCase):

    def setUp(self):
        pass

    def test_properties_and_symmetry(self):
        self.assertEqual(Constants.PI.symbol, 'π')
        self.assertEqual(Constants.e.symbol, 'e')
        self.assertEqual(Constants.GOLDEN_RATIO.symbol, 'φ')

        # test symmetry
        self.assertEqual(Constants.PI, Constants('π'))
        self.assertEqual(Constants.e, Constants('e'))
        self.assertEqual(Constants.GOLDEN_RATIO, Constants('φ'))

        self.assertEqual(Constants.PI, Constants('PI'))
        self.assertEqual(Constants.e, Constants('e'))
        self.assertEqual(Constants.GOLDEN_RATIO, Constants('GOLDEN_RATIO'))

        self.assertEqual(Constants.PI, Constants('Pi'))
        self.assertEqual(Constants.e, Constants("Euler's Number"))
        self.assertEqual(Constants.GOLDEN_RATIO, Constants('Golden Ratio'))

        self.assertEqual(TextEnum.VALUE1.version, 0)
        self.assertEqual(TextEnum.VALUE2.version, 1)
        self.assertEqual(TextEnum.VALUE3.version, 2)
        self.assertEqual(TextEnum.DEFAULT.version, 3)

        self.assertEqual(TextEnum.VALUE1.help, 'Some help text about value1.')
        self.assertEqual(TextEnum.VALUE2.help, 'Some help text about value2.')
        self.assertEqual(TextEnum.VALUE3.help, 'Some help text about value3.')
        self.assertEqual(TextEnum.DEFAULT.help, 'Some help text about default.')

        self.assertEqual(TextEnum.VALUE1, TextEnum('VALUE1'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('VALUE2'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('VALUE3'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('DEFAULT'))

        self.assertEqual(TextEnum.VALUE1, TextEnum('Value1'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('Value2'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('Value3'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('Default'))

        # test asymmetry
        self.assertRaises(ValueError, TextEnum, 0)
        self.assertRaises(ValueError, TextEnum, 1)
        self.assertRaises(ValueError, TextEnum, 2)
        self.assertRaises(ValueError, TextEnum, 3)

        # test asymmetry
        self.assertRaises(ValueError, TextEnum, 'Some help text about value1.')
        self.assertRaises(ValueError, TextEnum, 'Some help text about value2.')
        self.assertRaises(ValueError, TextEnum, 'Some help text about value3.')
        self.assertRaises(ValueError, TextEnum, 'Some help text about default.')

        # test basic case insensitive iterable symmetry
        self.assertEqual(TextEnum.VALUE1, TextEnum('val1'))
        self.assertEqual(TextEnum.VALUE1, TextEnum('v1'))
        self.assertEqual(TextEnum.VALUE1, TextEnum('v one'))
        self.assertEqual(TextEnum.VALUE1, TextEnum('VaL1'))
        self.assertEqual(TextEnum.VALUE1, TextEnum('V1'))
        self.assertEqual(TextEnum.VALUE1, TextEnum('v ONE'))

        self.assertEqual(TextEnum.VALUE2, TextEnum('val22'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('v2'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('v two'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('VaL22'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('V2'))
        self.assertEqual(TextEnum.VALUE2, TextEnum('v TWo'))

        self.assertEqual(TextEnum.VALUE3, TextEnum('val333'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('v3'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('v three'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('VaL333'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('V333'))
        self.assertEqual(TextEnum.VALUE3, TextEnum('v THRee'))

        self.assertEqual(TextEnum.DEFAULT, TextEnum('default'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('DeFaULT'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('DEfacTO'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('defacto'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('NONE'))
        self.assertEqual(TextEnum.DEFAULT, TextEnum('none'))

    def test_value_type_coercion(self):
        """test basic value coercion from str"""
        self.assertEqual(Constants.PI, Constants('3.14159265358979323846264338327950288'))
        self.assertEqual(Constants.e, Constants('2.71828'))
        self.assertEqual(Constants.GOLDEN_RATIO, Constants('1.61803398874989484820458683436563811'))

        self.assertEqual(SmallPosIntEnum.VAL1, SmallPosIntEnum('0'))
        self.assertEqual(SmallPosIntEnum.VAL2, SmallPosIntEnum('2'))
        self.assertEqual(SmallPosIntEnum.VAL3, SmallPosIntEnum('32767'))

        self.assertEqual(SmallIntEnum.VALn1, SmallIntEnum('-32768'))
        self.assertEqual(SmallIntEnum.VAL0, SmallIntEnum('0'))
        self.assertEqual(SmallIntEnum.VAL1, SmallIntEnum('1'))
        self.assertEqual(SmallIntEnum.VAL2, SmallIntEnum('2'))
        self.assertEqual(SmallIntEnum.VAL3, SmallIntEnum('32767'))

        self.assertEqual(IntEnum.VALn1, IntEnum('-2147483648'))
        self.assertEqual(IntEnum.VAL0, IntEnum('0'))
        self.assertEqual(IntEnum.VAL1, IntEnum('1'))
        self.assertEqual(IntEnum.VAL2, IntEnum('2'))
        self.assertEqual(IntEnum.VAL3, IntEnum('2147483647'))

        self.assertEqual(PosIntEnum.VAL0, PosIntEnum('0'))
        self.assertEqual(PosIntEnum.VAL1, PosIntEnum('1'))
        self.assertEqual(PosIntEnum.VAL2, PosIntEnum('2'))
        self.assertEqual(PosIntEnum.VAL3, PosIntEnum('2147483647'))

        self.assertEqual(BigPosIntEnum.VAL0, BigPosIntEnum('0'))
        self.assertEqual(BigPosIntEnum.VAL1, BigPosIntEnum('1'))
        self.assertEqual(BigPosIntEnum.VAL2, BigPosIntEnum('2'))
        self.assertEqual(BigPosIntEnum.VAL3, BigPosIntEnum('2147483648'))

        self.assertEqual(BigIntEnum.VAL0, BigIntEnum('-2147483649'))
        self.assertEqual(BigIntEnum.VAL1, BigIntEnum('1'))
        self.assertEqual(BigIntEnum.VAL2, BigIntEnum('2'))
        self.assertEqual(BigIntEnum.VAL3, BigIntEnum('2147483648'))

    def test_symmetric_type_coercion(self):
        """test that symmetric properties have types coerced"""
        self.assertEqual(BigIntEnum.VAL0, BigIntEnum(BigPosIntEnum.VAL0))
        self.assertEqual(BigIntEnum.VAL1, BigIntEnum(BigPosIntEnum.VAL1))
        self.assertEqual(BigIntEnum.VAL2, BigIntEnum(BigPosIntEnum.VAL2))
        self.assertEqual(BigIntEnum.VAL3, BigIntEnum(BigPosIntEnum.VAL3))

        self.assertEqual(BigIntEnum.VAL0, BigIntEnum(0))
        self.assertEqual(BigIntEnum.VAL0, BigIntEnum('0'))

    def test_precedence(self):
        """
        test that symmetric properties with non-hashable iterable values treat each iterable as a separate
        symmetric value
        """
        self.assertEqual(PrecedenceTest.P1, PrecedenceTest(0))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest(1))
        self.assertEqual(PrecedenceTest.P3, PrecedenceTest(2))
        self.assertEqual(PrecedenceTest.P4, PrecedenceTest(3))

        self.assertEqual(PrecedenceTest.P1, PrecedenceTest('Precedence 1'))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest('Precedence 2'))
        self.assertEqual(PrecedenceTest.P3, PrecedenceTest('Precedence 3'))
        self.assertEqual(PrecedenceTest.P4, PrecedenceTest('Precedence 4'))

        # type match takes precedence
        self.assertEqual(PrecedenceTest.P3, PrecedenceTest('1'))
        self.assertEqual(PrecedenceTest.P1, PrecedenceTest('0.4'))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest('0.3'))

        self.assertEqual(PrecedenceTest.P1, PrecedenceTest(0.1))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest(0.2))
        self.assertEqual(PrecedenceTest.P1, PrecedenceTest('0.1'))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest('0.2'))
        self.assertEqual(PrecedenceTest.P3, PrecedenceTest(0.3))
        self.assertEqual(PrecedenceTest.P4, PrecedenceTest(0.4))

        self.assertEqual(PrecedenceTest.P1, PrecedenceTest('First'))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest('Second'))
        self.assertEqual(PrecedenceTest.P3, PrecedenceTest('Third'))
        self.assertEqual(PrecedenceTest.P4, PrecedenceTest('Fourth'))

        # lower priority case insensitive match
        self.assertEqual(PrecedenceTest.P4, PrecedenceTest('FIRST'))
        self.assertEqual(PrecedenceTest.P3, PrecedenceTest('SECOND'))
        self.assertEqual(PrecedenceTest.P2, PrecedenceTest('THIRD'))
        self.assertEqual(PrecedenceTest.P1, PrecedenceTest('FOURTH'))

        self.assertEqual(PrecedenceTest.P4, PrecedenceTest(4))
        self.assertEqual(PrecedenceTest.P4, PrecedenceTest('4'))

    def test_unhashable_symmetry(self):
        """
        Tests that a value error is thrown when an unhashable type is used as a symmetrical property
        """
        with self.assertRaises(TypeError):
            class BadEnum(TextChoices, p('bad_prop', symmetric=True)):
                VAL1 = 'E1', 'E1 Label', 'Good prop'
                VAL2 = 'E2', 'E2 Label', {'hashable': False}

    def test_no_labels(self):
        """
        Tests that an enum without labels and with properties works as expected
        """
        class NoLabels(TextChoices, p('not_a_label', symmetric=True)):
            VAL1 = 'E1', 'E1 Label'
            VAL2 = 'E2', 'E2 Label'

        self.assertEqual(NoLabels.VAL1.label, 'VAL1'.title())
        self.assertEqual(NoLabels.VAL1.name, 'VAL1')
        self.assertEqual(NoLabels.VAL2.label, 'VAL2'.title())
        self.assertEqual(NoLabels.VAL2.name, 'VAL2')
        self.assertEqual(NoLabels.VAL1.not_a_label, 'E1 Label')
        self.assertEqual(NoLabels.VAL2.not_a_label, 'E2 Label')

        self.assertEqual(NoLabels.VAL1, NoLabels('E1 Label'))
        self.assertEqual(NoLabels.VAL2, NoLabels('E2 Label'))

        self.assertEqual(NoLabels.VAL1, NoLabels('VAL1'))
        self.assertEqual(NoLabels.VAL2, NoLabels('Val2'))

        self.assertEqual(NoLabels.VAL1, NoLabels('E1'))
        self.assertEqual(NoLabels.VAL2, NoLabels('E2'))

        class NoLabelsOrProps(TextChoices):
            VAL1 = 'E1'
            VAL2 = 'E2'

        self.assertEqual(NoLabelsOrProps.VAL1.label, 'VAL1'.title())
        self.assertEqual(NoLabelsOrProps.VAL1.name, 'VAL1')
        self.assertEqual(NoLabelsOrProps.VAL2.label, 'VAL2'.title())
        self.assertEqual(NoLabelsOrProps.VAL2.name, 'VAL2')

        self.assertEqual(NoLabelsOrProps.VAL1, NoLabelsOrProps('VAL1'))
        self.assertEqual(NoLabelsOrProps.VAL2, NoLabelsOrProps('Val2'))

        self.assertEqual(NoLabelsOrProps.VAL1, NoLabelsOrProps('E1'))
        self.assertEqual(NoLabelsOrProps.VAL2, NoLabelsOrProps('E2'))

    def test_base_fields(self):
        """
        Test that the Enum metaclass picks the correct database field type for each enum.
        """
        tester = EnumTester.objects.create()
        from django.db.models import (
            BigIntegerField,
            CharField,
            FloatField,
            IntegerField,
            PositiveBigIntegerField,
            PositiveIntegerField,
            PositiveSmallIntegerField,
            SmallIntegerField,
        )

        self.assertIsInstance(tester._meta.get_field('small_int'), SmallIntegerField)
        self.assertEqual(tester.small_int, tester._meta.get_field('small_int').default)
        self.assertEqual(tester.small_int, SmallIntEnum.VAL3)
        self.assertIsInstance(tester._meta.get_field('small_pos_int'), PositiveSmallIntegerField)
        self.assertIsNone(tester.small_pos_int)
        self.assertIsInstance(tester._meta.get_field('int'), IntegerField)
        self.assertIsNone(tester.int)

        self.assertIsInstance(tester._meta.get_field('pos_int'), PositiveIntegerField)
        self.assertEqual(tester.pos_int, tester._meta.get_field('pos_int').default)
        self.assertEqual(tester.pos_int, PosIntEnum.VAL3)

        self.assertIsInstance(tester._meta.get_field('big_int'), BigIntegerField)
        self.assertEqual(tester.big_int, tester._meta.get_field('big_int').default)
        self.assertEqual(tester.big_int, BigIntEnum.VAL0)

        self.assertIsInstance(tester._meta.get_field('big_pos_int'), PositiveBigIntegerField)
        self.assertIsNone(tester.big_pos_int)

        self.assertIsInstance(tester._meta.get_field('constant'), FloatField)
        self.assertIsNone(tester.constant)

        self.assertIsInstance(tester._meta.get_field('text'), CharField)
        self.assertEqual(tester._meta.get_field('text').max_length, 4)
        self.assertIsNone(tester.text)

    def test_saving(self):
        """
        Test that the Enum metaclass picks the correct database field type for each enum.
        """
        tester = EnumTester.objects.create(
            small_pos_int=SmallPosIntEnum.VAL2,
            small_int=SmallIntEnum.VAL0,
            pos_int=PosIntEnum.VAL1,
            int=IntEnum.VALn1,
            big_pos_int=BigPosIntEnum.VAL3,
            big_int=BigIntEnum.VAL2,
            constant=Constants.GOLDEN_RATIO,
            text=TextEnum.VALUE2
        )

        self.assertEqual(tester.small_pos_int, SmallPosIntEnum.VAL2)
        self.assertEqual(tester.small_int, SmallIntEnum.VAL0)
        self.assertEqual(tester.pos_int, PosIntEnum.VAL1)
        self.assertEqual(tester.int, IntEnum.VALn1)
        self.assertEqual(tester.big_pos_int, BigPosIntEnum.VAL3)
        self.assertEqual(tester.big_int, BigIntEnum.VAL2)
        self.assertEqual(tester.constant, Constants.GOLDEN_RATIO)
        self.assertEqual(tester.text, TextEnum.VALUE2)

        tester.small_pos_int = SmallPosIntEnum.VAL1
        tester.small_int = SmallIntEnum.VAL2
        tester.pos_int = PosIntEnum.VAL0
        tester.int = IntEnum.VAL1
        tester.big_pos_int = BigPosIntEnum.VAL2
        tester.big_int = BigIntEnum.VAL1
        tester.constant = Constants.PI
        tester.text = TextEnum.VALUE3

        tester.save()

        self.assertEqual(tester.small_pos_int, SmallPosIntEnum.VAL1)
        self.assertEqual(tester.small_int, SmallIntEnum.VAL2)
        self.assertEqual(tester.pos_int, PosIntEnum.VAL0)
        self.assertEqual(tester.int, IntEnum.VAL1)
        self.assertEqual(tester.big_pos_int, BigPosIntEnum.VAL2)
        self.assertEqual(tester.big_int, BigIntEnum.VAL1)
        self.assertEqual(tester.constant, Constants.PI)
        self.assertEqual(tester.text, TextEnum.VALUE3)

        tester.refresh_from_db()

        self.assertEqual(tester.small_pos_int, SmallPosIntEnum.VAL1)
        self.assertEqual(tester.small_int, SmallIntEnum.VAL2)
        self.assertEqual(tester.pos_int, PosIntEnum.VAL0)
        self.assertEqual(tester.int, IntEnum.VAL1)
        self.assertEqual(tester.big_pos_int, BigPosIntEnum.VAL2)
        self.assertEqual(tester.big_int, BigIntEnum.VAL1)
        self.assertEqual(tester.constant, Constants.PI)
        self.assertEqual(tester.text, TextEnum.VALUE3)

        tester.small_pos_int = '32767'
        tester.small_int = -32768
        tester.pos_int = 2147483647
        tester.int = -2147483648
        tester.big_pos_int = 2147483648
        tester.big_int = -2147483649
        tester.constant = '2.71828'
        tester.text = 'D'

        tester.save()
        tester.refresh_from_db()

        self.assertEqual(tester.small_pos_int, 32767)
        self.assertEqual(tester.small_int, -32768)
        self.assertEqual(tester.pos_int, 2147483647)
        self.assertEqual(tester.int, -2147483648)
        self.assertEqual(tester.big_pos_int, 2147483648)
        self.assertEqual(tester.big_int, -2147483649)
        self.assertEqual(tester.constant, 2.71828)
        self.assertEqual(tester.text, 'D')

        with transaction.atomic():
            tester.text = 'not valid'
            self.assertRaises(ValueError, tester.save)
        tester.refresh_from_db()

        with transaction.atomic():
            tester.text = type('WrongType')()
            self.assertRaises(ValueError, tester.save)
        tester.refresh_from_db()

        with transaction.atomic():
            tester.text = 1
            self.assertRaises(ValueError, tester.save)
        tester.refresh_from_db()

        # fields with choices are more permissive - choice check does not happen on basic save
        with transaction.atomic():
            tester.char_choice = 'not valid'
            tester.save()
            #self.assertRaises(ValidationError, tester.save)
        tester.refresh_from_db()

        with transaction.atomic():
            tester.char_choice = 5
            tester.save()
            #self.assertRaises(ValueError, tester.save)
        tester.refresh_from_db()

        with transaction.atomic():
            tester.int_choice = 5
            tester.save()
            #self.assertRaises(ValueError, tester.save)
        tester.refresh_from_db()
        #####################################################################################

        with transaction.atomic():
            tester.int_choice = 'a'
            self.assertRaises(ValueError, tester.save)
        tester.refresh_from_db()

        tester.text = None
        tester.save()
        self.assertEqual(tester.text, None)

    def test_serialization(self):
        tester = EnumTester.objects.create(
            small_pos_int=SmallPosIntEnum.VAL2,
            small_int=SmallIntEnum.VAL0,
            pos_int=PosIntEnum.VAL1,
            int=IntEnum.VALn1,
            big_pos_int=BigPosIntEnum.VAL3,
            big_int=BigIntEnum.VAL2,
            constant=Constants.GOLDEN_RATIO,
            text=TextEnum.VALUE2
        )

        serialized = serializers.serialize('json', EnumTester.objects.all())

        tester.delete()

        for mdl in serializers.deserialize('json', serialized):
            mdl.save()
            tester = mdl.object

        self.assertEqual(tester.small_pos_int, SmallPosIntEnum.VAL2)
        self.assertEqual(tester.small_int, SmallIntEnum.VAL0)
        self.assertEqual(tester.pos_int, PosIntEnum.VAL1)
        self.assertEqual(tester.int, IntEnum.VALn1)
        self.assertEqual(tester.big_pos_int, BigPosIntEnum.VAL3)
        self.assertEqual(tester.big_int, BigIntEnum.VAL2)
        self.assertEqual(tester.constant, Constants.GOLDEN_RATIO)
        self.assertEqual(tester.text, TextEnum.VALUE2)

    def test_validate(self):
        tester = EnumTester.objects.create()
        self.assertRaises(ValidationError, tester._meta.get_field('small_pos_int').validate, 666, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('small_int').validate, 666, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('pos_int').validate, 666, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('int').validate, 666, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('big_pos_int').validate, 666, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('big_int').validate, 666, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('constant').validate, 66.6, tester)
        self.assertRaises(ValidationError, tester._meta.get_field('text').validate, '666', tester)

        self.assertRaises(ValidationError, tester._meta.get_field('small_pos_int').validate, 'anna', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('small_int').validate, 'maria', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('pos_int').validate, 'montes', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('int').validate, '3<', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('big_pos_int').validate, 'itwb', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('big_int').validate, 'walwchh', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('constant').validate, 'xx.x', tester)
        self.assertRaises(ValidationError, tester._meta.get_field('text').validate, '666', tester)

        self.assertRaises(ValidationError, tester._meta.get_field('small_int').validate, None, tester)

        self.assertTrue(tester._meta.get_field('small_pos_int').validate(0, tester) is None)
        self.assertTrue(tester._meta.get_field('small_int').validate('Value -32768', tester) is None)
        self.assertTrue(tester._meta.get_field('pos_int').validate(2147483647, tester) is None)
        self.assertTrue(tester._meta.get_field('int').validate('VALn1', tester) is None)
        self.assertTrue(tester._meta.get_field('big_pos_int').validate('Value 2147483647', tester) is None)
        self.assertTrue(tester._meta.get_field('big_int').validate(BigPosIntEnum.VAL2, tester) is None)
        self.assertTrue(tester._meta.get_field('constant').validate('φ', tester) is None)
        self.assertTrue(tester._meta.get_field('text').validate('default', tester) is None)


    def test_clean(self):

        tester = EnumTester(
            small_pos_int=666,
            small_int=666,
            pos_int=666,
            int=666,
            big_pos_int=666,
            big_int=666,
            constant=66.6,
            text='666',
        )
        try:
            tester.full_clean()
            self.assertTrue(False, "full_clean should have thrown a ValidationError")  # pragma: no cover
        except ValidationError as ve:
            self.assertTrue('small_pos_int' in ve.message_dict)
            self.assertTrue('small_int' in ve.message_dict)
            self.assertTrue('pos_int' in ve.message_dict)
            self.assertTrue('int' in ve.message_dict)
            self.assertTrue('big_pos_int' in ve.message_dict)
            self.assertTrue('big_int' in ve.message_dict)
            self.assertTrue('constant' in ve.message_dict)
            self.assertTrue('text' in ve.message_dict)


class TestEnumQueries(TestCase):

    def setUp(self):
        EnumTester.objects.all().delete()

    def test_query(self):
        EnumTester.objects.create(
            small_pos_int=SmallPosIntEnum.VAL2,
            small_int=SmallIntEnum.VAL0,
            pos_int=PosIntEnum.VAL1,
            int=IntEnum.VALn1,
            big_pos_int=BigPosIntEnum.VAL3,
            big_int=BigIntEnum.VAL2,
            constant=Constants.GOLDEN_RATIO,
            text=TextEnum.VALUE2
        )
        EnumTester.objects.create(
            small_pos_int=SmallPosIntEnum.VAL2,
            small_int=SmallIntEnum.VAL0,
            pos_int=PosIntEnum.VAL1,
            int=IntEnum.VALn1,
            big_pos_int=BigPosIntEnum.VAL3,
            big_int=BigIntEnum.VAL2,
            constant=Constants.GOLDEN_RATIO,
            text=TextEnum.VALUE2
        )

        EnumTester.objects.create()

        self.assertEqual(EnumTester.objects.filter(small_pos_int=SmallPosIntEnum.VAL2).count(), 2)
        self.assertEqual(EnumTester.objects.filter(small_pos_int=SmallPosIntEnum.VAL2.value).count(), 2)
        self.assertEqual(EnumTester.objects.filter(small_pos_int='Value 2').count(), 2)
        self.assertEqual(EnumTester.objects.filter(small_pos_int=SmallPosIntEnum.VAL2.name).count(), 2)

        self.assertEqual(EnumTester.objects.filter(big_pos_int=BigPosIntEnum.VAL3).count(), 2)
        self.assertEqual(EnumTester.objects.filter(big_pos_int=BigPosIntEnum.VAL3.label).count(), 2)
        self.assertEqual(EnumTester.objects.filter(big_pos_int=None).count(), 1)

        self.assertEqual(EnumTester.objects.filter(constant=Constants.GOLDEN_RATIO).count(), 2)
        self.assertEqual(EnumTester.objects.filter(constant=Constants.GOLDEN_RATIO.name).count(), 2)
        self.assertEqual(EnumTester.objects.filter(constant=Constants.GOLDEN_RATIO.value).count(), 2)
        self.assertEqual(EnumTester.objects.filter(constant__isnull=True).count(), 1)

        # test symmetry
        self.assertEqual(EnumTester.objects.filter(constant=Constants.GOLDEN_RATIO.symbol).count(), 2)
        self.assertEqual(EnumTester.objects.filter(constant='φ').count(), 2)

        self.assertEqual(EnumTester.objects.filter(text=TextEnum.VALUE2).count(), 2)
        self.assertEqual(len(TextEnum.VALUE2.aliases), 3)
        for alias in TextEnum.VALUE2.aliases:
            self.assertEqual(EnumTester.objects.filter(text=alias).count(), 2)

        self.assertRaises(ValueError, EnumTester.objects.filter, int_field='a')
        self.assertRaises(ValueError, EnumTester.objects.filter, float_field='a')
        self.assertRaises(ValueError, EnumTester.objects.filter, constant='p')
        self.assertRaises(ValueError, EnumTester.objects.filter, big_pos_int='p')
        self.assertRaises(ValueError, EnumTester.objects.filter, big_pos_int=type('WrongType')())


class TestRequests(TestCase):

    def setUp(self):
        EnumTester.objects.all().delete()

    def test_post(self):
        c = Client()
        response = c.post(
            reverse('enum_properties_tests_django_app1:enum-add'),
            {
                'small_pos_int': SmallPosIntEnum.VAL2,
                'small_int': SmallIntEnum.VAL0,
                'pos_int': PosIntEnum.VAL1,
                'int': IntEnum.VALn1,
                'big_pos_int': BigPosIntEnum.VAL3,
                'big_int': BigIntEnum.VAL2,
                'constant': Constants.GOLDEN_RATIO,
                'text': TextEnum.VALUE2
            },
            follow=True
        )
        soup = Soup(response.content, features='html.parser')
        added = soup.find_all('div', class_='enum')[-1]
        self.assertEqual(
            SmallPosIntEnum(added.find(class_="small_pos_int").find("span", class_="value").text),
            SmallPosIntEnum.VAL2
        )
        self.assertEqual(
            SmallIntEnum(added.find(class_="small_int").find("span", class_="value").text),
            SmallIntEnum.VAL0
        )
        self.assertEqual(
            PosIntEnum(added.find(class_="pos_int").find("span", class_="value").text),
            PosIntEnum.VAL1
        )
        self.assertEqual(
            IntEnum(added.find(class_="int").find("span", class_="value").text),
            IntEnum.VALn1
        )
        self.assertEqual(
            BigPosIntEnum(added.find(class_="big_pos_int").find("span", class_="value").text),
            BigPosIntEnum.VAL3
        )
        self.assertEqual(
            BigIntEnum(added.find(class_="big_int").find("span", class_="value").text),
            BigIntEnum.VAL2
        )
        self.assertEqual(
            Constants(added.find(class_="constant").find("span", class_="value").text),
            Constants.GOLDEN_RATIO
        )
        self.assertEqual(
            TextEnum(added.find(class_="text").find("span", class_="value").text),
            TextEnum.VALUE2
        )

    def test_form(self):
        c = Client()
        response = c.get(reverse('enum_properties_tests_django_app1:enum-add'))
        soup = Soup(response.content, features='html.parser')

        for field in [
            'small_pos_int',
            'small_int',
            'pos_int',
            'int',
            'big_pos_int',
            'big_int',
            'constant',
            'text',
        ]:
            field = EnumTester._meta.get_field(field)
            expected = dict(zip(field.enum.values, field.enum.labels))  # value -> label
            null_opt = False
            for child in soup.find('select', id=f'id_{field.name}').find_all('option'):
                if child.value is None and child.text.count('-') >= 2:
                    self.assertTrue(field.blank or field.null)
                    null_opt = True
                    continue

                try:
                    self.assertTrue(str(expected[field.enum(child['value']).value]), child.text)
                    del expected[field.enum(child['value'])]
                except KeyError:  # pragma: no cover
                    self.fail(f'{field.name} did not expect option {child["value"]}: {child.text}.')

            self.assertEqual(len(expected), 0)

            if not field.null and not field.blank:
                self.assertFalse(null_opt, "An unexpected null option is present")  # pragma: no cover


class TestNonDjangoEnums(TestCase):

    def setUp(self):
        EnumTester.objects.all().delete()

    def test_properties_and_symmetry(self):
        from enum import Enum, auto
        from enum_properties import EnumProperties, SymmetricMixin

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
        from enum import Enum
        from enum_properties import EnumProperties

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
        from enum import Enum
        from enum_properties import EnumProperties, SymmetricMixin

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
        from enum import Enum
        from enum_properties import EnumProperties, SymmetricMixin

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
        from enum import Enum, auto
        from enum_properties import EnumProperties, SymmetricMixin

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
        from enum import Enum
        from enum_properties import EnumProperties, SymmetricMixin

        class Color(
            SymmetricMixin,
            Enum,
            p('spanish'),
            p('rgb', symmetric=True),
            p('hex', symmetric=True, case_sensitive=False),
            metaclass=EnumProperties
        ):

            _ignore_ = ['BLACK']

            RED = 1, 'Roja', (1, 0, 0), 'ff0000'
            GREEN = 2, 'Verde', (0, 1, 0), '00ff00'
            BLUE = 3, 'Azul', (0, 0, 1), '0000ff'
            BLACK = 4, 'Negra', (1, 1, 1), 'ffffff'

        self.assertFalse(hasattr(Color, 'BLACK'))
        self.assertRaises(ValueError, Color, 4)
        self.assertRaises(ValueError, Color, (1, 1, 1))
        self.assertRaises(ValueError, Color, 'ffffff')
