import enum_properties
if enum_properties.DJANGO_SUPPORTED:  # pragma: no cover
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('app1/', include('enum_properties.tests.django.app1.urls'))
    ]
