import enum
import sys
from enum import auto
from unittest import TestCase
import warnings

from enum_properties import (
    EnumProperties,
    p,
    s,
)


def transparent(func):
    return func  # pragma: no cover


nonmember, member = (
    (enum.nonmember, enum.member)
    if sys.version_info >= (3, 11)
    else (transparent, transparent)
)


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

        class TestEnum(EnumProperties, s("label")):
            VALUE1 = Type1, "value1"
            VALUE2 = Type2, "value2"
            VALUE3 = Type3, "value3"

        self.assertEqual(
            [en for en in TestEnum], [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )

        self.assertEqual(
            [en.label for en in TestEnum],
            [TestEnum.VALUE1.label, TestEnum.VALUE2.label, TestEnum.VALUE3.label],
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum("value1"), TestEnum("value2"), TestEnum("value3")],
        )
        self.assertEqual(
            [en for en in TestEnum], [TestEnum(Type1), TestEnum(Type2), TestEnum(Type3)]
        )
        self.assertEqual([en.value for en in TestEnum], [Type1, Type2, Type3])

    def test_nested_classes(self):
        class TestEnum(EnumProperties, s("label")):
            VALUE1 = auto(), "value1"
            VALUE2 = auto(), "value2"
            VALUE3 = auto(), "value3"

            def function(self):
                return self.value

            @classmethod
            def default(cls):
                return cls.VALUE1

            @staticmethod
            def static_property():
                return "static_prop"

            @nonmember
            class NestedClass:
                @property
                def prop(self):
                    return "nested"

        self.assertEqual(TestEnum.VALUE1.function(), TestEnum.VALUE1.value)
        self.assertEqual(TestEnum.VALUE2.function(), TestEnum.VALUE2.value)
        self.assertEqual(TestEnum.VALUE3.function(), TestEnum.VALUE3.value)
        self.assertEqual(TestEnum.default(), TestEnum.VALUE1)
        self.assertEqual(TestEnum.static_property(), "static_prop")
        self.assertEqual(TestEnum.NestedClass().prop, "nested")
        self.assertEqual(
            [en for en in TestEnum], [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )
        self.assertEqual(
            [en.label for en in TestEnum],
            [TestEnum.VALUE1.label, TestEnum.VALUE2.label, TestEnum.VALUE3.label],
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum("value1"), TestEnum("value2"), TestEnum("value3")],
        )

    def test_nested_classes_as_values(self):
        class TestEnum(EnumProperties, s("label")):
            @nonmember
            class Type1:
                pass

            @nonmember
            class Type2:
                pass

            @nonmember
            class Type3:
                pass

            VALUE1 = member(Type1), "value1"
            VALUE2 = member(Type2), "value2"
            VALUE3 = member(Type3), "value3"

        self.assertEqual(
            [en for en in TestEnum], [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )

        self.assertEqual(
            [en.label for en in TestEnum],
            [TestEnum.VALUE1.label, TestEnum.VALUE2.label, TestEnum.VALUE3.label],
        )
        self.assertEqual(
            [en for en in TestEnum],
            [TestEnum("value1"), TestEnum("value2"), TestEnum("value3")],
        )
        self.assertEqual(
            [en for en in TestEnum],
            [
                TestEnum(TestEnum.Type1),
                TestEnum(TestEnum.Type2),
                TestEnum(TestEnum.Type3),
            ],
        )
        self.assertEqual(
            [en.value for en in TestEnum],
            [TestEnum.Type1, TestEnum.Type2, TestEnum.Type3],
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
            [en for en in TestEnum], [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3]
        )
        self.assertEqual(
            [en for en in TestEnum],
            [
                TestEnum(TestEnum.Type1),
                TestEnum(TestEnum.Type2),
                TestEnum(TestEnum.Type3),
            ],
        )
        self.assertEqual(
            [en.value for en in TestEnum],
            [TestEnum.Type1, TestEnum.Type2, TestEnum.Type3],
        )

    def test_example(self):
        class MyEnum(EnumProperties, p("label")):
            @nonmember
            class Type1:
                pass

            @nonmember
            class Type2:
                pass

            @nonmember
            class Type3:
                pass

            VALUE1 = member(Type1), "label1"
            VALUE2 = member(Type2), "label2"
            VALUE3 = member(Type3), "label3"

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
            class MyEnum(EnumProperties, p("label")):
                @nonmember
                class Type1:
                    pass

                @nonmember
                class Type2:
                    pass

                @nonmember
                class Type3:
                    pass

                VALUE1 = member(Type1), "label1"
                VALUE2 = member(Type2), "label2"
                VALUE3 = member(Type3), "label3"
                VALUE4 = nonmember((Type3, "label4"))

            # nested classes are usable like normal
            self.assertEqual(MyEnum.Type1, MyEnum.VALUE1.value)
            self.assertEqual(MyEnum.Type2, MyEnum.VALUE2.value)
            self.assertEqual(MyEnum.Type3, MyEnum.VALUE3.value)
            self.assertEqual(len(MyEnum), 3)
            self.assertEqual(MyEnum.VALUE4, (MyEnum.Type3, "label4"))
            self.assertTrue(MyEnum.Type1().__class__ is MyEnum.Type1)
            self.assertTrue(MyEnum.Type2().__class__ is MyEnum.Type2)
            self.assertTrue(MyEnum.Type3().__class__ is MyEnum.Type3)

        def test_member_decorator(self):
            with self.assertRaises(ValueError):

                class MyEnum(EnumProperties, p("label")):
                    @member
                    class Type1:
                        pass

                    @member
                    class Type2:
                        pass

                    @member
                    class Type3:
                        pass

                    VALUE1 = Type1, "label1"
                    VALUE2 = Type2, "label2"
                    VALUE3 = Type3, "label3"

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

            VALUE1 = Type1, "label1"
            VALUE2 = Type2, "label2"
            VALUE3 = Type3, "label3"

        self.assertEqual(MyEnum.Type1.value, MyEnum.VALUE1.value[0])
        self.assertEqual(MyEnum.Type2.value, MyEnum.VALUE2.value[0])
        self.assertEqual(MyEnum.Type3.value, MyEnum.VALUE3.value[0])
        self.assertEqual(len(MyEnum), 6)
        self.assertTrue(MyEnum.Type1.value().__class__ is MyEnum.Type1.value)
        self.assertTrue(MyEnum.Type2.value().__class__ is MyEnum.Type2.value)
        self.assertTrue(MyEnum.Type3.value().__class__ is MyEnum.Type3.value)

    if sys.version_info < (3, 13):  # pragma: no cover

        def test_unmarked_nested_classes(self):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)

                class TestEnum(EnumProperties, s("label")):
                    VALUE1 = auto(), "value1"
                    VALUE2 = auto(), "value2"
                    VALUE3 = auto(), "value3"

                    class NestedClass:
                        @property
                        def prop(self):
                            return "nested"

                self.assertEqual(TestEnum.NestedClass().prop, "nested")
                self.assertEqual(
                    [en for en in TestEnum],
                    [TestEnum.VALUE1, TestEnum.VALUE2, TestEnum.VALUE3],
                )
                self.assertEqual(
                    [en.label for en in TestEnum],
                    [
                        TestEnum.VALUE1.label,
                        TestEnum.VALUE2.label,
                        TestEnum.VALUE3.label,
                    ],
                )
                self.assertEqual(
                    [en for en in TestEnum],
                    [TestEnum("value1"), TestEnum("value2"), TestEnum("value3")],
                )
