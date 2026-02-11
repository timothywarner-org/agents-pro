"""
Mock issue source for loading pre-defined test issues.

Provides a simple interface to load issues from the mock_issues/ folder.
Useful for demos and testing without needing GitHub access.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from ..config import get_config
from ..models import Issue
from .file_issue_source import FileIssueSource


class MockIssueSource:
    """Load mock issues from the mock_issues/ folder.

    Mock issues are pre-defined JSON files for testing and demos.
    """

    def __init__(self, mock_dir: Optional[Path] = None):
        """Initialize the mock issue source.

        Args:
            mock_dir: Directory containing mock issues.
                      Defaults to project's mock_issues/ folder.
        """
        if mock_dir is None:
            config = get_config()
            mock_dir = config.mock_issues_dir
        self.mock_dir = Path(mock_dir)

    def list_available(self) -> list[str]:
        """List available mock issue files.

        Returns:
            List of mock issue filenames.
        """
        if not self.mock_dir.exists():
            return []
        return sorted([f.name for f in self.mock_dir.glob("issue_*.json")])

    def load(self, filename: str) -> Issue:
        """Load a specific mock issue by filename.

        Args:
            filename: Name of the mock file (e.g., "issue_001.json").

        Returns:
            Validated Issue model.

        Raises:
            FileNotFoundError: If the mock file doesn't exist.
        """
        file_path = self.mock_dir / filename
        if not file_path.exists():
            available = self.list_available()
            raise FileNotFoundError(
                f"Mock issue not found: {filename}\n"
                f"Available mock issues: {available}"
            )
        return FileIssueSource.from_path(file_path)

    def load_by_path(self, path: Union[str, Path]) -> Issue:
        """Load a mock issue by full or relative path.

        Args:
            path: Path to the mock file.

        Returns:
            Validated Issue model.
        """
        return FileIssueSource.from_path(path)

    @classmethod
    def get_default(cls) -> "MockIssueSource":
        """Get a MockIssueSource with default configuration.

        Returns:
            MockIssueSource instance.
        """
        return cls()
