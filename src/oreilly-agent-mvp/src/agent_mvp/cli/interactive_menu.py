"""Interactive CLI menu for the O'Reilly Agent MVP."""

import json
import os
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from ..config import Config
from ..issue_sources import FileIssueSource
from ..logging_setup import get_pipeline_logger, setup_logging
from ..persistence import SQLiteStore
from ..pipeline.run_once import run_pipeline, save_result
from ..util.reporting import format_run_report

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VENV_BIN = PROJECT_ROOT / ".venv" / "Scripts"
DEFAULT_PROXY_PORT = "6277"


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("O'Reilly Agent MVP - Interactive Menu")
    print("=" * 50)
    print("\nShow off the multi-agent GitHub issue triage and resolution pipeline.\n")
    print("\n1. Request an issue from GitHub")
    print("2. Load a mock issue")
    print("3. Start the folder watcher")
    print("4. Start MCP Server & Inspector (web UI)")
    print("q. Quit")
    print()


def handle_github_issue() -> Optional[Path]:
    """Fetch an issue from GitHub and save to incoming/."""
    from ..integrations.github_issue_fetcher import fetch_github_issue

    print("\n--- GitHub Issue Request ---")
    print("Repository: timothywarner-org/agents2")
    issue_number = input("Enter issue number: ").strip()

    if not issue_number.isdigit():
        print("Error: Issue number must be numeric.")
        return None

    try:
        print(f"\nFetching issue #{issue_number} from GitHub...")
        issue_data = fetch_github_issue(
            owner="timothywarner-org",
            repo="agents2",
            issue_number=int(issue_number),
        )

        incoming_dir = PROJECT_ROOT / "incoming"
        incoming_dir.mkdir(exist_ok=True)

        issue_file = incoming_dir / f"github_issue_{issue_number}.json"

        with open(issue_file, "w", encoding="utf-8") as f:
            json.dump(issue_data, f, indent=2)

        print(f"OK: Issue #{issue_number} saved to {issue_file}")
        print(f"  Title: {issue_data['title']}")
        return issue_file

    except Exception as e:
        print(f"\nError fetching issue: {e}")
        return None


def handle_mock_issue() -> Optional[Path]:
    """Let user select a mock issue file."""
    print("\n--- Mock Issue Selection ---")
    mock_dir = PROJECT_ROOT / "mock_issues"

    if not mock_dir.exists():
        print("Error: mock_issues/ directory not found.")
        return None

    mock_files = sorted(mock_dir.glob("*.json"))

    if not mock_files:
        print("Error: No mock issues found in mock_issues/")
        return None

    print("\nAvailable mock issues:")
    for idx, file in enumerate(mock_files, start=1):
        print(f"  {idx}. {file.name}")

    choice = input("\nSelect a mock issue (number): ").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(mock_files)):
        print("Error: Invalid selection.")
        return None

    selected = mock_files[int(choice) - 1]
    print(f"OK: Selected: {selected}")
    return selected


def handle_watcher() -> None:
    """Start the folder watcher with optional demo trigger."""
    import random
    import threading

    from ..watcher.folder_watcher import FolderWatcher

    print("\n--- Folder Watcher ---")

    incoming_dir = PROJECT_ROOT / "incoming"
    incoming_dir.mkdir(exist_ok=True)

    # Offer to trigger a demo by copying a mock issue
    print("\nOptions:")
    print("  1. Start watcher only (wait for files to be dropped)")
    print("  2. Start watcher + auto-trigger with a random mock issue (demo mode)")
    print()
    demo_choice = input("Choose mode (1 or 2, default=2): ").strip()

    auto_trigger = demo_choice != "1"

    print()
    print(f"Watching: {incoming_dir}")
    print("Press Ctrl+C to stop\n")

    # Setup config, logging, and watcher
    config = Config.from_env(PROJECT_ROOT)
    setup_logging(level=config.log_level)
    watcher = FolderWatcher(
        config=config,
        poll_interval=3.0,
        write_dev_files=False,
        verbose_polling=True,
    )

    def delayed_copy():
        """Copy a mock issue after a short delay to demonstrate the flow."""
        time.sleep(5)  # Wait 5 seconds so user can see initial polling
        mock_dir = PROJECT_ROOT / "mock_issues"
        mock_files = [f for f in mock_dir.glob("issue_*.json")]
        if mock_files:
            selected = random.choice(mock_files)
            dest = incoming_dir / f"demo_{selected.name}"
            shutil.copy(selected, dest)
            print(f"\n[Demo] Copied {selected.name} -> incoming/{dest.name}")
            print("[Demo] Watch the pipeline process it!\n")

    if auto_trigger:
        print("[Demo mode] A mock issue will be copied in ~5 seconds...")
        print()
        trigger_thread = threading.Thread(target=delayed_copy, daemon=True)
        trigger_thread.start()

    try:
        watcher.start()
    except KeyboardInterrupt:
        print("\n\nWatcher stopped.")


@contextmanager
def _temporary_env(overrides: dict[str, str]):
    """Temporarily set environment variables within a context."""
    original = {key: os.environ.get(key) for key in overrides}
    try:
        os.environ.update(overrides)
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _ensure_venv_activated() -> str:
    """Return path to venv Python, raising if missing."""
    venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        raise FileNotFoundError(
            "Virtual environment not found. Run scripts/setup.ps1 first."
        )
    os.environ.setdefault("VIRTUAL_ENV", str(PROJECT_ROOT / ".venv"))
    os.environ["PATH"] = f"{VENV_BIN};{os.environ.get('PATH', '')}"
    return str(venv_python)


def _find_npx() -> str | None:
    """Locate npx executable across different platforms."""
    for candidate in ("npx", "npx.cmd", "npx.exe"):
        path = shutil.which(candidate)
        if path:
            return path
    return None


def _find_node() -> str | None:
    """Locate node executable."""
    for candidate in ("node", "node.exe"):
        path = shutil.which(candidate)
        if path:
            return path
    return None


def _is_port_in_use(port: str) -> bool:
    """Check if a TCP port is in use by invoking netstat."""
    try:
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True, check=False
        )
        return port in result.stdout
    except Exception:
        return False


def _free_port(port: str) -> None:
    """Attempt to free the given port by killing node.exe processes bound to it."""
    netstat = subprocess.run(
        ["netstat", "-ano"], capture_output=True, text=True, check=False
    )
    pids = set()
    for line in netstat.stdout.splitlines():
        if f":{port}" in line and "LISTENING" in line:
            parts = line.split()
            if parts:
                pids.add(parts[-1])

    for pid in pids:
        subprocess.run(
            ["taskkill", "/F", "/PID", pid],
            capture_output=True,
            text=True,
            check=False,
        )


def handle_mcp_server_and_inspector() -> None:
    """Start the MCP Server and Inspector together."""

    print("\n--- MCP Server & Inspector ---")
    print("Starting MCP Server with Inspector web UI...")
    print("")
    print("This will:")
    print("  - Start the MCP server (exposes tools, resources, and prompts)")
    print("  - Launch the Inspector web UI for interactive testing")
    print("")

    # Check if Node.js is available
    if not _find_node():
        print("ERROR: Node.js not found!")
        print("")
        print("MCP Inspector requires Node.js.")
        print("Install from: https://nodejs.org/")
        print("")
        input("Press Enter to return to menu...")
        return

    venv_python = _ensure_venv_activated()
    npx_command = _find_npx()

    if not npx_command:
        print("ERROR: npx not found!")
        print("")
        print("Install Node.js 18+ or ensure your PATH includes npm's bin directory.")
        print("")
        input("Press Enter to return to menu...")
        return

    print("Inspector will open in your browser at http://localhost:5173")
    print("Press Ctrl+C to stop\n")

    proxy_port = os.environ.get("MCP_PROXY_PORT", DEFAULT_PROXY_PORT)
    if _is_port_in_use(proxy_port):
        print(f"Port {proxy_port} in use by another process. Attempting to free it...")
        _free_port(proxy_port)
        if _is_port_in_use(proxy_port):
            print(
                f"ERROR: Port {proxy_port} is still in use. Close other MCP Inspector instances and try again."
            )
            input("Press Enter to return to menu...")
            return

    try:
        with _temporary_env({"DANGEROUSLY_OMIT_AUTH": "true"}):
            subprocess.run(
                [
                    npx_command,
                    "@modelcontextprotocol/inspector",
                    venv_python,
                    "-m",
                    "agent_mvp.mcp_server",
                ],
                check=True,
                cwd=PROJECT_ROOT,
            )
    except KeyboardInterrupt:
        print("\n\nMCP Server & Inspector stopped.")
    except subprocess.CalledProcessError as e:
        print(f"\nError starting MCP Server & Inspector: {e}")
        input("Press Enter to return to menu...")


def process_issue_file(issue_file: Path) -> None:
    """Run the pipeline for a single issue file and write output."""
    config = Config.from_env(PROJECT_ROOT)
    setup_logging(level=config.log_level)
    logger = get_pipeline_logger()

    issue = FileIssueSource.from_path(issue_file)
    result = run_pipeline(issue, config, source_file=str(issue_file))

    output_dir = config.outgoing_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path, html_path = save_result(result, output_dir)

    db_path = config.project_root / "data" / "pipeline.db"
    store = SQLiteStore(db_path)
    store.save_result(result)

    logger.complete_run(
        run_id=result.run_id,
        issue_id=result.issue.issue_id,
        verdict=result.qa.verdict.value,
        output_file=str(json_path),
    )
    print("\n" + format_run_report(result, json_path, html_path))


def main() -> None:
    """Run the interactive menu loop."""
    print("\nWelcome to O'Reilly Agent MVP!")
    print(f"Project root: {PROJECT_ROOT}")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().lower()

        if choice == "q":
            print("\nGoodbye!")
            sys.exit(0)

        elif choice == "1":
            issue_file = handle_github_issue()
            if issue_file:
                proceed = input("\nProcess this issue now? (y/n): ").strip().lower()
                if proceed == "y":
                    try:
                        process_issue_file(issue_file)
                    except Exception as e:
                        print(f"\nPipeline failed: {e}")

        elif choice == "2":
            issue_file = handle_mock_issue()
            if issue_file:
                proceed = input(f"\nProcess {issue_file.name}? (y/n): ").strip().lower()
                if proceed == "y":
                    try:
                        process_issue_file(issue_file)
                    except Exception as e:
                        print(f"\nPipeline failed: {e}")

        elif choice == "3":
            handle_watcher()

        elif choice == "4":
            handle_mcp_server_and_inspector()

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, 4, or q.")


if __name__ == "__main__":
    main()
