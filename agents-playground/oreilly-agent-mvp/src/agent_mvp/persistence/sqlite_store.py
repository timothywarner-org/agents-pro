"""SQLite persistence for pipeline results.

Provides enterprise-pattern persistence using SQLite:
- Stores run metadata for fast queries
- Stores full JSON results for complete data
- Auto-creates tables on first use
- Thread-safe with connection-per-call pattern
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from ..models import PipelineResult


class SQLiteStore:
    """SQLite-backed storage for pipeline results.

    Usage:
        store = SQLiteStore(Path("data/pipeline.db"))
        store.save_result(result)

        # Query runs
        recent = store.get_recent_runs(limit=10)
        failures = store.get_runs_by_verdict("fail")
    """

    def __init__(self, db_path: Path):
        """Initialize the store.

        Args:
            db_path: Path to SQLite database file. Created if doesn't exist.
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a new database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn

    def _init_schema(self) -> None:
        """Create tables if they don't exist."""
        with self._get_connection() as conn:
            conn.executescript("""
                -- Pipeline run metadata (fast queries)
                CREATE TABLE IF NOT EXISTS pipeline_runs (
                    run_id TEXT PRIMARY KEY,
                    issue_id TEXT NOT NULL,
                    repo TEXT,
                    issue_number INTEGER,
                    title TEXT,
                    source TEXT,
                    verdict TEXT,
                    started_at TEXT,
                    completed_at TEXT,
                    duration_seconds REAL,
                    pm_criteria_count INTEGER,
                    dev_file_count INTEGER,
                    qa_finding_count INTEGER
                );

                -- Full result JSON (complete data)
                CREATE TABLE IF NOT EXISTS pipeline_results (
                    run_id TEXT PRIMARY KEY,
                    result_json TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (run_id) REFERENCES pipeline_runs(run_id)
                );

                -- Indexes for common queries
                CREATE INDEX IF NOT EXISTS idx_runs_issue ON pipeline_runs(issue_id);
                CREATE INDEX IF NOT EXISTS idx_runs_repo ON pipeline_runs(repo);
                CREATE INDEX IF NOT EXISTS idx_runs_verdict ON pipeline_runs(verdict);
                CREATE INDEX IF NOT EXISTS idx_runs_completed ON pipeline_runs(completed_at);
            """)
            conn.commit()

    def save_result(self, result: PipelineResult) -> None:
        """Save a pipeline result to the database.

        Args:
            result: The PipelineResult to persist.
        """
        now = datetime.utcnow().isoformat()

        # Extract metadata for the runs table
        run_data = {
            "run_id": result.run_id,
            "issue_id": result.issue.issue_id,
            "repo": result.issue.repo,
            "issue_number": result.issue.issue_number,
            "title": result.issue.title,
            "source": result.issue.source,
            "verdict": result.qa.verdict.value if result.qa else None,
            "started_at": result.timestamp_utc,  # Use timestamp from result
            "completed_at": now,
            "duration_seconds": None,  # Not tracked in current model
            "pm_criteria_count": len(result.pm.acceptance_criteria) if result.pm else 0,
            "dev_file_count": len(result.dev.files) if result.dev else 0,
            "qa_finding_count": len(result.qa.findings) if result.qa else 0,
        }

        # Full JSON for the results table
        result_json = result.model_dump_json(indent=2)

        with self._get_connection() as conn:
            # Insert or replace run metadata
            conn.execute("""
                INSERT OR REPLACE INTO pipeline_runs (
                    run_id, issue_id, repo, issue_number, title, source,
                    verdict, started_at, completed_at, duration_seconds,
                    pm_criteria_count, dev_file_count, qa_finding_count
                ) VALUES (
                    :run_id, :issue_id, :repo, :issue_number, :title, :source,
                    :verdict, :started_at, :completed_at, :duration_seconds,
                    :pm_criteria_count, :dev_file_count, :qa_finding_count
                )
            """, run_data)

            # Insert or replace full result
            conn.execute("""
                INSERT OR REPLACE INTO pipeline_results (run_id, result_json, created_at)
                VALUES (?, ?, ?)
            """, (result.run_id, result_json, now))

            conn.commit()

    def get_result(self, run_id: str) -> PipelineResult | None:
        """Get a full result by run ID.

        Args:
            run_id: The run ID to fetch.

        Returns:
            PipelineResult if found, None otherwise.
        """
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT result_json FROM pipeline_results WHERE run_id = ?",
                (run_id,)
            ).fetchone()

            if row:
                return PipelineResult.model_validate_json(row["result_json"])
            return None

    def get_recent_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        """Get recent pipeline runs (metadata only).

        Args:
            limit: Maximum number of runs to return.

        Returns:
            List of run metadata dicts.
        """
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM pipeline_runs
                ORDER BY completed_at DESC
                LIMIT ?
            """, (limit,)).fetchall()

            return [dict(row) for row in rows]

    def get_runs_by_verdict(self, verdict: str, limit: int = 50) -> list[dict[str, Any]]:
        """Get runs filtered by verdict.

        Args:
            verdict: Verdict to filter by ('pass', 'fail', 'needs-human').
            limit: Maximum number of runs to return.

        Returns:
            List of run metadata dicts.
        """
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM pipeline_runs
                WHERE verdict = ?
                ORDER BY completed_at DESC
                LIMIT ?
            """, (verdict, limit)).fetchall()

            return [dict(row) for row in rows]

    def get_runs_by_repo(self, repo: str, limit: int = 50) -> list[dict[str, Any]]:
        """Get runs filtered by repository.

        Args:
            repo: Repository in 'owner/repo' format.
            limit: Maximum number of runs to return.

        Returns:
            List of run metadata dicts.
        """
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM pipeline_runs
                WHERE repo = ?
                ORDER BY completed_at DESC
                LIMIT ?
            """, (repo, limit)).fetchall()

            return [dict(row) for row in rows]

    def get_stats(self) -> dict[str, Any]:
        """Get aggregate statistics.

        Returns:
            Dict with total_runs, pass_count, fail_count, etc.
        """
        with self._get_connection() as conn:
            stats = {}

            # Total runs
            stats["total_runs"] = conn.execute(
                "SELECT COUNT(*) FROM pipeline_runs"
            ).fetchone()[0]

            # Verdict breakdown
            verdict_rows = conn.execute("""
                SELECT verdict, COUNT(*) as count
                FROM pipeline_runs
                GROUP BY verdict
            """).fetchall()
            stats["by_verdict"] = {row["verdict"]: row["count"] for row in verdict_rows}

            # Average duration
            avg_row = conn.execute("""
                SELECT AVG(duration_seconds) as avg_duration
                FROM pipeline_runs
                WHERE duration_seconds IS NOT NULL
            """).fetchone()
            stats["avg_duration_seconds"] = avg_row["avg_duration"]

            # Repos processed
            stats["unique_repos"] = conn.execute(
                "SELECT COUNT(DISTINCT repo) FROM pipeline_runs"
            ).fetchone()[0]

            return stats
