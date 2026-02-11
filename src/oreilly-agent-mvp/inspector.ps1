# Quick MCP Inspector Launcher
# PowerShell 7+ - Start MCP Inspector web UI

#Requires -Version 7.0

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $ProjectRoot

# Ensure virtual environment exists and use its Python
$venvRoot = Join-Path $ProjectRoot ".venv"
$venvPython = Join-Path $venvRoot "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: .venv not found. Run .\scripts\setup.ps1 first." -ForegroundColor Red
    exit 1
}
$env:VIRTUAL_ENV = $venvRoot
$env:PATH = (Join-Path $venvRoot "Scripts") + ";" + $env:PATH

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

npx "@modelcontextprotocol/inspector" $venvPython -m agent_mvp.mcp_server
