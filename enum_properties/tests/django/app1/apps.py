import enum_properties
if enum_properties.DJANGO_SUPPORTED:  # pragma: no cover
    from django.apps import AppConfig


    class App1Config(AppConfig):
        name = 'enum_properties.tests.django.app1'
        label = name.replace('.', '_')

        def ready(self):
            pass
