import pytest
from django.core.management import call_command


@pytest.fixture
def remigrate_testapp():
    """Re-apply all testapp migrations after the test completes.

    Used by integration tests that roll back migrations against a real DB
    (transaction=True) to ensure the DB is in a clean state for subsequent tests.
    """
    yield
    call_command("migrate", "testapp", verbosity=0)
