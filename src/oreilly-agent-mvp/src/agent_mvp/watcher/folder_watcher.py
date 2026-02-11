"""
Folder watcher for event-triggered pipeline execution.

Polls the incoming/ folder for new JSON files and processes them
through the agent pipeline.

Usage:
    python -m agent_mvp.watcher.folder_watcher
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path
from typing import Set

from ..config import Config, get_config
from ..logging_setup import setup_logging, get_pipeline_logger, print_banner, console
from ..util.fs import ensure_dirs
from .process_file import process_issue_file


class FolderWatcher:
    """Watch a folder for new issue files and process them.

    Uses polling (not filesystem events) for cross-platform reliability.
    Tracks processed files to avoid reprocessing.
    """

    def __init__(
        self,
        config: Config,
        poll_interval: float = 3.0,
        write_dev_files: bool = False,
        verbose_polling: bool = True,
    ):
        """Initialize the folder watcher.

        Args:
            config: Application configuration.
            poll_interval: Seconds between folder checks.
            write_dev_files: Whether to write dev files to disk.
            verbose_polling: When True, print the poll status each cycle (default: True).
        """
        self.config = config
        self.poll_interval = poll_interval
        self.write_dev_files = write_dev_files
        self.verbose_polling = verbose_polling
        self.logger = get_pipeline_logger()

        # Track files we've seen to avoid reprocessing
        self._seen_files: Set[str] = set()
        self._running = False

    def start(self):
        """Start watching the incoming folder.

        Runs until interrupted (Ctrl+C) or stop() is called.
        """
        self._running = True

        # Ensure directories exist
        ensure_dirs(
            self.config.incoming_dir,
            self.config.processed_dir,
            self.config.outgoing_dir,
        )

        self.logger.info(f"Watching folder: {self.config.incoming_dir}")
        self.logger.info(f"Poll interval: {self.poll_interval}s")
        console.print("[dim]Press Ctrl+C to stop[/]")
        console.print()

        # Initial scan to mark existing files as seen
        self._scan_existing()

        while self._running:
            try:
                self._poll()
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                self.logger.info("Interrupted by user")
                break

        self.logger.info("Watcher stopped")

    def stop(self):
        """Stop the watcher."""
        self._running = False

    def _scan_existing(self):
        """Scan for existing files without processing them.

        This prevents processing files that were already there
        before the watcher started.
        """
        existing = list(self.config.incoming_dir.glob("*.json"))
        for file_path in existing:
            self._seen_files.add(str(file_path))

        if existing:
            self.logger.info(
                f"Found {len(existing)} existing file(s) in incoming/ - "
                "will not process (already present at startup)"
            )

    def _poll(self):
        """Check for new files and process them."""
        # Get current JSON files
        current_files = list(self.config.incoming_dir.glob("*.json"))
        new_files = []

        for file_path in current_files:
            file_key = str(file_path)

            # Skip if we've already seen this file
            if file_key in self._seen_files:
                continue

            # Mark as seen immediately to prevent double-processing
            self._seen_files.add(file_key)

            # Verify file still exists (might have been moved already)
            if not file_path.exists():
                continue

            new_files.append(file_path)

        if self.verbose_polling:
            if new_files:
                names = ", ".join(file.name for file in new_files)
                console.print(
                    f"[cyan]Polling {self.config.incoming_dir} → new file(s): {names}[/]"
                )
            else:
                console.print(
                    f"[dim]Polling {self.config.incoming_dir} → no new files[/]"
                )

        for file_path in new_files:
            # Process the file
            console.rule(f"[bold cyan]New Issue File: {file_path.name}[/]")
            try:
                output_path = process_issue_file(
                    file_path=file_path,
                    config=self.config,
                    write_dev_files=self.write_dev_files,
                )

                if output_path:
                    console.print(
                        f"[success]✓ Successfully processed: {file_path.name}[/]"
                    )
                else:
                    console.print(
                        f"[warning]⚠ Processing failed: {file_path.name}[/]"
                    )

            except Exception as e:
                self.logger.error(f"Unexpected error processing {file_path.name}: {e}")

            console.print()


def main():
    """Main entry point for the folder watcher CLI."""
    parser = argparse.ArgumentParser(
        description="Watch incoming/ folder for new issues and process them",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start watching with default settings
  python -m agent_mvp.watcher.folder_watcher

  # Watch with custom poll interval
  python -m agent_mvp.watcher.folder_watcher --poll-interval 5

  # Watch and write dev files to disk
  python -m agent_mvp.watcher.folder_watcher --write-files
        """,
    )

    parser.add_argument(
        "--poll-interval",
        type=float,
        help=f"Seconds between folder checks (default: from config or 3)",
    )
    parser.add_argument(
        "--write-files",
        action="store_true",
        help="Write dev files to disk in addition to result JSON",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log level (default: INFO)",
    )

    args = parser.parse_args()

    # Determine project root
    if args.project_root:
        project_root = Path(args.project_root).resolve()
    else:
        cwd = Path.cwd()
        script_root = Path(__file__).resolve().parents[3]

        candidate_roots = [
            cwd,
            cwd / "oreilly-agent-mvp",
            cwd.parent,
            cwd.parent / "oreilly-agent-mvp",
            script_root,
        ]

        project_root = next(
            (
                candidate.resolve()
                for candidate in candidate_roots
                if candidate and (candidate / "pyproject.toml").exists()
            ),
            script_root,
        )

    # Load config
    config = Config.from_env(project_root)

    # Setup logging
    setup_logging(level=args.log_level or config.log_level)

    # Print banner
    print_banner()

    # Validate config
    errors = config.validate()
    if errors:
        logger = get_pipeline_logger()
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)

    # Determine poll interval
    poll_interval = args.poll_interval or config.watch_poll_seconds

    # Create and start watcher
    watcher = FolderWatcher(
        config=config,
        poll_interval=poll_interval,
        write_dev_files=args.write_files,
    )

    # Handle SIGTERM gracefully
    def handle_sigterm(signum, frame):
        console.print("\n[yellow]Received SIGTERM, shutting down...[/]")
        watcher.stop()

    signal.signal(signal.SIGTERM, handle_sigterm)

    # Start watching
    try:
        watcher.start()
    except KeyboardInterrupt:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
