"""
Integration tests that run the management commands against a real SQLite test DB
and real Django migrations, with no mocking of the migration layer.

Each test uses transaction=True so migration state changes are actually committed.
The `remigrate_testapp` fixture (defined in conftest.py) re-applies all migrations
after each test so the DB is clean for the next one.
"""

from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.db.migrations.loader import MigrationLoader


def _applied(app_label: str) -> set:
    """Return the set of applied migration names for an app."""
    loader = MigrationLoader(connection)
    return {name for (app, name) in loader.applied_migrations if app == app_label}


@pytest.mark.django_db(transaction=True)
def test_migrateprevious_rolls_back_one_migration(remigrate_testapp):
    """Running migrateprevious rolls back only the latest migration, leaving the previous one applied."""
    assert "0001_initial" in _applied("testapp")
    assert "0002_author_bio" in _applied("testapp")

    call_command("migrateprevious", "testapp", stdout=StringIO())

    applied = _applied("testapp")
    assert "0001_initial" in applied
    assert "0002_author_bio" not in applied


@pytest.mark.django_db(transaction=True)
def test_migrateprevious_raises_when_only_one_migration_applied(remigrate_testapp):
    """Running migrateprevious when only one migration is applied raises a CommandError."""
    call_command("migrate", "testapp", "0001", verbosity=0)

    with pytest.raises(CommandError):
        call_command("migrateprevious", "testapp", stdout=StringIO())


@pytest.mark.django_db(transaction=True)
def test_migraterollback_rolls_back_to_specified_migration(remigrate_testapp):
    """migraterollback calls migrate with the migration returned by get_latest_migration_in_git."""
    assert "0001_initial" in _applied("testapp")
    assert "0002_author_bio" in _applied("testapp")

    with patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git") as mock_git:
        mock_git.return_value = "0001"
        call_command("migraterollback", "testapp", "main", stdout=StringIO())

    applied = _applied("testapp")
    assert "0001_initial" in applied
    assert "0002_author_bio" not in applied


@pytest.mark.django_db(transaction=True)
def test_migraterollback_raises_when_git_returns_no_migration():
    """migraterollback raises a CommandError when no migration is found in git."""
    with patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git") as mock_git:
        mock_git.return_value = ""

        with pytest.raises(CommandError):
            call_command("migraterollback", "testapp", "main", stdout=StringIO())


def _table_columns(table_name: str) -> set:
    """Return the set of column names for a table in the current DB."""
    with connection.cursor() as cursor:
        return {col.name for col in connection.introspection.get_table_description(cursor, table_name)}


@pytest.mark.django_db(transaction=True)
def test_migrateprevious_fake_updates_migration_record_but_leaves_schema(remigrate_testapp):
    """--fake marks 0002 as unapplied but does not drop the bio column from the DB."""
    assert "0002_author_bio" in _applied("testapp")
    assert "bio" in _table_columns("testapp_author")

    call_command("migrateprevious", "testapp", "--fake", stdout=StringIO())

    assert "0002_author_bio" not in _applied("testapp")
    assert "bio" in _table_columns("testapp_author")


@pytest.mark.django_db(transaction=True)
def test_migraterollback_fake_updates_migration_record_but_leaves_schema(remigrate_testapp):
    """--fake marks 0002 as unapplied but does not drop the bio column from the DB."""
    assert "0002_author_bio" in _applied("testapp")
    assert "bio" in _table_columns("testapp_author")

    with patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git") as mock_git:
        mock_git.return_value = "0001"
        call_command("migraterollback", "testapp", "--fake", stdout=StringIO())

    assert "0002_author_bio" not in _applied("testapp")
    assert "bio" in _table_columns("testapp_author")


@pytest.mark.django_db(transaction=True)
def test_migrateprevious_rolls_back_all_apps_when_no_app_given(remigrate_testapp):
    """Omitting app rolls back both testapp and testapp2 by one migration each.

    get_all_migrated_app_names is patched to return only our two test apps so
    Django's built-in apps are not touched and test DB teardown stays intact.
    """
    assert "0002_author_bio" in _applied("testapp")
    assert "0002_book_summary" in _applied("testapp2")

    with patch("migration_rollback.management.commands.migrateprevious.get_all_migrated_app_names") as mock_apps:
        mock_apps.return_value = ["testapp", "testapp2"]
        call_command("migrateprevious", stdout=StringIO())

    assert "0001_initial" in _applied("testapp")
    assert "0002_author_bio" not in _applied("testapp")
    assert "0001_initial" in _applied("testapp2")
    assert "0002_book_summary" not in _applied("testapp2")


@pytest.mark.django_db(transaction=True)
def test_migraterollback_rolls_back_all_apps_when_no_app_given(remigrate_testapp):
    """Omitting app rolls back both testapp and testapp2 to the git branch state.

    get_all_migrated_app_names is patched to return only our two test apps so
    Django's built-in apps are not touched and test DB teardown stays intact.
    """
    assert "0002_author_bio" in _applied("testapp")
    assert "0002_book_summary" in _applied("testapp2")

    with patch("migration_rollback.management.commands.migraterollback.get_all_migrated_app_names") as mock_apps:
        mock_apps.return_value = ["testapp", "testapp2"]
        with patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git") as mock_git:
            mock_git.return_value = "0001"
            call_command("migraterollback", stdout=StringIO())

    assert "0001_initial" in _applied("testapp")
    assert "0002_author_bio" not in _applied("testapp")
    assert "0001_initial" in _applied("testapp2")
    assert "0002_book_summary" not in _applied("testapp2")
