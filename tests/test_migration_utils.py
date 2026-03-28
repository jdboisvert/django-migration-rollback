from unittest.mock import MagicMock, patch

import pytest

from migration_rollback.utils.migration_utils import (
    get_latest_migration_in_git,
    get_previous_migration,
)


def _mock_popen(output: bytes) -> MagicMock:
    """Return a mock Popen instance whose stdout.read() returns the given bytes."""
    mock_pipe = MagicMock()
    mock_pipe.stdout.read.return_value = output
    return mock_pipe


class TestGetLatestMigrationInGit:
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
    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_returns_migration_number(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"0002_some_change\n")

        result = get_previous_migration(app_name="myapp")

        assert result == "0002"

    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_returns_empty_string_when_no_migration_found(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"")

        result = get_previous_migration(app_name="myapp")

        assert result == ""

    @patch("migration_rollback.utils.migration_utils.Popen")
    def test_passes_app_name_to_command(self, mock_popen):
        mock_popen.return_value = _mock_popen(b"0001_initial\n")

        get_previous_migration(app_name="myapp")

        command = mock_popen.call_args[0][0]
        assert "myapp" in command
