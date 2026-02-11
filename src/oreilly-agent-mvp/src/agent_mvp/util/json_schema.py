"""
JSON schema validation for issue files.

Validates incoming issues against the expected schema before processing.
"""

from __future__ import annotations

from typing import Any


class IssueValidationError(Exception):
    """Raised when an issue fails schema validation."""

    def __init__(self, message: str, errors: list[str] | None = None):
        """Initialize with message and optional list of errors.

        Args:
            message: Main error message.
            errors: List of specific validation errors.
        """
        super().__init__(message)
        self.errors = errors or []


# Issue JSON Schema definition
ISSUE_SCHEMA = {
    "type": "object",
    "required": ["issue_id", "repo", "issue_number", "title", "url"],
    "properties": {
        "issue_id": {
            "type": "string",
            "description": "Unique identifier in format 'owner/repo#123'",
            "pattern": r"^[\w.-]+/[\w.-]+#\d+$",
        },
        "repo": {
            "type": "string",
            "description": "Repository in 'owner/repo' format",
            "pattern": r"^[\w.-]+/[\w.-]+$",
        },
        "issue_number": {
            "type": "integer",
            "description": "Issue number within the repository",
            "minimum": 1,
        },
        "title": {
            "type": "string",
            "description": "Issue title",
            "minLength": 1,
        },
        "body": {
            "type": "string",
            "description": "Issue body/description",
            "default": "",
        },
        "labels": {
            "type": "array",
            "description": "Labels attached to the issue",
            "items": {"type": "string"},
            "default": [],
        },
        "url": {
            "type": "string",
            "description": "URL to the issue on GitHub",
            "pattern": r"^https?://",
        },
        "source": {
            "type": "string",
            "description": "Where this issue came from",
            "enum": ["mock", "github-mcp", "manual"],
            "default": "manual",
        },
    },
    "additionalProperties": False,
}


def validate_issue(data: Any) -> bool:
    """Validate issue data against the schema.

    Uses a lightweight validation approach without requiring jsonschema library.
    For production, consider using pydantic validation via Issue.model_validate().

    Args:
        data: The data to validate.

    Returns:
        True if valid.

    Raises:
        IssueValidationError: If validation fails.
    """
    errors = []

    # Check it's a dict
    if not isinstance(data, dict):
        raise IssueValidationError(
            "Issue must be a JSON object",
            ["Expected object, got " + type(data).__name__]
        )

    # Check required fields
    required = ["issue_id", "repo", "issue_number", "title", "url"]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if errors:
        raise IssueValidationError(
            f"Issue validation failed: {len(errors)} error(s)",
            errors
        )

    # Type checks
    if "issue_id" in data and not isinstance(data["issue_id"], str):
        errors.append("issue_id must be a string")

    if "repo" in data and not isinstance(data["repo"], str):
        errors.append("repo must be a string")

    if "issue_number" in data:
        if not isinstance(data["issue_number"], int):
            errors.append("issue_number must be an integer")
        elif data["issue_number"] < 1:
            errors.append("issue_number must be >= 1")

    if "title" in data:
        if not isinstance(data["title"], str):
            errors.append("title must be a string")
        elif len(data["title"]) < 1:
            errors.append("title must not be empty")

    if "body" in data and not isinstance(data["body"], str):
        errors.append("body must be a string")

    if "labels" in data:
        if not isinstance(data["labels"], list):
            errors.append("labels must be an array")
        elif not all(isinstance(label, str) for label in data["labels"]):
            errors.append("labels must be an array of strings")

    if "url" in data and not isinstance(data["url"], str):
        errors.append("url must be a string")

    if "source" in data:
        valid_sources = ["mock", "github-mcp", "manual"]
        if data["source"] not in valid_sources:
            errors.append(f"source must be one of: {valid_sources}")

    # Pattern checks
    if "issue_id" in data and isinstance(data["issue_id"], str):
        # Check format: owner/repo#123
        import re
        if not re.match(r"^[\w.-]+/[\w.-]+#\d+$", data["issue_id"]):
            errors.append("issue_id must be in format 'owner/repo#123'")

    if "repo" in data and isinstance(data["repo"], str):
        import re
        if not re.match(r"^[\w.-]+/[\w.-]+$", data["repo"]):
            errors.append("repo must be in format 'owner/repo'")

    if "url" in data and isinstance(data["url"], str):
        if not data["url"].startswith(("http://", "https://")):
            errors.append("url must start with http:// or https://")

    if errors:
        raise IssueValidationError(
            f"Issue validation failed: {len(errors)} error(s)",
            errors
        )

    return True


def get_schema_description() -> str:
    """Get a human-readable description of the issue schema.

    Returns:
        Formatted schema description.
    """
    return """
Issue JSON Schema
=================

Required fields:
  - issue_id (string): Unique identifier in format 'owner/repo#123'
  - repo (string): Repository in 'owner/repo' format
  - issue_number (integer): Issue number (>= 1)
  - title (string): Issue title (non-empty)
  - url (string): URL to the issue (must start with http:// or https://)

Optional fields:
  - body (string): Issue description (default: "")
  - labels (array of strings): Labels on the issue (default: [])
  - source (string): Origin of issue, one of: "mock", "github-mcp", "manual"

Example:
{
  "issue_id": "microsoft/vscode#12345",
  "repo": "microsoft/vscode",
  "issue_number": 12345,
  "title": "Add dark mode toggle to settings",
  "body": "Users want a quick way to toggle dark mode...",
  "labels": ["enhancement", "ui"],
  "url": "https://github.com/microsoft/vscode/issues/12345",
  "source": "mock"
}
""".strip()
