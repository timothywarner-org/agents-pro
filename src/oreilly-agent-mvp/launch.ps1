# Quick Launch - O'Reilly Agent MVP
# PowerShell 7+ script for easy access to all functions

#Requires -Version 7.0

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

function Show-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         O'Reilly Agent MVP - Quick Launch            ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Menu {
    Write-Host "Select an option:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] Interactive Menu" -ForegroundColor Green
    Write-Host "      └─ Main app with GitHub/Mock/Watcher options"
    Write-Host ""
    Write-Host "  [2] Run Pipeline Once" -ForegroundColor Green
    Write-Host "      └─ Process a single mock issue"
    Write-Host ""
    Write-Host "  [3] Start Folder Watcher" -ForegroundColor Green
    Write-Host "      └─ Auto-process files in incoming/"
    Write-Host ""
    Write-Host "  [4] Start MCP Server" -ForegroundColor Magenta
    Write-Host "      └─ For Claude Desktop / VS Code integration"
    Write-Host ""
    Write-Host "  [5] Start MCP Inspector" -ForegroundColor Magenta
    Write-Host "      └─ Web UI for testing MCP tools (requires Node.js)"
    Write-Host ""
    Write-Host "  [6] Run Tests" -ForegroundColor Cyan
    Write-Host "      └─ Validate MCP server and schemas"
    Write-Host ""
    Write-Host "  [Q] Quit" -ForegroundColor Red
    Write-Host ""
}

function Activate-VirtualEnv {
    $venvPath = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
    $script:VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    if (Test-Path $venvPath -and (Test-Path $script:VenvPython)) {
        & $venvPath
        Write-Host "Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Virtual environment not found. Run .\scripts\setup.ps1 first." -ForegroundColor Red
        exit 1
    }
}

function Invoke-InteractiveMenu {
    Write-Host ""
    Write-Host "Starting Interactive Menu..." -ForegroundColor Cyan
    Write-Host ""
    & $script:VenvPython -m agent_mvp.cli.interactive_menu
}

function Invoke-RunOnce {
    Write-Host ""
    Write-Host "Available mock issues:" -ForegroundColor Cyan
    Get-ChildItem "$ProjectRoot\mock_issues\*.json" | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor White
    }
    Write-Host ""
    $mockFile = Read-Host "Enter mock issue filename (or press Enter for issue_001.json)"
    if ([string]::IsNullOrWhiteSpace($mockFile)) {
        $mockFile = "issue_001.json"
    }

    $fullPath = Join-Path "$ProjectRoot\mock_issues" $mockFile
    if (Test-Path $fullPath) {
        Write-Host ""
        Write-Host "Processing $mockFile..." -ForegroundColor Cyan
        Write-Host ""
        & $script:VenvPython -m agent_mvp.pipeline.run_once $fullPath
    } else {
        Write-Host "Error: File not found: $mockFile" -ForegroundColor Red
        Read-Host "Press Enter to continue"
    }
}

function Invoke-Watcher {
    Write-Host ""
    Write-Host "Starting Folder Watcher..." -ForegroundColor Cyan
    Write-Host "Drop JSON files into: $ProjectRoot\incoming\" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    & $script:VenvPython -m agent_mvp.watcher.folder_watcher
}

function Invoke-MCPServer {
    Write-Host ""
    Write-Host "Starting MCP Server..." -ForegroundColor Magenta
    Write-Host "This exposes tools via stdio for Claude/VS Code" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    & $script:VenvPython -m agent_mvp.mcp_server
}

function Invoke-MCPInspector {
    Write-Host ""
    Write-Host "Starting MCP Inspector..." -ForegroundColor Magenta

    # Check for Node.js
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Host "ERROR: Node.js not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "MCP Inspector requires Node.js." -ForegroundColor Yellow
        Write-Host "Install from: https://nodejs.org/" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "Opening web UI at http://localhost:5173" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    npx "@modelcontextprotocol/inspector" $script:VenvPython -m agent_mvp.mcp_server
}

function Invoke-Tests {
    Write-Host ""
    Write-Host "Running tests..." -ForegroundColor Cyan
    Write-Host ""

    Write-Host "1. Schema validation tests:" -ForegroundColor Yellow
    & $script:VenvPython -m pytest tests/test_schema.py -v

    Write-Host ""
    Write-Host "2. MCP server validation:" -ForegroundColor Yellow
    & $script:VenvPython tests/test_mcp_server.py

    Write-Host ""
    Write-Host "Tests complete!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

# Main script
Set-Location $ProjectRoot
Clear-Host
Show-Banner

Write-Host "Project: $ProjectRoot" -ForegroundColor DarkGray
Write-Host ""

Activate-VirtualEnv

while ($true) {
    Write-Host ""
    Show-Menu

    $choice = Read-Host "Enter your choice"

    switch ($choice.ToUpper()) {
        "1" { Invoke-InteractiveMenu }
        "2" { Invoke-RunOnce }
        "3" { Invoke-Watcher }
        "4" { Invoke-MCPServer }
        "5" { Invoke-MCPInspector }
        "6" { Invoke-Tests }
        "Q" {
            Write-Host ""
            Write-Host "Goodbye! 👋" -ForegroundColor Cyan
            Write-Host ""
            exit 0
        }
        default {
            Write-Host ""
            Write-Host "Invalid choice. Please enter 1-6 or Q." -ForegroundColor Red
        }
    }
}
