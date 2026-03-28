from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class MigrateRollbackCommandTest(TestCase):
    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_rolls_back_app_to_migration_on_branch(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0002"

        call_command("migraterollback", "myapp", "main", stdout=StringIO())

        mock_get_migration.assert_called_once_with(app_name="myapp", branch_name="main")
        args, kwargs = mock_migrate.call_args
        assert args == ("migrate", "myapp", "0002")

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_uses_main_as_default_branch(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0001"

        call_command("migraterollback", "myapp", stdout=StringIO())

        mock_get_migration.assert_called_once_with(app_name="myapp", branch_name="main")

    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_raises_error_when_no_migration_found(self, mock_get_migration):
        mock_get_migration.return_value = ""

        with self.assertRaises(CommandError):
            call_command("migraterollback", "myapp", "main", stdout=StringIO())
