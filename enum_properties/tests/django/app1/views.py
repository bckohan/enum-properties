import enum_properties
if enum_properties.DJANGO_SUPPORTED:  # pragma: no cover
    from django.urls import reverse_lazy
    from django.views.generic import DetailView, ListView
    from django.forms import ModelForm
    from django.views.generic.edit import CreateView, DeleteView, UpdateView
    from enum_properties.django import (
        FilterSet as EnumFilterSet,
        EnumChoiceField
    )

    from django_filters.views import FilterView
    from enum_properties.tests.django.app1.models import EnumTester
    from enum_properties.tests.django.app1.enums import (
        TextEnum,
        Constants,
        SmallPosIntEnum,
        SmallIntEnum,
        IntEnum,
        PosIntEnum,
        BigPosIntEnum,
        BigIntEnum
    )

    class EnumTesterDetailView(DetailView):
        model = EnumTester


    class EnumTesterListView(ListView):
        model = EnumTester


    class EnumTesterCreateView(CreateView):
        model = EnumTester
        fields = '__all__'


    class EnumTesterUpdateView(UpdateView):
        model = EnumTester
        fields = '__all__'


    class EnumTesterFormView(UpdateView):

        class EnumTesterForm(ModelForm):
            small_pos_int = EnumChoiceField(SmallPosIntEnum)
            small_int = EnumChoiceField(SmallIntEnum)
            pos_int = EnumChoiceField(PosIntEnum)
            int = EnumChoiceField(IntEnum)
            big_pos_int = EnumChoiceField(BigPosIntEnum)
            big_int = EnumChoiceField(BigIntEnum)
            constant = EnumChoiceField(Constants)
            text = EnumChoiceField(TextEnum)

            class Meta:
                model = EnumTester
                fields = '__all__'

        form_class = EnumTesterForm
        model = EnumTester


    class EnumTesterDeleteView(DeleteView):
        model = EnumTester
        success_url = reverse_lazy(
            'enum_properties_tests_django_app1:enum-list'
        )


    class EnumTesterFilterViewSet(FilterView):

        class EnumTesterFilter(EnumFilterSet):
            class Meta:
                model = EnumTester
                fields = '__all__'

        filterset_class = EnumTesterFilter
        model = EnumTester
        template_name = (
            'enum_properties_tests_django_app1/enumtester_list.html'
        )
