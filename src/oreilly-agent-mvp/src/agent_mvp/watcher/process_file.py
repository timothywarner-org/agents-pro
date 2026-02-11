"""
File processing logic for the folder watcher.

Handles validation, pipeline execution, and file movement.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..config import Config
from ..issue_sources import FileIssueSource
from ..logging_setup import get_pipeline_logger
from ..persistence import SQLiteStore
from ..util.fs import atomic_move, get_timestamped_filename, safe_write_json
from ..util.reporting import format_run_report
from ..util.json_schema import IssueValidationError
from ..pipeline.run_once import run_pipeline, save_result


def process_issue_file(
    file_path: Path,
    config: Config,
    write_dev_files: bool = False,
) -> Optional[Path]:
    """Process a single issue file through the pipeline.

    This function:
    1. Validates the issue JSON
    2. Moves the file to processed/ (or processed/invalid/ on failure)
    3. Runs the pipeline
    4. Saves the result to outgoing/

    Args:
        file_path: Path to the issue JSON file.
        config: Application configuration.
        write_dev_files: Whether to write dev files to disk.

    Returns:
        Path to the output file if successful, None if failed.
    """
    logger = get_pipeline_logger()
    logger.file_operation("Processing", str(file_path))

    # Generate processed filename with timestamp
    processed_name = get_timestamped_filename(
        file_path.stem,
        file_path.suffix,
    )

    try:
        # Validate and load the issue
        issue = FileIssueSource.from_path(file_path)
        logger.info(f"Loaded issue: {issue.issue_id}")

    except IssueValidationError as e:
        # Move to invalid folder
        logger.error(f"Validation failed: {e}")
        for error in e.errors:
            logger.error(f"  - {error}")

        invalid_dir = config.processed_dir / "invalid"
        invalid_dir.mkdir(parents=True, exist_ok=True)
        invalid_path = invalid_dir / processed_name

        try:
            atomic_move(file_path, invalid_path)
            logger.file_operation("Moved to invalid", str(invalid_path))
        except Exception as move_error:
            logger.error(f"Failed to move invalid file: {move_error}")

        return None

    except Exception as e:
        logger.error(f"Failed to load issue: {e}")
        return None

    # Move to processed folder (before running pipeline)
    processed_path = config.processed_dir / processed_name
    try:
        atomic_move(file_path, processed_path)
        logger.file_operation("Moved to processed", str(processed_path))
    except Exception as e:
        logger.error(f"Failed to move to processed: {e}")
        return None

    # Run the pipeline
    try:
        result = run_pipeline(
            issue=issue,
            config=config,
            source_file=str(processed_path),
        )

        # Save result to file (JSON + HTML)
        json_path, html_path = save_result(
            result=result,
            output_dir=config.outgoing_dir,
            write_files=write_dev_files,
        )

        # Persist to SQLite database
        db_path = config.project_root / 'data' / 'pipeline.db'
        store = SQLiteStore(db_path)
        store.save_result(result)
        logger.file_operation('Persisted to database', str(db_path))

        # Print run report with token usage and HTML link
        print("\n" + format_run_report(result, json_path, html_path))

        # Log completion
        logger.complete_run(
            run_id=result.run_id,
            issue_id=result.issue.issue_id,
            verdict=result.qa.verdict.value,
            output_file=str(json_path),
        )

        return json_path

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", e)
        return None
