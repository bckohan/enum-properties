from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('django_enum.tests.app1.urls'))
]
