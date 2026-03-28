"""
Integration tests that run the management commands against a real SQLite test DB
and real Django migrations, with no mocking of the migration layer.

Each test uses transaction=True so migration state changes are actually committed,
and cleans up by re-applying all migrations in a finally block.
"""

from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.db import connection
from django.db.migrations.loader import MigrationLoader


def _applied(app_label: str) -> set:
    """Return the set of applied migration names for an app."""
    loader = MigrationLoader(connection)
    return {name for (app, name) in loader.applied_migrations if app == app_label}


@pytest.mark.django_db(transaction=True)
def test_migrateprevious_rolls_back_one_migration():
    """Running migrateprevious rolls back only the latest migration, leaving the previous one applied."""
    assert "0001_initial" in _applied("testapp")
    assert "0002_author_bio" in _applied("testapp")

    try:
        call_command("migrateprevious", "testapp", stdout=StringIO())

        applied = _applied("testapp")
        assert "0001_initial" in applied
        assert "0002_author_bio" not in applied
    finally:
        call_command("migrate", "testapp", verbosity=0)


@pytest.mark.django_db(transaction=True)
def test_migrateprevious_raises_when_only_one_migration_applied():
    """Running migrateprevious when only one migration is applied raises a CommandError."""
    from django.core.management.base import CommandError

    # Roll back to 0001 first so there is no "previous" to go to
    call_command("migrate", "testapp", "0001", verbosity=0)

    try:
        with pytest.raises(CommandError):
            call_command("migrateprevious", "testapp", stdout=StringIO())
    finally:
        call_command("migrate", "testapp", verbosity=0)


@pytest.mark.django_db(transaction=True)
def test_migraterollback_rolls_back_to_specified_migration():
    """migraterollback calls migrate with the migration returned by get_latest_migration_in_git."""
    assert "0001_initial" in _applied("testapp")
    assert "0002_author_bio" in _applied("testapp")

    with patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git") as mock_git:
        mock_git.return_value = "0001"

        try:
            call_command("migraterollback", "testapp", "main", stdout=StringIO())

            applied = _applied("testapp")
            assert "0001_initial" in applied
            assert "0002_author_bio" not in applied
        finally:
            call_command("migrate", "testapp", verbosity=0)


@pytest.mark.django_db(transaction=True)
def test_migraterollback_raises_when_git_returns_no_migration():
    """migraterollback raises a CommandError when no migration is found in git."""
    from django.core.management.base import CommandError

    with patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git") as mock_git:
        mock_git.return_value = ""

        with pytest.raises(CommandError):
            call_command("migraterollback", "testapp", "main", stdout=StringIO())
