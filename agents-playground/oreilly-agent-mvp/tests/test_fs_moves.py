"""
Tests for file system utilities.
"""

import tempfile
from pathlib import Path

import pytest

from agent_mvp.util.fs import (
    atomic_move,
    ensure_dirs,
    get_timestamped_filename,
    safe_write_json,
)


class TestAtomicMove:
    """Tests for atomic_move function."""

    def test_move_file(self, tmp_path):
        """Test moving a file to a new location."""
        # Create source file
        src = tmp_path / "source.txt"
        src.write_text("test content")

        # Move to destination
        dest = tmp_path / "subdir" / "dest.txt"
        result = atomic_move(src, dest)

        assert result == dest
        assert dest.exists()
        assert dest.read_text() == "test content"
        assert not src.exists()

    def test_move_nonexistent_file(self, tmp_path):
        """Test that moving a nonexistent file raises error."""
        src = tmp_path / "nonexistent.txt"
        dest = tmp_path / "dest.txt"

        with pytest.raises(FileNotFoundError):
            atomic_move(src, dest)

    def test_move_overwrites_existing(self, tmp_path):
        """Test that move overwrites existing destination."""
        src = tmp_path / "source.txt"
        src.write_text("new content")

        dest = tmp_path / "dest.txt"
        dest.write_text("old content")

        atomic_move(src, dest)

        assert dest.read_text() == "new content"


class TestEnsureDirs:
    """Tests for ensure_dirs function."""

    def test_create_single_dir(self, tmp_path):
        """Test creating a single directory."""
        new_dir = tmp_path / "new_dir"
        assert not new_dir.exists()

        ensure_dirs(new_dir)

        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_create_nested_dirs(self, tmp_path):
        """Test creating nested directories."""
        nested = tmp_path / "a" / "b" / "c"
        assert not nested.exists()

        ensure_dirs(nested)

        assert nested.exists()

    def test_existing_dir_no_error(self, tmp_path):
        """Test that existing directory does not raise error."""
        ensure_dirs(tmp_path)  # Should not raise
        assert tmp_path.exists()


class TestGetTimestampedFilename:
    """Tests for get_timestamped_filename function."""

    def test_generates_filename(self):
        """Test that function generates a valid filename."""
        filename = get_timestamped_filename("test")

        assert filename.startswith("test_")
        assert filename.endswith(".json")
        assert len(filename) > len("test_.json")

    def test_custom_extension(self):
        """Test custom extension."""
        filename = get_timestamped_filename("test", ".txt")
        assert filename.endswith(".txt")

    def test_extension_without_dot(self):
        """Test extension without leading dot."""
        filename = get_timestamped_filename("test", "csv")
        assert filename.endswith(".csv")


class TestSafeWriteJson:
    """Tests for safe_write_json function."""

    def test_writes_json(self, tmp_path):
        """Test that function writes JSON content."""
        path = tmp_path / "test.json"
        content = '{"key": "value"}'

        result = safe_write_json(content, path)

        assert result == path
        assert path.exists()
        assert path.read_text() == content

    def test_creates_parent_dirs(self, tmp_path):
        """Test that function creates parent directories."""
        path = tmp_path / "a" / "b" / "test.json"
        content = '{}'

        safe_write_json(content, path)

        assert path.exists()

    def test_no_temp_file_left_behind(self, tmp_path):
        """Test that no .tmp file is left behind."""
        path = tmp_path / "test.json"
        safe_write_json('{}',
 path)

        temp_path = path.with_suffix(".tmp")
        assert not temp_path.exists()
