from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from enum_properties.tests.django.app1.models import EnumTester


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


class EnumTesterDeleteView(DeleteView):
    model = EnumTester
    success_url = reverse_lazy('enum_properties_tests_django_app1:enum-list')
