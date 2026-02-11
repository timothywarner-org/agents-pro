"""Persistence module for storing pipeline results."""

from .sqlite_store import SQLiteStore

__all__ = ["SQLiteStore"]
