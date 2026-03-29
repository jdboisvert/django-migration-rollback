import pytest
from unittest.mock import MagicMock, patch

from migration_rollback.utils.migration_utils import (
    get_all_migrated_app_names,
    get_latest_migration_in_git,
    get_previous_migration,
)


def _mock_popen(output: bytes) -> MagicMock:
    """Return a mock Popen instance whose stdout.read() returns the given bytes."""
    mock_pipe = MagicMock()
    mock_pipe.stdout.read.return_value = output
    return mock_pipe


class TestGetAllMigratedAppNames:
    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_returns_apps_with_applied_migrations(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {
            ("myapp", "0001_initial"): None,
            ("myapp", "0002_add_field"): None,
            ("otherapp", "0001_initial"): None,
        }
        mock_loader_class.return_value = mock_loader

        result = get_all_migrated_app_names()

        assert set(result) == {"myapp", "otherapp"}

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_returns_each_app_only_once(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {
            ("myapp", "0001_initial"): None,
            ("myapp", "0002_add_field"): None,
            ("myapp", "0003_another"): None,
        }
        mock_loader_class.return_value = mock_loader

        result = get_all_migrated_app_names()

        assert result.count("myapp") == 1

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_returns_empty_list_when_no_migrations_applied(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {}
        mock_loader_class.return_value = mock_loader

        result = get_all_migrated_app_names()

        assert result == []

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_excludes_system_apps_by_default(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {
            ("myapp", "0001_initial"): None,
            ("auth", "0001_initial"): None,
            ("contenttypes", "0001_initial"): None,
            ("sessions", "0001_initial"): None,
            ("admin", "0001_initial"): None,
        }
        mock_loader_class.return_value = mock_loader

        result = get_all_migrated_app_names()

        assert result == ["myapp"]

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_includes_system_apps_when_requested(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {
            ("myapp", "0001_initial"): None,
            ("auth", "0001_initial"): None,
        }
        mock_loader_class.return_value = mock_loader

        result = get_all_migrated_app_names(include_system_apps=True)

        assert set(result) == {"myapp", "auth"}


class TestGetLatestMigrationInGit:
    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_strips_trailing_newline_from_result(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"\n")

        result = get_latest_migration_in_git(app_name="myapp", branch_name="main")

        assert result == ""

    def test_raises_on_unsafe_app_name(self):
        with pytest.raises(ValueError, match="Invalid app_name"):
            get_latest_migration_in_git(app_name="my app; rm -rf /", branch_name="main")

    def test_raises_on_unsafe_branch_name(self):
        with pytest.raises(ValueError, match="Invalid branch_name"):
            get_latest_migration_in_git(app_name="myapp", branch_name="main; rm -rf /")

    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_returns_migration_number(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"0003_add_field\n")

        result = get_latest_migration_in_git(app_name="myapp", branch_name="main")

        assert result == "0003"

    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_returns_empty_string_when_no_migration_found(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"")

        result = get_latest_migration_in_git(app_name="myapp", branch_name="main")

        assert result == ""

    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_passes_correct_branch_and_app_to_command(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"0001_initial\n")

        get_latest_migration_in_git(app_name="myapp", branch_name="feature/my-branch")

        command = mock_popen.call_args[0][0]
        assert "feature/my-branch" in command
        assert "myapp" in command


class TestGetPreviousMigration:
    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_returns_previous_migration_number(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {
            ("myapp", "0001_initial"): None,
            ("myapp", "0002_add_field"): None,
        }
        mock_loader_class.return_value = mock_loader

        result = get_previous_migration(app_name="myapp")

        assert result == "0001"

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_returns_empty_string_when_only_one_migration_applied(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {("myapp", "0001_initial"): None}
        mock_loader_class.return_value = mock_loader

        result = get_previous_migration(app_name="myapp")

        assert result == ""

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_returns_empty_string_when_no_migrations_applied(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {}
        mock_loader_class.return_value = mock_loader

        result = get_previous_migration(app_name="myapp")

        assert result == ""

    @patch("migration_rollback.utils.migration_utils.MigrationLoader")
    def test_filters_by_app_name(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.applied_migrations = {
            ("myapp", "0001_initial"): None,
            ("myapp", "0002_add_field"): None,
            ("otherapp", "0001_initial"): None,
            ("otherapp", "0002_something"): None,
        }
        mock_loader_class.return_value = mock_loader

        result = get_previous_migration(app_name="myapp")

        assert result == "0001"
