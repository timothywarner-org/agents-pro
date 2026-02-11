"""
Tests for JSON schema validation.
"""

import pytest

from agent_mvp.util.json_schema import validate_issue, IssueValidationError


class TestValidateIssue:
    """Tests for the validate_issue function."""

    def test_valid_issue(self):
        """Test that a valid issue passes validation."""
        valid_issue = {
            "issue_id": "owner/repo#123",
            "repo": "owner/repo",
            "issue_number": 123,
            "title": "Test issue",
            "body": "This is a test issue",
            "labels": ["bug", "priority:high"],
            "url": "https://github.com/owner/repo/issues/123",
            "source": "mock"
        }
        assert validate_issue(valid_issue) is True

    def test_minimal_valid_issue(self):
        """Test that a minimal valid issue passes."""
        minimal_issue = {
            "issue_id": "owner/repo#1",
            "repo": "owner/repo",
            "issue_number": 1,
            "title": "Minimal",
            "url": "https://github.com/owner/repo/issues/1"
        }
        assert validate_issue(minimal_issue) is True

    def test_missing_required_field(self):
        """Test that missing required fields raise error."""
        invalid_issue = {
            "issue_id": "owner/repo#123",
            "repo": "owner/repo",
            # missing issue_number, title, url
        }
        with pytest.raises(IssueValidationError) as exc_info:
            validate_issue(invalid_issue)
        assert "Missing required field" in str(exc_info.value.errors)

    def test_invalid_issue_id_format(self):
        """Test that invalid issue_id format raises error."""
        invalid_issue = {
            "issue_id": "invalid-format",
            "repo": "owner/repo",
            "issue_number": 123,
            "title": "Test",
            "url": "https://github.com/owner/repo/issues/123"
        }
        with pytest.raises(IssueValidationError) as exc_info:
            validate_issue(invalid_issue)
        assert "issue_id must be in format" in str(exc_info.value.errors)

    def test_invalid_issue_number(self):
        """Test that issue_number < 1 raises error."""
        invalid_issue = {
            "issue_id": "owner/repo#0",
            "repo": "owner/repo",
            "issue_number": 0,
            "title": "Test",
            "url": "https://github.com/owner/repo/issues/0"
        }
        with pytest.raises(IssueValidationError) as exc_info:
            validate_issue(invalid_issue)
        assert "issue_number must be >= 1" in str(exc_info.value.errors)

    def test_invalid_source_value(self):
        """Test that invalid source value raises error."""
        invalid_issue = {
            "issue_id": "owner/repo#123",
            "repo": "owner/repo",
            "issue_number": 123,
            "title": "Test",
            "url": "https://github.com/owner/repo/issues/123",
            "source": "invalid-source"
        }
        with pytest.raises(IssueValidationError) as exc_info:
            validate_issue(invalid_issue)
        assert "source must be one of" in str(exc_info.value.errors)

    def test_not_a_dict(self):
        """Test that non-dict input raises error."""
        with pytest.raises(IssueValidationError) as exc_info:
            validate_issue("not a dict")
        assert "must be a JSON object" in str(exc_info.value)

    def test_empty_title(self):
        """Test that empty title raises error."""
        invalid_issue = {
            "issue_id": "owner/repo#123",
            "repo": "owner/repo",
            "issue_number": 123,
            "title": "",
            "url": "https://github.com/owner/repo/issues/123"
        }
        with pytest.raises(IssueValidationError) as exc_info:
            validate_issue(invalid_issue)
        assert "title must not be empty" in str(exc_info.value.errors)
