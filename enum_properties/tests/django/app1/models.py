import enum_properties
if enum_properties.DJANGO_SUPPORTED:  # pragma: no cover
    from django.db import models
    from django.urls import reverse
    from enum_properties.django import EnumField
    from enum_properties.tests.django.app1.enums import *


    class EnumTester(models.Model):

        small_pos_int = EnumField(SmallPosIntEnum, null=True, default=None, db_index=True, blank=True)
        small_int = EnumField(SmallIntEnum, null=False, default=SmallIntEnum.VAL3, db_index=True, blank=True)

        pos_int = EnumField(PosIntEnum, default=PosIntEnum.VAL3, db_index=True, blank=True)
        int = EnumField(IntEnum, null=True, db_index=True, blank=True)

        big_pos_int = EnumField(BigPosIntEnum, null=True, default=None, db_index=True, blank=True)
        big_int = EnumField(BigIntEnum, default=BigIntEnum.VAL0, db_index=True, blank=True)

        constant = EnumField(Constants, null=True, default=None, db_index=True, blank=True)

        text = EnumField(TextEnum, null=True, default=None, db_index=True, blank=True)

        # basic choice fields - used to compare behavior
        int_choice = models.IntegerField(
            default=1,
            null=False,
            blank=True,
            choices=((1, 'One'), (2, 'Two'), (3, 'Three'))
        )

        char_choice = models.CharField(
            max_length=1,
            default='A',
            null=False,
            blank=True,
            choices=(('A', 'First'), ('B', 'Second'), ('C', 'Third'))
        )

        int_field = models.IntegerField(
            default=1,
            null=False,
            blank=True
        )

        float_field = models.FloatField(
            default=1.5,
            null=False,
            blank=True
        )

        char_field = models.CharField(
            max_length=1,
            default='A',
            null=False,
            blank=True
        )
        ################################################

        def get_absolute_url(self):
            return reverse('enum_properties_tests_django_app1:enum-detail', kwargs={'pk': self.pk})

        class Meta:
            ordering = ('id',)
