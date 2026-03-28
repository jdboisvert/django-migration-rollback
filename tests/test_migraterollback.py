from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class MigrateRollbackCommandTest(TestCase):
    # --- single app ---

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_rolls_back_app_to_migration_on_branch(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0002"

        call_command("migraterollback", "myapp", branch="main", stdout=StringIO())

        mock_get_migration.assert_called_once_with(app_name="myapp", branch_name="main")
        args, kwargs = mock_migrate.call_args
        assert args == ("migrate", "myapp", "0002")

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_uses_main_as_default_branch(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0001"

        call_command("migraterollback", "myapp", stdout=StringIO())

        mock_get_migration.assert_called_once_with(app_name="myapp", branch_name="main")

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_fake_flag_is_passed_to_migrate(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0002"

        call_command("migraterollback", "myapp", "--fake", branch="main", stdout=StringIO())

        _, kwargs = mock_migrate.call_args
        assert kwargs["fake"] is True
        assert kwargs["fake_initial"] is False

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_fake_initial_flag_is_passed_to_migrate(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0002"

        call_command("migraterollback", "myapp", "--fake-initial", branch="main", stdout=StringIO())

        _, kwargs = mock_migrate.call_args
        assert kwargs["fake"] is False
        assert kwargs["fake_initial"] is True

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_fake_flags_default_to_false(self, mock_get_migration, mock_migrate):
        mock_get_migration.return_value = "0002"

        call_command("migraterollback", "myapp", branch="main", stdout=StringIO())

        _, kwargs = mock_migrate.call_args
        assert kwargs["fake"] is False
        assert kwargs["fake_initial"] is False

    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_raises_error_when_no_migration_found(self, mock_get_migration):
        mock_get_migration.return_value = ""

        with self.assertRaises(CommandError):
            call_command("migraterollback", "myapp", branch="main", stdout=StringIO())

    # --- multiple explicit apps ---

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    def test_rolls_back_multiple_explicit_apps(self, mock_get_migration, mock_migrate):
        mock_get_migration.side_effect = ["0001", "0003"]

        call_command("migraterollback", "app1", "app2", branch="main", stdout=StringIO())

        assert mock_migrate.call_count == 2
        assert mock_migrate.call_args_list[0][0] == ("migrate", "app1", "0001")
        assert mock_migrate.call_args_list[1][0] == ("migrate", "app2", "0003")

    # --- rollback all ---

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    @patch("migration_rollback.management.commands.migraterollback.get_all_migrated_app_names")
    def test_rolls_back_all_apps_when_no_app_given(self, mock_get_apps, mock_get_migration, mock_migrate):
        mock_get_apps.return_value = ["app1", "app2"]
        mock_get_migration.side_effect = ["0001", "0003"]

        call_command("migraterollback", stdout=StringIO())

        assert mock_migrate.call_count == 2
        assert mock_migrate.call_args_list[0][0] == ("migrate", "app1", "0001")
        assert mock_migrate.call_args_list[1][0] == ("migrate", "app2", "0003")

    @patch("migration_rollback.management.commands.migraterollback.get_all_migrated_app_names")
    def test_raises_error_when_no_apps_found(self, mock_get_apps):
        mock_get_apps.return_value = []

        with self.assertRaises(CommandError):
            call_command("migraterollback", stdout=StringIO())

    @patch("migration_rollback.management.commands.migraterollback.get_all_migrated_app_names")
    def test_excludes_system_apps_by_default(self, mock_get_apps):
        mock_get_apps.return_value = []

        with self.assertRaises(CommandError):
            call_command("migraterollback", stdout=StringIO())

        mock_get_apps.assert_called_once_with(include_system_apps=False)

    @patch("migration_rollback.management.commands.migraterollback.management.call_command")
    @patch("migration_rollback.management.commands.migraterollback.get_latest_migration_in_git")
    @patch("migration_rollback.management.commands.migraterollback.get_all_migrated_app_names")
    def test_includes_system_apps_when_flag_given(self, mock_get_apps, mock_get_migration, mock_migrate):
        mock_get_apps.return_value = ["app1"]
        mock_get_migration.return_value = "0001"

        call_command("migraterollback", "--include-system-apps", stdout=StringIO())

        mock_get_apps.assert_called_once_with(include_system_apps=True)
