from django.urls import path
from enum_properties.tests.django.app1.models import EnumTester
from enum_properties.tests.django.app1.views import (
    EnumTesterCreateView,
    EnumTesterDeleteView,
    EnumTesterDetailView,
    EnumTesterListView,
    EnumTesterUpdateView,
)
from django_filters.views import FilterView

app_name = 'enum_properties_tests_django_app1'

urlpatterns = [
    path('enum/<int:pk>', EnumTesterDetailView.as_view(), name='enum-detail'),
    path('enum/list/', EnumTesterListView.as_view(), name='enum-list'),
    path(
        'enum/filter/',
        FilterView.as_view(
            model=EnumTester,
            filterset_fields='__all__',
            template_name='enum_properties_tests_django_app1/enumtester_list.html'
        ),
        name='enum-filter'
    ),
    path('enum/add/', EnumTesterCreateView.as_view(), name='enum-add'),
    path('enum/<int:pk>/', EnumTesterUpdateView.as_view(), name='enum-update'),
    path('enum/<int:pk>/delete/', EnumTesterDeleteView.as_view(), name='enum-delete'),
]
