INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "migration_rollback",
    "tests.testapp",
    "tests.testapp2",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
