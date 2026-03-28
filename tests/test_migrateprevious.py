from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class MigratePreviousCommandTest(TestCase):
    @patch("migration_rollback.management.commands.migrateprevious.management.call_command")
    @patch("migration_rollback.management.commands.migrateprevious.get_previous_migration")
    def test_rolls_back_app_to_previous_migration(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0001"

        call_command("migrateprevious", "myapp", stdout=StringIO())

        mock_get_migration.assert_called_once_with(app_name="myapp")
        args, kwargs = mock_migrate.call_args
        assert args == ("migrate", "myapp", "0001")

    @patch("migration_rollback.management.commands.migrateprevious.get_previous_migration")
    def test_raises_error_when_no_migration_found(self, mock_get_migration):
        mock_get_migration.return_value = ""

        with self.assertRaises(CommandError):
            call_command("migrateprevious", "myapp", stdout=StringIO())
