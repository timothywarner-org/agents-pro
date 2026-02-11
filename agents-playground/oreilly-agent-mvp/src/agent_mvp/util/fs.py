"""
File system utilities for safe file operations.

All operations use pathlib for Windows compatibility.
Implements atomic moves to prevent data loss.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Union


def ensure_dirs(*dirs: Union[str, Path]) -> None:
    """Ensure directories exist, creating them if needed.

    Args:
        *dirs: Directory paths to ensure exist.
    """
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def atomic_move(src: Union[str, Path], dest: Union[str, Path]) -> Path:
    """Atomically move a file from src to dest.

    Uses shutil.move which handles cross-filesystem moves.
    If dest exists, it will be overwritten.

    Args:
        src: Source file path.
        dest: Destination file path.

    Returns:
        The destination path.

    Raises:
        FileNotFoundError: If source doesn't exist.
    """
    src = Path(src)
    dest = Path(dest)

    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")

    # Ensure destination directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Move the file
    shutil.move(str(src), str(dest))
    return dest


def get_timestamped_filename(prefix: str, extension: str = ".json") -> str:
    """Generate a timestamped filename.

    Args:
        prefix: Filename prefix.
        extension: File extension (default: .json).

    Returns:
        Filename like "prefix_20240115_143022.json"
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not extension.startswith("."):
        extension = "." + extension
    return f"{prefix}_{timestamp}{extension}"


def safe_write_json(content: str, path: Union[str, Path]) -> Path:
    """Safely write JSON content to a file.

    Writes to a temp file first, then moves to final location
    to prevent partial writes on failure.

    Args:
        content: JSON string to write.
        path: Destination file path.

    Returns:
        The written file path.
    """
    path = Path(path)
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file first
    temp_path = path.with_suffix(".tmp")
    temp_path.write_text(content, encoding="utf-8")

    # Move to final location
    shutil.move(str(temp_path), str(path))
    return path


def get_file_age_seconds(path: Union[str, Path]) -> float:
    """Get the age of a file in seconds.

    Args:
        path: Path to the file.

    Returns:
        Age in seconds since last modification.

    Raises:
        FileNotFoundError: If file doesn't exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    mtime = path.stat().st_mtime
    now = datetime.now().timestamp()
    return now - mtime


def list_json_files(directory: Union[str, Path]) -> list[Path]:
    """List all JSON files in a directory.

    Args:
        directory: Directory to scan.

    Returns:
        List of JSON file paths, sorted by name.
    """
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))
