"""
Structured logging setup with rich formatting.

Provides clear, readable output for demos with:
- Timestamps
- Role/component markers
- Colored output for different log levels
"""

from __future__ import annotations

import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


# Custom theme for consistent colors
THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "role.pm": "bold magenta",
    "role.dev": "bold blue",
    "role.qa": "bold yellow",
    "role.system": "bold white",
    "issue": "bold cyan",
    "file": "dim",
})

# Global console for consistent output
console = Console(theme=THEME)


def setup_logging(
    level: str = "INFO",
    show_path: bool = False,
) -> logging.Logger:
    """Configure logging with rich formatting.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR).
        show_path: Whether to show file paths in log output.

    Returns:
        Configured root logger.
    """
    # Configure rich handler
    handler = RichHandler(
        console=console,
        show_time=True,
        show_path=show_path,
        rich_tracebacks=True,
        tracebacks_show_locals=False,
        markup=True,
    )

    # Set format
    handler.setFormatter(logging.Formatter("%(message)s"))

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=[handler],
        force=True,
    )

    return logging.getLogger()


class PipelineLogger:
    """Structured logger for pipeline execution.

    Provides consistent, readable output for each stage of the pipeline.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the pipeline logger.

        Args:
            logger: Logger instance to use. If None, uses root logger.
        """
        self.logger = logger or logging.getLogger(__name__)

    def start_run(self, run_id: str, issue_id: str, source: str):
        """Log the start of a pipeline run."""
        console.rule("[bold green]Pipeline Run Starting[/]")
        console.print(f"  [bold]Run ID:[/] {run_id}")
        console.print(f"  [issue]Issue:[/] {issue_id}")
        console.print(f"  [file]Source:[/] {source}")
        console.print()

    def node_enter(self, node_name: str):
        """Log entering a pipeline node."""
        role_style = self._get_role_style(node_name)
        self.logger.info(f"[{role_style}]▶ Entering node: {node_name}[/]")

    def node_exit(self, node_name: str, summary: Optional[str] = None):
        """Log exiting a pipeline node."""
        role_style = self._get_role_style(node_name)
        msg = f"[{role_style}]✓ Completed node: {node_name}[/]"
        if summary:
            msg += f" - {summary}"
        self.logger.info(msg)

    def agent_message(self, role: str, message: str):
        """Log a message from an agent."""
        role_style = self._get_role_style(role)
        self.logger.info(f"  [{role_style}][{role.upper()}][/] {message}")

    def state_update(self, field: str, value: str):
        """Log a state field update."""
        self.logger.debug(f"  State updated: {field} = {value}")

    def complete_run(
        self,
        run_id: str,
        issue_id: str,
        verdict: str,
        output_file: str,
        duration: Optional[float] = None,
    ):
        """Log the completion of a pipeline run."""
        console.print()
        console.rule("[bold green]Pipeline Run Complete[/]")
        console.print(f"  [bold]Run ID:[/] {run_id}")
        console.print(f"  [issue]Issue:[/] {issue_id}")

        # Color verdict based on result
        if verdict == "pass":
            verdict_display = "[success]PASS[/]"
        elif verdict == "fail":
            verdict_display = "[error]FAIL[/]"
        else:
            verdict_display = "[warning]NEEDS-HUMAN[/]"
        console.print(f"  [bold]Verdict:[/] {verdict_display}")

        if duration is not None:
            console.print(f"  [bold]Duration:[/] {duration:.2f}s")

        console.print(f"  [file]Output:[/] {output_file}")
        console.print()

    def error(self, message: str, exc: Optional[Exception] = None):
        """Log an error."""
        self.logger.error(f"[error]✗ {message}[/]")
        if exc:
            self.logger.exception(exc)

    def warning(self, message: str):
        """Log a warning."""
        self.logger.warning(f"[warning]⚠ {message}[/]")

    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def file_operation(self, operation: str, path: str):
        """Log a file operation."""
        self.logger.info(f"  [file]{operation}:[/] {path}")

    def _get_role_style(self, name: str) -> str:
        """Get the style name for a role/node."""
        name_lower = name.lower()
        if "pm" in name_lower:
            return "role.pm"
        elif "dev" in name_lower:
            return "role.dev"
        elif "qa" in name_lower:
            return "role.qa"
        return "role.system"


# Module-level logger for convenience
_pipeline_logger: Optional[PipelineLogger] = None


def get_pipeline_logger() -> PipelineLogger:
    """Get the global pipeline logger instance.

    Returns:
        PipelineLogger instance.
    """
    global _pipeline_logger
    if _pipeline_logger is None:
        _pipeline_logger = PipelineLogger()
    return _pipeline_logger


def print_banner():
    """Print the application banner."""
    console.print()
    console.print("[bold cyan]╔══════════════════════════════════════════════════════════╗[/]")
    console.print("[bold cyan]║[/]  [bold white]O'Reilly AI Agents MVP[/]                                  [bold cyan]║[/]")
    console.print("[bold cyan]║[/]  [dim]Issue Triage + Implementation Draft Pipeline[/]            [bold cyan]║[/]")
    console.print("[bold cyan]╚══════════════════════════════════════════════════════════╝[/]")
    console.print()
