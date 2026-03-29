from django.apps import AppConfig


class TestApp2Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tests.testapp2"
    label = "testapp2"
