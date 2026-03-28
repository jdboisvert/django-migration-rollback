INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "migration_rollback",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
