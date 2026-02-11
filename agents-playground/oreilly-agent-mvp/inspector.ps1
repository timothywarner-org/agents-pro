# Quick MCP Inspector Launcher
# PowerShell 7+ - Start MCP Inspector web UI

#Requires -Version 7.0

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Set-Location $ProjectRoot

# Activate venv if available
$venvPath = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
}

Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║          O'Reilly Agent MVP - MCP Inspector          ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# Check for Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Node.js not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "MCP Inspector requires Node.js." -ForegroundColor Yellow
    Write-Host "Install from: https://nodejs.org/" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "Starting MCP Inspector..." -ForegroundColor Yellow
Write-Host "Opens web UI at: http://localhost:5173" -ForegroundColor Gray
Write-Host ""
Write-Host "This provides:" -ForegroundColor Cyan
Write-Host "  • Interactive tool testing" -ForegroundColor White
Write-Host "  • Resource browsing" -ForegroundColor White
Write-Host "  • Prompt templates" -ForegroundColor White
Write-Host "  • Real-time logs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor DarkGray
Write-Host ""

npx "@modelcontextprotocol/inspector" python -m agent_mvp.mcp_server
