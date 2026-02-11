"""
CLI command for running the pipeline once on a single issue.

Usage:
    python -m agent_mvp.pipeline.run_once --source mock --mock-file mock_issues/issue_001.json
    python -m agent_mvp.pipeline.run_once --source file --file incoming/some_issue.json
    python -m agent_mvp.pipeline.run_once --source github --repo owner/repo --issue 123
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from uuid import uuid4

from ..config import Config, get_config
from ..issue_sources import FileIssueSource, MockIssueSource
from ..logging_setup import setup_logging, get_pipeline_logger, print_banner
from ..models import Issue, PipelineResult
from ..persistence import SQLiteStore
from ..util.fs import safe_write_json, get_timestamped_filename
from ..util.html_report import save_html_report
from ..util.reporting import format_run_report
from .graph import create_pipeline_graph, PipelineState


def run_pipeline(
    issue: Issue,
    config: Config,
    source_file: str | None = None,
) -> PipelineResult:
    """Run the pipeline on an issue.

    Args:
        issue: The issue to process.
        config: Application configuration.
        source_file: Optional source file path for logging.

    Returns:
        PipelineResult with all agent outputs.

    Raises:
        Exception: If pipeline execution fails.
    """
    logger = get_pipeline_logger()

    # Generate run ID
    run_id = str(uuid4())
    start_time = time.time()

    # Log start
    logger.start_run(
        run_id=run_id,
        issue_id=issue.issue_id,
        source=source_file or "direct",
    )

    # Create initial state
    initial_state: PipelineState = {
        "run_id": run_id,
        "start_time": start_time,
        "source_file": source_file,
        "issue": issue.model_dump(),
        "token_usages": [],  # Track token usage per agent
    }

    # Create and run the graph
    graph = create_pipeline_graph()
    final_state = graph.invoke(initial_state)

    # Check for errors
    if final_state.get("error"):
        raise Exception(f"Pipeline failed: {final_state['error']}")

    # Parse result
    result = PipelineResult(**final_state["result"])

    return result


def save_result(
    result: PipelineResult,
    output_dir: Path,
    write_files: bool = False,
) -> tuple[Path, Path]:
    """Save the pipeline result to JSON and HTML files.

    Args:
        result: The pipeline result to save.
        output_dir: Directory to save to.
        write_files: Whether to also write dev files to disk.

    Returns:
        Tuple of (json_path, html_path) for the saved files.
    """
    logger = get_pipeline_logger()

    # Generate output filename
    issue_id_safe = result.issue.issue_id.replace("/", "_").replace("#", "_")
    filename = get_timestamped_filename(f"result_{issue_id_safe}")

    # Save result JSON
    output_path = output_dir / filename
    result_json = result.model_dump_json(indent=2)
    safe_write_json(result_json, output_path)

    logger.file_operation("Saved result", str(output_path))

    # Generate and save HTML report
    html_path = save_html_report(result, output_path)
    logger.file_operation("Saved HTML report", str(html_path))

    # Optionally write dev files
    if write_files and result.dev.files:
        files_dir = output_dir / f"files_{issue_id_safe}"
        files_dir.mkdir(parents=True, exist_ok=True)

        for dev_file in result.dev.files:
            file_path = files_dir / dev_file.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(dev_file.content, encoding="utf-8")
            logger.file_operation("Wrote file", str(file_path))

    return output_path, html_path


def main():
    """Main entry point for the run_once CLI."""
    parser = argparse.ArgumentParser(
        description="Run the agent pipeline on a single issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with a mock issue
  python -m agent_mvp.pipeline.run_once --source mock --mock-file mock_issues/issue_001.json

  # Run with a file from incoming/
  python -m agent_mvp.pipeline.run_once --source file --file incoming/my_issue.json

  # Run and write dev files to disk
  python -m agent_mvp.pipeline.run_once --source mock --mock-file mock_issues/issue_001.json --write-files

  # Fetch from GitHub via MCP and run
  python -m agent_mvp.pipeline.run_once --source github --repo owner/repo --issue 123
        """,
    )

    parser.add_argument(
        "--source",
        choices=["mock", "file", "github"],
        required=True,
        help="Issue source: 'mock', 'file', or 'github' (via MCP)",
    )
    parser.add_argument(
        "--mock-file",
        type=str,
        help="Path to mock issue file (relative to project root or absolute)",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to issue file (relative or absolute)",
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="GitHub repo in 'owner/repo' format (for --source github)",
    )
    parser.add_argument(
        "--issue",
        type=int,
        help="GitHub issue number (for --source github)",
    )
    parser.add_argument(
        "--write-files",
        action="store_true",
        help="Write dev files to disk in addition to result JSON",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory (default: outgoing/)",
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
        # Try to find project root by looking for pyproject.toml
        cwd = Path.cwd()
        if (cwd / "pyproject.toml").exists():
            project_root = cwd
        elif (cwd.parent / "pyproject.toml").exists():
            project_root = cwd.parent
        else:
            project_root = cwd

    # Load config
    config = Config.from_env(project_root)

    # Setup logging
    setup_logging(level=args.log_level or config.log_level)

    # Print banner
    print_banner()

    # Validate arguments
    if args.source == "mock" and not args.mock_file:
        parser.error("--mock-file is required when --source is 'mock'")
    if args.source == "file" and not args.file:
        parser.error("--file is required when --source is 'file'")
    if args.source == "github" and (not args.repo or not args.issue):
        parser.error("--repo and --issue are required when --source is 'github'")

    # Load issue
    logger = get_pipeline_logger()
    try:
        if args.source == "mock":
            mock_path = Path(args.mock_file)
            if not mock_path.is_absolute():
                mock_path = project_root / mock_path
            issue = FileIssueSource.from_path(mock_path)
            source_file = str(mock_path)
        elif args.source == "github":
            # Fetch from GitHub via MCP
            from ..integrations.github_issue_fetcher import fetch_github_issue
            owner, repo = args.repo.split("/")
            issue_data = fetch_github_issue(owner, repo, args.issue)
            issue = Issue(**issue_data)
            source_file = f"github:{args.repo}#{args.issue}"
        else:
            file_path = Path(args.file)
            if not file_path.is_absolute():
                file_path = project_root / file_path
            issue = FileIssueSource.from_path(file_path)
            source_file = str(file_path)

    except FileNotFoundError as e:
        logger.error(f"Issue file not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to load issue: {e}")
        sys.exit(1)

    # Validate config
    errors = config.validate()
    if errors:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)

    # Determine output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = project_root / output_dir
    else:
        output_dir = config.outgoing_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    # Run pipeline
    try:
        result = run_pipeline(issue, config, source_file)

        # Save result to file (JSON + HTML)
        json_path, html_path = save_result(result, output_dir, args.write_files)

        # Persist to SQLite database
        db_path = project_root / 'data' / 'pipeline.db'
        store = SQLiteStore(db_path)
        store.save_result(result)
        logger.file_operation('Persisted to database', str(db_path))

        # Print run report with token usage
        print("\n" + format_run_report(result, json_path, html_path))

        # Log completion
        logger.complete_run(
            run_id=result.run_id,
            issue_id=result.issue.issue_id,
            verdict=result.qa.verdict.value,
            output_file=str(json_path),
        )

        sys.exit(0)

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
