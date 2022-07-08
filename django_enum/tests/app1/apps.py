from django.apps import AppConfig


class App1Config(AppConfig):
    name = 'django_enum.tests.app1'
    label = name.replace('.', '_')
