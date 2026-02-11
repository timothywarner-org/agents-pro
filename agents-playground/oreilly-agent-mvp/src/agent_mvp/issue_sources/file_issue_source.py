"""
File-based issue source for loading issues from JSON files.

This is the primary way issues enter the pipeline:
- Manually created JSON files
- Files saved from GitHub MCP
- Files dropped into the incoming/ folder
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from ..models import Issue
from ..util.json_schema import validate_issue, IssueValidationError


class FileIssueSource:
    """Load and validate issues from JSON files.
    
    Provides static methods for loading issues from file paths.
    """

    @staticmethod
    def from_path(path: Union[str, Path]) -> Issue:
        """Load an issue from a JSON file.

        Args:
            path: Path to the JSON file.

        Returns:
            Validated Issue model.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            IssueValidationError: If the JSON doesn't match the schema.
            json.JSONDecodeError: If the file isn't valid JSON.
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Issue file not found: {path}")
        
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        # Read and parse JSON
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)

        # Validate against schema
        validate_issue(data)

        # Create and return Issue model
        return Issue(**data)

    @staticmethod
    def from_string(json_string: str) -> Issue:
        """Load an issue from a JSON string.

        Args:
            json_string: JSON string representing an issue.

        Returns:
            Validated Issue model.

        Raises:
            IssueValidationError: If the JSON doesn't match the schema.
            json.JSONDecodeError: If the string isn't valid JSON.
        """
        data = json.loads(json_string)
        validate_issue(data)
        return Issue(**data)

    @staticmethod
    def validate_file(path: Union[str, Path]) -> list[str]:
        """Validate an issue file without loading it.

        Args:
            path: Path to the JSON file.

        Returns:
            Empty list if valid, list of error messages if invalid.
        """
        path = Path(path)
        errors = []

        if not path.exists():
            return [f"File not found: {path}"]

        if not path.is_file():
            return [f"Path is not a file: {path}"]

        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)
            validate_issue(data)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")
        except IssueValidationError as e:
            errors.extend(e.errors)
        except Exception as e:
            errors.append(f"Unexpected error: {e}")

        return errors
